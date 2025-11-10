#!/usr/bin/env python3
"""
🌉 VCM Dashboard API Bridge
==========================

API FastAPI que faz a ponte entre o Dashboard React e os scripts Python existentes.
Permite executar os scripts de automação através de chamadas HTTP.

Funcionalidades:
- Executar scripts de geração de biografias
- Executar cascata de scripts (1-5)
- Verificar status dos scripts
- Sincronizar dados com Supabase
- Ingestão RAG no Supabase

Autor: Sergio Castro
Data: November 2025
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import subprocess
import sys
import os
import json
import asyncio
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import RAG service
try:
    rag_path = Path(__file__).parent / "AUTOMACAO" / "02_PROCESSAMENTO_PERSONAS"
    sys.path.append(str(rag_path))
    from rag_ingestion_service import ingest_empresa_rag, get_rag_status
    RAG_AVAILABLE = True
    logger.info("✅ RAG service carregado com sucesso")
except ImportError as e:
    logger.warning(f"⚠️ RAG service não disponível: {e}")
    RAG_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VCM Dashboard API Bridge", version="1.0.0")

# Configurar CORS para permitir conexões do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class BiografiaGenerationRequest(BaseModel):
    empresa_codigo: str
    empresa_nome: str
    total_personas: Optional[int] = 20
    idiomas: Optional[List[str]] = ["pt", "en"]
    pais: Optional[str] = "BR"

class CascadeScriptRequest(BaseModel):
    empresa_codigo: str
    force_regenerate: Optional[bool] = False

class ScriptResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output: Optional[str] = None

# Configurações
AUTOMACAO_DIR = Path(__file__).parent / "AUTOMACAO"
SCRIPT_PATHS = {
    "biografia": AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "05_auto_biografia_generator.py",
    "competencias": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "01_generate_competencias.py",
    "tech_specs": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "02_generate_tech_specs.py",
    "rag": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "03_generate_rag.py",
    "fluxos": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "04_generate_fluxos_analise.py",
    "workflows": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "05_generate_workflows_n8n.py",
}

def run_python_script(script_path: Path, args: List[str] = None) -> Dict[str, Any]:
    """
    Executa um script Python e retorna o resultado
    """
    try:
        if not script_path.exists():
            return {
                "success": False,
                "error": f"Script não encontrado: {script_path}"
            }
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        logger.info(f"Executando: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos timeout
            cwd=script_path.parent
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "return_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Script timeout (5 minutos)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erro ao executar script: {str(e)}"
        }

@app.get("/")
async def root():
    """Status da API"""
    return {
        "message": "VCM Dashboard API Bridge está rodando",
        "version": "1.0.0",
        "scripts_available": list(SCRIPT_PATHS.keys())
    }

@app.post("/generate-biografias", response_model=ScriptResponse)
async def generate_biografias(request: BiografiaGenerationRequest):
    """
    Gera biografias para uma empresa usando o script 05_auto_biografia_generator.py
    """
    try:
        script_path = SCRIPT_PATHS["biografia"]
        
        # Executar script de biografias
        result = run_python_script(script_path, [
            "--empresa-codigo", request.empresa_codigo,
            "--empresa-nome", request.empresa_nome,
            "--total-personas", str(request.total_personas),
            "--pais", request.pais
        ])
        
        if result["success"]:
            return ScriptResponse(
                success=True,
                message=f"Biografias geradas com sucesso para {request.empresa_nome}",
                data={
                    "empresa_codigo": request.empresa_codigo,
                    "total_personas": request.total_personas
                },
                output=result["output"]
            )
        else:
            return ScriptResponse(
                success=False,
                message="Erro ao gerar biografias",
                error=result["error"],
                output=result.get("output")
            )
            
    except Exception as e:
        logger.error(f"Erro em generate_biografias: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )

@app.post("/cascade-script/{script_number}", response_model=ScriptResponse)
async def execute_cascade_script(script_number: int, request: CascadeScriptRequest):
    """
    Executa um script específico da cascata (1-5)
    """
    if script_number not in [1, 2, 3, 4, 5]:
        raise HTTPException(status_code=400, detail="Número do script deve ser entre 1 e 5")
    
    script_map = {
        1: "competencias",
        2: "tech_specs", 
        3: "rag",
        4: "fluxos",
        5: "workflows"
    }
    
    try:
        script_key = script_map[script_number]
        script_path = SCRIPT_PATHS[script_key]
        
        args = ["--empresa-codigo", request.empresa_codigo]
        if request.force_regenerate:
            args.extend(["--force-regenerate"])
        
        result = run_python_script(script_path, args)
        
        if result["success"]:
            return ScriptResponse(
                success=True,
                message=f"Script {script_number} executado com sucesso",
                data={
                    "script_number": script_number,
                    "script_name": script_key,
                    "empresa_codigo": request.empresa_codigo
                },
                output=result["output"]
            )
        else:
            return ScriptResponse(
                success=False,
                message=f"Erro ao executar script {script_number}",
                error=result["error"],
                output=result.get("output")
            )
            
    except Exception as e:
        logger.error(f"Erro em execute_cascade_script: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )

@app.post("/full-cascade", response_model=ScriptResponse)
async def execute_full_cascade(request: CascadeScriptRequest, background_tasks: BackgroundTasks):
    """
    Executa toda a cascata de scripts (1-5) em sequência
    """
    try:
        results = []
        for script_num in [1, 2, 3, 4, 5]:
            script_map = {
                1: "competencias",
                2: "tech_specs",
                3: "rag", 
                4: "fluxos",
                5: "workflows"
            }
            
            script_key = script_map[script_num]
            script_path = SCRIPT_PATHS[script_key]
            
            logger.info(f"Executando script {script_num}: {script_key}")
            
            args = ["--empresa-codigo", request.empresa_codigo]
            if request.force_regenerate:
                args.extend(["--force-regenerate"])
            
            result = run_python_script(script_path, args)
            results.append({
                "script_number": script_num,
                "script_name": script_key,
                "success": result["success"],
                "output": result.get("output", ""),
                "error": result.get("error")
            })
            
            # Se um script falha, para a execução
            if not result["success"]:
                return ScriptResponse(
                    success=False,
                    message=f"Cascata interrompida no script {script_num}",
                    data={"results": results},
                    error=result["error"]
                )
        
        return ScriptResponse(
            success=True,
            message="Cascata completa executada com sucesso",
            data={
                "empresa_codigo": request.empresa_codigo,
                "scripts_executed": 5,
                "results": results
            }
        )
        
    except Exception as e:
        logger.error(f"Erro em execute_full_cascade: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )

@app.get("/script-status/{empresa_codigo}", response_model=ScriptResponse)
async def get_script_status(empresa_codigo: str):
    """
    Verifica o status dos scripts para uma empresa
    """
    try:
        # Verificar se existem outputs dos scripts
        output_dir = AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output"
        personas_config_path = output_dir / "personas_config.json"
        
        status = {
            "empresa_codigo": empresa_codigo,
            "biografias_generated": False,
            "scripts_completed": [],
            "output_directories": []
        }
        
        # Verificar biografias
        if personas_config_path.exists():
            status["biografias_generated"] = True
            
        # Verificar outputs dos scripts 1-5
        script_dirs = {
            1: "competencias_output",
            2: "tech_specs_output", 
            3: "rag_output",
            4: "fluxos_output",
            5: "workflows_output"
        }
        
        for script_num, dir_name in script_dirs.items():
            script_output_dir = AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / dir_name
            if script_output_dir.exists():
                status["scripts_completed"].append(script_num)
                status["output_directories"].append(str(script_output_dir))
        
        return ScriptResponse(
            success=True,
            message="Status verificado com sucesso",
            data=status
        )
        
    except Exception as e:
        logger.error(f"Erro em get_script_status: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro ao verificar status",
            error=str(e)
        )

@app.get("/script-outputs/{empresa_codigo}", response_model=ScriptResponse)
async def list_script_outputs(empresa_codigo: str):
    """
    Lista os outputs gerados pelos scripts
    """
    try:
        outputs = {
            "empresa_codigo": empresa_codigo,
            "files": [],
            "directories": []
        }
        
        # Listar arquivos de output
        base_dirs = [
            AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output",
            AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS"
        ]
        
        for base_dir in base_dirs:
            if base_dir.exists():
                for item in base_dir.iterdir():
                    if item.is_file() and item.suffix in ['.json', '.md', '.txt']:
                        outputs["files"].append({
                            "name": item.name,
                            "path": str(item),
                            "size": item.stat().st_size,
                            "modified": item.stat().st_mtime
                        })
                    elif item.is_dir():
                        outputs["directories"].append({
                            "name": item.name,
                            "path": str(item),
                            "file_count": len(list(item.glob("*")))
                        })
        
        return ScriptResponse(
            success=True,
            message="Outputs listados com sucesso",
            data=outputs
        )
        
    except Exception as e:
        logger.error(f"Erro em list_script_outputs: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro ao listar outputs",
            error=str(e)

# ========================================
# 🧠 RAG ENDPOINTS
# ========================================

class RAGRequest(BaseModel):
    empresa_id: str
    force_update: Optional[bool] = False

class RAGResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.post("/api/rag/ingest", response_model=RAGResponse)
async def ingest_rag_data(request: RAGRequest, background_tasks: BackgroundTasks):
    """
    🧠 Ingerir dados RAG para uma empresa
    
    Processa biografias, competências, workflows e knowledge base
    da empresa para o sistema RAG no Supabase.
    """
    try:
        logger.info(f"🚀 Iniciando ingestão RAG para empresa: {request.empresa_id}")
        
        if not RAG_AVAILABLE:
            return RAGResponse(
                success=False,
                message="Serviço RAG não disponível",
                error="RAG service não está carregado"
            )
        
        # Executar ingestão em background
        def run_rag_ingestion():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    ingest_empresa_rag(request.empresa_id, request.force_update)
                )
                logger.info(f"✅ Ingestão RAG concluída: {result}")
                return result
            except Exception as e:
                logger.error(f"❌ Erro na ingestão RAG: {e}")
                raise e
            finally:
                loop.close()
        
        # Executar em background
        background_tasks.add_task(run_rag_ingestion)
        
        return RAGResponse(
            success=True,
            message=f"Ingestão RAG iniciada para empresa {request.empresa_id}",
            data={
                "empresa_id": request.empresa_id,
                "force_update": request.force_update,
                "status": "started"
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Erro em ingest_rag_data: {str(e)}")
        return RAGResponse(
            success=False,
            message="Erro ao iniciar ingestão RAG",
            error=str(e)
        )

@app.get("/api/rag/status/{empresa_id}", response_model=RAGResponse)
async def get_rag_status_endpoint(empresa_id: str):
    """
    📊 Obter status da ingestão RAG de uma empresa
    
    Retorna informações sobre jobs recentes, estatísticas
    e última sincronização RAG.
    """
    try:
        logger.info(f"📊 Consultando status RAG para empresa: {empresa_id}")
        
        if not RAG_AVAILABLE:
            return RAGResponse(
                success=False,
                message="Serviço RAG não disponível",
                error="RAG service não está carregado"
            )
        
        # Obter status RAG
        status_data = get_rag_status(empresa_id)
        
        if 'error' in status_data:
            return RAGResponse(
                success=False,
                message="Erro ao obter status RAG",
                error=status_data['error']
            )
        
        return RAGResponse(
            success=True,
            message="Status RAG obtido com sucesso",
            data={
                "empresa_id": empresa_id,
                **status_data
            }
        )
        
    except Exception as e:
        logger.error(f"❌ Erro em get_rag_status_endpoint: {str(e)}")
        return RAGResponse(
            success=False,
            message="Erro ao consultar status RAG",
            error=str(e)
        )

@app.post("/api/rag/ingest-sync", response_model=RAGResponse)
async def ingest_rag_data_sync(request: RAGRequest):
    """
    🧠 Ingerir dados RAG de forma síncrona
    
    Versão síncrona da ingestão RAG para casos onde
    é necessário aguardar o resultado.
    """
    try:
        logger.info(f"🔄 Ingestão RAG síncrona para empresa: {request.empresa_id}")
        
        if not RAG_AVAILABLE:
            return RAGResponse(
                success=False,
                message="Serviço RAG não disponível",
                error="RAG service não está carregado"
            )
        
        # Executar ingestão síncrona
        result = await ingest_empresa_rag(request.empresa_id, request.force_update)
        
        return RAGResponse(
            success=True,
            message="Ingestão RAG concluída com sucesso",
            data=result
        )
        
    except Exception as e:
        logger.error(f"❌ Erro em ingest_rag_data_sync: {str(e)}")
        return RAGResponse(
            success=False,
            message="Erro na ingestão RAG síncrona",
            error=str(e)
        )

@app.get("/api/rag/health")
async def rag_health_check():
    """
    ❤️ Verificar saúde do serviço RAG
    """
    try:
        health_status = {
            "rag_available": RAG_AVAILABLE,
            "timestamp": str(asyncio.get_event_loop().time()),
            "status": "healthy" if RAG_AVAILABLE else "rag_service_unavailable"
        }
        
        if RAG_AVAILABLE:
            # Verificar conexão Supabase através do serviço RAG
            try:
                from rag_ingestion_service import rag_service
                has_supabase = rag_service.supabase is not None
                health_status["supabase_connected"] = has_supabase
                health_status["status"] = "healthy" if has_supabase else "supabase_disconnected"
            except Exception as e:
                health_status["supabase_connected"] = False
                health_status["supabase_error"] = str(e)
                health_status["status"] = "supabase_error"
        
        return {
            "success": True,
            "message": "Health check concluído",
            "data": health_status
        }
        
    except Exception as e:
        logger.error(f"❌ Erro em rag_health_check: {str(e)}")
        return {
            "success": False,
            "message": "Erro no health check RAG",
            "error": str(e)
        }
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando VCM Dashboard API Bridge...")
    print("📁 Diretório de automação:", AUTOMACAO_DIR)
    print("🔗 API estará disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    
    uvicorn.run(
        "api_bridge:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )