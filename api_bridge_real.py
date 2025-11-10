#!/usr/bin/env python3
"""
🌉 VCM DASHBOARD API BRIDGE - REAL
==================================

API FastAPI que faz a ponte entre o Dashboard e os scripts Python existentes.
EXECUTA OS SCRIPTS REAIS sem modificá-los.

Funcionalidades:
- Executar gerador de biografias
- Executar cascata de scripts (1-5) em sequência
- Monitorar status e logs em tempo real
- Sincronizar dados com Supabase

Autor: Sergio Castro
Data: November 2025
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_bridge.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VCM Dashboard API Bridge - REAL",
    description="API para executar scripts Python do VCM",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class BiografiaRequest(BaseModel):
    empresa_nome: str = "TechVision Solutions"
    empresa_industry: str = "tecnologia"
    nacionalidade: str = "latinos"
    ceo_genero: str = "feminino"
    executivos_homens: int = 2
    executivos_mulheres: int = 2
    assistentes_homens: int = 2
    assistentes_mulheres: int = 3
    especialistas_homens: int = 3
    especialistas_mulheres: int = 3
    idiomas_extras: List[str] = ["alemão", "japonês"]

class ScriptRequest(BaseModel):
    script_number: int
    force_regenerate: bool = False

class ScriptResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output: Optional[str] = None
    execution_time: Optional[float] = None

# Configurações de caminhos
BASE_DIR = Path(__file__).parent
AUTOMACAO_DIR = BASE_DIR / "AUTOMACAO"
BIO_SCRIPT = AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "05_auto_biografia_generator.py"
SCRIPT_PATHS = {
    1: AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "01_generate_competencias.py",
    2: AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "02_generate_tech_specs.py",
    3: AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "03_generate_rag.py",
    4: AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "04_generate_fluxos_analise.py",
    5: AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "05_generate_workflows_n8n.py",
}

# Controle de execução
execution_status = {
    "biografia": {"running": False, "last_run": None, "last_result": None},
    "script_1": {"running": False, "last_run": None, "last_result": None},
    "script_2": {"running": False, "last_run": None, "last_result": None},
    "script_3": {"running": False, "last_run": None, "last_result": None},
    "script_4": {"running": False, "last_run": None, "last_result": None},
    "script_5": {"running": False, "last_run": None, "last_result": None},
    "cascade": {"running": False, "last_run": None, "last_result": None},
}

def run_python_script(script_path: Path, cwd: Path = None, timeout: int = 300) -> Dict[str, Any]:
    """
    Executa um script Python e retorna o resultado
    """
    start_time = datetime.now()
    
    try:
        if not script_path.exists():
            return {
                "success": False,
                "error": f"Script não encontrado: {script_path}",
                "execution_time": 0
            }
        
        cmd = [sys.executable, str(script_path)]
        working_dir = cwd or script_path.parent
        
        logger.info(f"Executando: {' '.join(cmd)} em {working_dir}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=working_dir,
            encoding='utf-8',
            errors='replace'
        )
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "return_code": result.returncode,
            "execution_time": execution_time
        }
        
    except subprocess.TimeoutExpired:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "success": False,
            "error": f"Script timeout ({timeout} segundos)",
            "execution_time": execution_time
        }
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "success": False,
            "error": f"Erro ao executar script: {str(e)}",
            "execution_time": execution_time
        }

def copy_personas_to_processing_dir() -> bool:
    """
    Copia personas geradas para o diretório esperado pelos scripts de processamento
    """
    try:
        src = AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output" / "04_PERSONAS_SCRIPTS_1_2_3"
        dst = AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS"
        
        if not src.exists():
            logger.error(f"Pasta fonte não encontrada: {src}")
            return False
        
        # Remover destino se existir
        if dst.exists():
            import shutil
            shutil.rmtree(dst)
        
        # Copiar
        import shutil
        shutil.copytree(src, dst)
        
        logger.info(f"Personas copiadas: {src} → {dst}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao copiar personas: {str(e)}")
        return False

@app.get("/")
async def root():
    """Status da API"""
    return {
        "message": "VCM Dashboard API Bridge - REAL está rodando",
        "version": "1.0.0",
        "status": "active",
        "scripts_available": list(SCRIPT_PATHS.keys()),
        "base_dir": str(BASE_DIR),
        "automacao_dir": str(AUTOMACAO_DIR)
    }

@app.get("/status")
async def get_status():
    """Status de execução de todos os scripts"""
    return {
        "execution_status": execution_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/generate-biografias", response_model=ScriptResponse)
async def generate_biografias(request: BiografiaRequest):
    """
    Executa o gerador de biografias
    """
    if execution_status["biografia"]["running"]:
        raise HTTPException(status_code=429, detail="Gerador de biografias já está executando")
    
    execution_status["biografia"]["running"] = True
    execution_status["biografia"]["last_run"] = datetime.now().isoformat()
    
    try:
        logger.info("Iniciando geração de biografias")
        
        # Executar script de biografias
        result = run_python_script(BIO_SCRIPT, timeout=600)  # 10 minutos
        
        if result["success"]:
            # Copiar personas para diretório de processamento
            copy_success = copy_personas_to_processing_dir()
            
            # Verificar se personas_config.json foi gerado
            config_file = AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output" / "personas_config.json"
            config_exists = config_file.exists()
            
            execution_status["biografia"]["last_result"] = "success"
            
            return ScriptResponse(
                success=True,
                message="Biografias geradas com sucesso",
                data={
                    "config_file": str(config_file) if config_exists else None,
                    "config_exists": config_exists,
                    "copy_success": copy_success,
                    "output_dir": str(AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output"),
                    "processing_dir": str(AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS")
                },
                output=result["output"],
                execution_time=result["execution_time"]
            )
        else:
            execution_status["biografia"]["last_result"] = "error"
            return ScriptResponse(
                success=False,
                message="Erro na geração de biografias",
                error=result["error"],
                output=result["output"],
                execution_time=result["execution_time"]
            )
            
    except Exception as e:
        execution_status["biografia"]["last_result"] = "error"
        logger.error(f"Erro em generate_biografias: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )
    finally:
        execution_status["biografia"]["running"] = False

@app.post("/run-script/{script_number}", response_model=ScriptResponse)
async def run_script(script_number: int, request: ScriptRequest):
    """
    Executa um script específico da cascata (1-5)
    """
    if script_number not in SCRIPT_PATHS:
        raise HTTPException(status_code=400, detail=f"Script {script_number} não existe")
    
    script_key = f"script_{script_number}"
    
    if execution_status[script_key]["running"]:
        raise HTTPException(status_code=429, detail=f"Script {script_number} já está executando")
    
    execution_status[script_key]["running"] = True
    execution_status[script_key]["last_run"] = datetime.now().isoformat()
    
    try:
        script_path = SCRIPT_PATHS[script_number]
        logger.info(f"Executando Script {script_number}: {script_path}")
        
        # Verificar se 04_PERSONAS_COMPLETAS existe
        personas_dir = AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS"
        if not personas_dir.exists():
            return ScriptResponse(
                success=False,
                message=f"Diretório 04_PERSONAS_COMPLETAS não encontrado. Execute primeiro a geração de biografias.",
                error="Prerequisite missing"
            )
        
        result = run_python_script(script_path, timeout=600)  # 10 minutos
        
        if result["success"]:
            execution_status[script_key]["last_result"] = "success"
            return ScriptResponse(
                success=True,
                message=f"Script {script_number} executado com sucesso",
                data={
                    "script_number": script_number,
                    "script_path": str(script_path)
                },
                output=result["output"],
                execution_time=result["execution_time"]
            )
        else:
            execution_status[script_key]["last_result"] = "error"
            return ScriptResponse(
                success=False,
                message=f"Erro na execução do Script {script_number}",
                error=result["error"],
                output=result["output"],
                execution_time=result["execution_time"]
            )
            
    except Exception as e:
        execution_status[script_key]["last_result"] = "error"
        logger.error(f"Erro em run_script {script_number}: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )
    finally:
        execution_status[script_key]["running"] = False

@app.post("/run-cascade", response_model=ScriptResponse)
async def run_cascade(background_tasks: BackgroundTasks):
    """
    Executa toda a cascata de scripts (1-5) em sequência
    """
    if execution_status["cascade"]["running"]:
        raise HTTPException(status_code=429, detail="Cascata já está executando")
    
    execution_status["cascade"]["running"] = True
    execution_status["cascade"]["last_run"] = datetime.now().isoformat()
    
    try:
        logger.info("Iniciando cascata completa de scripts")
        
        # Verificar prerequisito
        personas_dir = AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS"
        if not personas_dir.exists():
            execution_status["cascade"]["last_result"] = "error"
            return ScriptResponse(
                success=False,
                message="Diretório 04_PERSONAS_COMPLETAS não encontrado. Execute primeiro a geração de biografias.",
                error="Prerequisite missing"
            )
        
        results = []
        total_time = 0
        
        for script_num in [1, 2, 3, 4, 5]:
            script_path = SCRIPT_PATHS[script_num]
            script_key = f"script_{script_num}"
            
            logger.info(f"Executando Script {script_num} na cascata")
            execution_status[script_key]["running"] = True
            execution_status[script_key]["last_run"] = datetime.now().isoformat()
            
            result = run_python_script(script_path, timeout=600)
            total_time += result.get("execution_time", 0)
            
            if result["success"]:
                execution_status[script_key]["last_result"] = "success"
                results.append({
                    "script": script_num,
                    "status": "success",
                    "execution_time": result["execution_time"]
                })
            else:
                execution_status[script_key]["last_result"] = "error"
                results.append({
                    "script": script_num,
                    "status": "error",
                    "error": result["error"],
                    "execution_time": result["execution_time"]
                })
                # Parar cascata em caso de erro
                break
            
            execution_status[script_key]["running"] = False
        
        # Verificar se todos foram executados com sucesso
        all_success = all(r["status"] == "success" for r in results)
        
        if all_success:
            execution_status["cascade"]["last_result"] = "success"
            return ScriptResponse(
                success=True,
                message="Cascata completa executada com sucesso",
                data={
                    "scripts_executed": len(results),
                    "results": results,
                    "total_execution_time": total_time
                },
                execution_time=total_time
            )
        else:
            execution_status["cascade"]["last_result"] = "error"
            return ScriptResponse(
                success=False,
                message=f"Cascata falhou no script {results[-1]['script']}",
                data={
                    "scripts_executed": len(results),
                    "results": results,
                    "total_execution_time": total_time
                },
                error=f"Falha no script {results[-1]['script']}",
                execution_time=total_time
            )
            
    except Exception as e:
        execution_status["cascade"]["last_result"] = "error"
        logger.error(f"Erro em run_cascade: {str(e)}")
        return ScriptResponse(
            success=False,
            message="Erro interno do servidor",
            error=str(e)
        )
    finally:
        execution_status["cascade"]["running"] = False

@app.get("/outputs")
async def list_outputs():
    """
    Lista todos os outputs gerados pelos scripts
    """
    try:
        outputs = {
            "biografias": {},
            "competencias": {},
            "personas_config": None
        }
        
        # Verificar personas_config.json
        config_file = AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "test_biografias_output" / "personas_config.json"
        if config_file.exists():
            outputs["personas_config"] = {
                "path": str(config_file),
                "size": config_file.stat().st_size,
                "modified": datetime.fromtimestamp(config_file.stat().st_mtime).isoformat()
            }
        
        # Verificar pasta de personas processadas
        personas_dir = AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS"
        if personas_dir.exists():
            for categoria_dir in personas_dir.iterdir():
                if categoria_dir.is_dir():
                    categoria = categoria_dir.name
                    outputs["biografias"][categoria] = []
                    outputs["competencias"][categoria] = []
                    
                    for persona_dir in categoria_dir.iterdir():
                        if persona_dir.is_dir():
                            persona_name = persona_dir.name
                            
                            # Verificar biografia
                            bio_files = list(persona_dir.glob("*_bio.md"))
                            if bio_files:
                                outputs["biografias"][categoria].append({
                                    "persona": persona_name,
                                    "bio_file": str(bio_files[0])
                                })
                            
                            # Verificar competências
                            comp_dir = persona_dir / "competencias"
                            if comp_dir.exists():
                                json_file = comp_dir / "competencias_core.json"
                                md_file = comp_dir / "competencias_detalhadas.md"
                                
                                if json_file.exists() and md_file.exists():
                                    outputs["competencias"][categoria].append({
                                        "persona": persona_name,
                                        "json_file": str(json_file),
                                        "md_file": str(md_file)
                                    })
        
        return {
            "success": True,
            "message": "Outputs listados com sucesso",
            "data": outputs,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erro em list_outputs: {str(e)}")
        return {
            "success": False,
            "message": "Erro ao listar outputs",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """
    Health check da API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "scripts_status": {
            "biografia_script": BIO_SCRIPT.exists(),
            "script_1": SCRIPT_PATHS[1].exists(),
            "script_2": SCRIPT_PATHS[2].exists(),
            "script_3": SCRIPT_PATHS[3].exists(),
            "script_4": SCRIPT_PATHS[4].exists(),
            "script_5": SCRIPT_PATHS[5].exists(),
        },
        "directories": {
            "automacao": AUTOMACAO_DIR.exists(),
            "personas_completas": (AUTOMACAO_DIR / "04_PERSONAS_COMPLETAS").exists()
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Iniciando VCM Dashboard API Bridge - REAL...")
    print(f"📁 Diretório base: {BASE_DIR}")
    print(f"📁 Diretório automação: {AUTOMACAO_DIR}")
    print("🔗 API estará disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    print("🏥 Health check em: http://localhost:8000/health")
    
    uvicorn.run(
        "api_bridge_real:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )