#!/usr/bin/env python3
"""
🎪 VCM DASHBOARD FULL-STACK SERVER
==================================

Servidor único que serve tanto o frontend React (build) quanto a API FastAPI.
Elimina a necessidade de dois containers separados.

Funcionalidades:
- Serve arquivos estáticos do Next.js build
- API FastAPI para automação VCM
- Servidor único na porta 8000
- Deploy simplificado com apenas 1 container

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
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="VCM Dashboard Full-Stack",
    description="Servidor único com frontend e API",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# 🏥 API ENDPOINTS
# ========================================

@app.get("/api/health")
async def health_check():
    """Health check da API"""
    return {
        "status": "healthy",
        "message": "VCM Full-Stack API is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/empresas")
async def list_empresas():
    """Lista empresas virtuais disponíveis"""
    return {
        "success": True,
        "data": [
            {"id": "lifeway", "nome": "LifewayUSA", "status": "active"},
            {"id": "carntrack", "nome": "CarnTrack", "status": "planned"}
        ]
    }

@app.get("/api/personas/{empresa_id}")
async def list_personas(empresa_id: str):
    """Lista personas de uma empresa"""
    return {
        "success": True,
        "data": {
            "empresa_id": empresa_id,
            "total": 20,
            "personas": [
                {"id": 1, "nome": "João Silva", "cargo": "CEO", "categoria": "executivos"},
                {"id": 2, "nome": "Maria Santos", "cargo": "CTO", "categoria": "executivos"}
            ]
        }
    }

class AutomationRequest(BaseModel):
    empresa_id: str
    script_type: str
    force_update: Optional[bool] = False

@app.post("/api/automation/run")
async def run_automation(request: AutomationRequest):
    """Executa scripts de automação"""
    return {
        "success": True,
        "message": f"Executando {request.script_type} para {request.empresa_id}",
        "task_id": f"task-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    }

# ========================================
# 🌐 FRONTEND STATIC FILES
# ========================================

# Diretório do build do Next.js
BUILD_DIR = Path(__file__).parent / "out"
if not BUILD_DIR.exists():
    BUILD_DIR = Path(__file__).parent / ".next" / "static"
    if not BUILD_DIR.exists():
        BUILD_DIR = Path(__file__).parent / "dist"

# Servir arquivos estáticos
if BUILD_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(BUILD_DIR)), name="static")
    logger.info(f"✅ Servindo arquivos estáticos: {BUILD_DIR}")
else:
    logger.warning("⚠️ Diretório de build não encontrado. Execute 'npm run build' primeiro.")

@app.get("/")
async def serve_index():
    """Serve o index.html do frontend"""
    index_path = BUILD_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    else:
        return {"message": "VCM Dashboard API", "build_required": "Execute 'npm run build' para gerar frontend"}

@app.get("/{path:path}")
async def serve_frontend(path: str):
    """Serve arquivos do frontend ou fallback para index.html"""
    file_path = BUILD_DIR / path
    
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    else:
        # Fallback para SPA routing
        index_path = BUILD_DIR / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
        else:
            raise HTTPException(status_code=404, detail="Page not found")

# ========================================
# 🚀 SERVIDOR
# ========================================

if __name__ == "__main__":
    import uvicorn
    
    print("🎪 Iniciando VCM Dashboard Full-Stack...")
    print("📁 Build directory:", BUILD_DIR)
    print("🔗 Servidor disponível em: http://localhost:8000")
    print("📚 API docs em: http://localhost:8000/docs")
    
    # Usar porta dinâmica para Easypanel
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "vcm_fullstack_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )