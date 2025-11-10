#!/usr/bin/env python3
"""
🚀 Inicializador completo do VCM Dashboard
==========================================

Inicia tanto o frontend (Next.js) quanto o backend (FastAPI) automaticamente.
Use este script para iniciar todo o sistema de uma vez.
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    # Verificar Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        print(f"✅ Node.js: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js não encontrado. Instale Node.js primeiro.")
        return False
    
    # Verificar Python
    try:
        result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Python não encontrado.")
        return False
    
    return True

def start_backend():
    """Inicia o servidor backend FastAPI"""
    print("🔗 Iniciando servidor backend (FastAPI)...")
    backend_process = subprocess.Popen(
        [sys.executable, 'api_bridge_real.py'],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguardar backend inicializar
    print("⏳ Aguardando backend inicializar...")
    time.sleep(3)
    
    return backend_process

def start_frontend():
    """Inicia o servidor frontend Next.js"""
    print("🌐 Iniciando servidor frontend (Next.js)...")
    frontend_dir = Path(__file__).parent / "vcm-dashboard-real"
    
    if not frontend_dir.exists():
        print(f"❌ Diretório frontend não encontrado: {frontend_dir}")
        return None
    
    frontend_process = subprocess.Popen(
        ['npm', 'run', 'dev'],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("⏳ Aguardando frontend inicializar...")
    time.sleep(5)
    
    return frontend_process

def main():
    """Função principal"""
    print("🚀 Iniciando VCM Dashboard completo...")
    print("=" * 50)
    
    if not check_dependencies():
        return 1
    
    processes = []
    
    try:
        # Iniciar backend
        backend_process = start_backend()
        if backend_process:
            processes.append(backend_process)
            print("✅ Backend iniciado na porta 8000")
        
        # Iniciar frontend
        frontend_process = start_frontend()
        if frontend_process:
            processes.append(frontend_process)
            print("✅ Frontend iniciado na porta 3001")
        
        print("\n" + "=" * 50)
        print("🎉 VCM Dashboard iniciado com sucesso!")
        print("🌐 Frontend: http://localhost:3001")
        print("🔗 Backend API: http://localhost:8000")
        print("📚 Documentação API: http://localhost:8000/docs")
        print("\n💡 Pressione Ctrl+C para parar todos os serviços")
        print("=" * 50)
        
        # Aguardar interrupção
        while True:
            time.sleep(1)
            
            # Verificar se algum processo morreu
            for process in processes:
                if process.poll() is not None:
                    print(f"⚠️ Um processo parou inesperadamente")
                    break
            
    except KeyboardInterrupt:
        print("\n🛑 Parando todos os serviços...")
        
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        print("✅ Todos os serviços foram parados")
        return 0
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())