#!/usr/bin/env python3
"""
🌉 VCM Dashboard API Bridge - LLM Integrated
===========================================

API FastAPI que integra o Dashboard React com o novo sistema LLM.
Suporte para Google AI (primary) + OpenAI (fallback) + Nano Banana avatares.

Funcionalidades:
- Geração de biografias com LLM
- Execução da cascata de scripts (1-6)
- Geração de avatares
- Tracking de custos e qualidade
- Integração com Supabase

Autor: VCM Team
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
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VCM Dashboard API Bridge LLM", version="2.0.0")

# Configurar CORS para permitir conexões do React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import dos serviços LLM (com fallback para scripts antigos)
try:
    sys.path.append(str(Path(__file__).parent / "AUTOMACAO" / "02_PROCESSAMENTO_PERSONAS"))
    from llm_service import LLMService, ContentType, get_cost_summary
    from avatar_service import generate_avatar_for_persona, get_avatar_cost_summary
    import importlib.util
    
    # Import dinâmico do script com número no nome
    spec = importlib.util.spec_from_file_location(
        "biografias_llm", 
        str(Path(__file__).parent / "AUTOMACAO" / "02_PROCESSAMENTO_PERSONAS" / "01_generate_biografias_llm.py")
    )
    biografias_llm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(biografias_llm)
    generate_biografias_api = biografias_llm.generate_biografias_api
    LLM_AVAILABLE = True
    logger.info("✅ Serviços LLM carregados com sucesso")
except ImportError as e:
    logger.warning(f"⚠️ Serviços LLM não disponíveis: {e}")
    LLM_AVAILABLE = False

# Modelos Pydantic
class NacionalidadePercentual(BaseModel):
    tipo: str
    percentual: int

class BiografiaGenerationRequest(BaseModel):
    name: str  # Nome da empresa
    industry: str  # Setor da empresa
    nacionalidades: List[NacionalidadePercentual] = [{"tipo": "brasileira", "percentual": 100}]
    ceo_genero: Optional[str] = "feminino"
    total_personas: Optional[int] = 5
    use_llm: Optional[bool] = True

class LLMBiografiaRequest(BaseModel):
    empresa_nome: str
    setor: str
    nacionalidades: List[NacionalidadePercentual] = [{"tipo": "brasileira", "percentual": 100}]
    cultura: Optional[str] = "colaborativa e inovadora"
    total_personas: Optional[int] = 5

class AvatarGenerationRequest(BaseModel):
    persona_data: Dict[str, Any]

class CascadeScriptRequest(BaseModel):
    empresa_codigo: str
    use_llm: Optional[bool] = True
    force_regenerate: Optional[bool] = False

class ScriptResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output: Optional[str] = None
    cost_info: Optional[Dict[str, Any]] = None

class CostSummaryResponse(BaseModel):
    llm_cost: Dict[str, Any]
    avatar_cost: Dict[str, Any]
    total_cost: float

# Configurações
AUTOMACAO_DIR = Path(__file__).parent / "AUTOMACAO"
SCRIPT_PATHS = {
    # Scripts LLM (novos)
    "biografia_llm": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "01_generate_biografias_llm.py",
    
    # Scripts legados (fallback)
    "biografia": AUTOMACAO_DIR / "01_SETUP_E_CRIACAO" / "05_auto_biografia_generator.py",
    "competencias": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "01_generate_competencias.py",
    "tech_specs": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "02_generate_tech_specs.py",
    "rag": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "03_generate_rag.py",
    "fluxos": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "04_generate_fluxos_analise.py",
    "workflows": AUTOMACAO_DIR / "02_PROCESSAMENTO_PERSONAS" / "05_generate_workflows_n8n.py",
}

def run_python_script(script_path: Path, args: List[str] = None) -> Dict[str, Any]:
    """
    Executa um script Python legado e retorna o resultado
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
        
        logger.info(f"Executando script legado: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos timeout
            cwd=script_path.parent,
            encoding='utf-8'
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
        "message": "VCM Dashboard API Bridge LLM está rodando",
        "version": "2.0.0",
        "llm_available": LLM_AVAILABLE,
        "scripts_available": list(SCRIPT_PATHS.keys()),
        "features": {
            "google_ai": LLM_AVAILABLE,
            "openai_fallback": LLM_AVAILABLE,
            "nano_banana_avatars": LLM_AVAILABLE,
            "cost_tracking": True,
            "quality_validation": LLM_AVAILABLE
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "llm_status": "available" if LLM_AVAILABLE else "unavailable"
    }

@app.get("/status")
async def execution_status():
    """Status de execução dos scripts"""
    # Retorna um mock do status por enquanto
    return {
        "biografia": {"running": False, "last_run": None, "last_result": None},
        "script_1": {"running": False, "last_run": None, "last_result": None},
        "script_2": {"running": False, "last_run": None, "last_result": None},
        "script_3": {"running": False, "last_run": None, "last_result": None},
        "script_4": {"running": False, "last_run": None, "last_result": None},
        "script_5": {"running": False, "last_run": None, "last_result": None},
        "cascade": {"running": False, "last_run": None, "last_result": None}
    }

@app.get("/outputs")
async def list_outputs():
    """Lista os outputs gerados"""
    return {
        "success": True,
        "data": []
    }

@app.post("/generate-biografias", response_model=ScriptResponse)
async def generate_biografias(request: BiografiaGenerationRequest):
    """
    Gera biografias usando LLM (primary) ou script legado (fallback)
    """
    try:
        if request.use_llm and LLM_AVAILABLE:
            # Usar novo sistema LLM
            logger.info(f"🧠 Gerando biografias com LLM para {request.name}")
            
            empresa_data = {
                "nome": request.name,
                "setor": request.industry,
                "nacionalidades": request.nacionalidades,  # Múltiplas nacionalidades
                "cultura": "inovadora e colaborativa"
            }
            
            # Chama função LLM
            result = await generate_biografias_api(empresa_data)
            
            # Calcula custos
            cost_info = {
                "llm_cost": get_cost_summary(),
                "avatar_cost": get_avatar_cost_summary(),
            }
            cost_info["total_cost"] = cost_info["llm_cost"].get("cost", 0) + cost_info["avatar_cost"].get("cost", 0)
            
            return ScriptResponse(
                success=True,
                message=f"Biografias LLM geradas com sucesso para {request.name}",
                data={
                    "empresa": result["empresa"],
                    "biografias": result["biografias"],
                    "metadata": result["metadata"],
                    "total_personas": len(result["biografias"])
                },
                cost_info=cost_info
            )
            
        else:
            # Usar script legado
            logger.info(f"📜 Gerando biografias com script legado para {request.name}")
            
            script_path = SCRIPT_PATHS["biografia"]
            result = run_python_script(script_path, [
                "--empresa-nome", request.name,
                "--setor", request.industry,
                "--nacionalidade", request.nacionalidade
            ])
            
            if result["success"]:
                return ScriptResponse(
                    success=True,
                    message=f"Biografias geradas com sucesso para {request.name}",
                    data={
                        "empresa_nome": request.name,
                        "total_personas": request.total_personas,
                        "method": "legacy_script"
                    },
                    output=result["output"]
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro na geração de biografias: {result['error']}"
                )
                
    except Exception as e:
        logger.error(f"Erro em generate_biografias: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-llm-biografias", response_model=ScriptResponse)
async def generate_llm_biografias(request: LLMBiografiaRequest):
    """
    Endpoint específico para geração LLM de biografias
    """
    if not LLM_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Serviços LLM não estão disponíveis"
        )
    
    try:
        logger.info(f"🧠 Geração LLM para {request.empresa_nome}")
        
        empresa_data = {
            "nome": request.empresa_nome,
            "setor": request.setor,
            "nacionalidades": request.nacionalidades,  # Múltiplas nacionalidades
            "cultura": request.cultura
        }
        
        result = await generate_biografias_api(empresa_data)
        
        # Custos detalhados
        cost_info = {
            "llm_cost": get_cost_summary(),
            "avatar_cost": get_avatar_cost_summary(),
        }
        cost_info["total_cost"] = cost_info["llm_cost"].get("cost", 0) + cost_info["avatar_cost"].get("cost", 0)
        
        return ScriptResponse(
            success=True,
            message=f"Biografias LLM geradas: {len(result['biografias'])} personas",
            data=result,
            cost_info=cost_info
        )
        
    except Exception as e:
        logger.error(f"Erro em generate_llm_biografias: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-avatar", response_model=ScriptResponse)
async def generate_avatar(request: AvatarGenerationRequest):
    """
    Gera avatar para persona específica
    """
    if not LLM_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Serviço de avatar não está disponível"
        )
    
    try:
        logger.info(f"🎨 Gerando avatar para {request.persona_data.get('nome_completo', 'persona')}")
        
        avatar_response = await generate_avatar_for_persona(request.persona_data)
        
        if avatar_response.success:
            return ScriptResponse(
                success=True,
                message="Avatar gerado com sucesso",
                data={
                    "avatar_url": avatar_response.image_url,
                    "generation_time_ms": avatar_response.generation_time_ms
                },
                cost_info={
                    "avatar_cost": avatar_response.cost_usd,
                    "generation_time": avatar_response.generation_time_ms
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na geração de avatar: {avatar_response.error}"
            )
            
    except Exception as e:
        logger.error(f"Erro em generate_avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/costs", response_model=CostSummaryResponse)
async def get_costs():
    """
    Retorna resumo de custos LLM e Avatar
    """
    if not LLM_AVAILABLE:
        return CostSummaryResponse(
            llm_cost={"cost": 0, "requests": 0, "tokens": 0},
            avatar_cost={"cost": 0, "generations": 0},
            total_cost=0.0
        )
    
    llm_cost = get_cost_summary()
    avatar_cost = get_avatar_cost_summary()
    
    total_cost = llm_cost.get("cost", 0) + avatar_cost.get("cost", 0)
    
    return CostSummaryResponse(
        llm_cost=llm_cost,
        avatar_cost=avatar_cost,
        total_cost=total_cost
    )

@app.post("/run-cascade", response_model=ScriptResponse)
async def run_cascade(request: CascadeScriptRequest):
    """
    Executa cascata de scripts (1-6) com suporte LLM
    """
    try:
        if request.use_llm and LLM_AVAILABLE:
            # Implementar cascata LLM no futuro
            logger.info(f"🔄 Cascata LLM ainda não implementada")
            raise HTTPException(
                status_code=501,
                detail="Cascata LLM ainda não implementada. Use cascata legada."
            )
        else:
            # Cascata legada
            results = []
            scripts_order = ["competencias", "tech_specs", "rag", "fluxos", "workflows"]
            
            for script_name in scripts_order:
                logger.info(f"Executando script: {script_name}")
                
                script_path = SCRIPT_PATHS[script_name]
                result = run_python_script(script_path, [request.empresa_codigo])
                
                if not result["success"]:
                    return ScriptResponse(
                        success=False,
                        message=f"Falha no script {script_name}",
                        error=result["error"]
                    )
                
                results.append({
                    "script": script_name,
                    "success": True,
                    "output": result["output"][:200] + "..." if len(result["output"]) > 200 else result["output"]
                })
            
            return ScriptResponse(
                success=True,
                message=f"Cascata executada com sucesso para {request.empresa_codigo}",
                data={
                    "empresa_codigo": request.empresa_codigo,
                    "scripts_executed": len(results),
                    "results": results
                }
            )
            
    except Exception as e:
        logger.error(f"Erro em run_cascade: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/script-status/{script_name}")
async def get_script_status(script_name: str):
    """
    Verifica status de um script específico
    """
    if script_name not in SCRIPT_PATHS:
        raise HTTPException(status_code=404, detail="Script não encontrado")
    
    script_path = SCRIPT_PATHS[script_name]
    
    return {
        "script_name": script_name,
        "path": str(script_path),
        "exists": script_path.exists(),
        "is_llm": script_name.endswith("_llm"),
        "llm_available": LLM_AVAILABLE
    }

@app.get("/llm-providers")
async def get_llm_providers():
    """
    Retorna status dos providers LLM
    """
    if not LLM_AVAILABLE:
        return {
            "available": False,
            "providers": []
        }
    
    # Teste básico dos providers
    try:
        from llm_service import llm_service
        return {
            "available": True,
            "providers": [p.value for p in llm_service.fallback_order],
            "primary": "google_ai",
            "fallback": "openai"
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e),
            "providers": []
        }

# Background task para cleanup
@app.on_event("startup")
async def startup_event():
    """Inicialização da API"""
    logger.info("🚀 VCM Dashboard API Bridge LLM iniciado")
    logger.info(f"📊 LLM disponível: {LLM_AVAILABLE}")
    
    if LLM_AVAILABLE:
        logger.info("✅ Integração Google AI + OpenAI + Nano Banana ativa")
    else:
        logger.info("⚠️ Usando apenas scripts legados")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup na finalização"""
    logger.info("🛑 VCM Dashboard API Bridge LLM finalizado")

# Endpoint de teste
@app.get("/test-llm")
async def test_llm():
    """
    Teste básico dos serviços LLM
    """
    if not LLM_AVAILABLE:
        return {"available": False, "error": "LLM services not loaded"}
    
    try:
        # Teste simples sem gerar conteúdo real
        from llm_service import llm_service
        
        return {
            "available": True,
            "providers": [p.value for p in llm_service.fallback_order],
            "google_ai_key": bool(llm_service.google_ai_key),
            "openai_key": bool(llm_service.openai_key),
            "templates_loaded": len(llm_service.templates)
        }
    except Exception as e:
        return {
            "available": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)