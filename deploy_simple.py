#!/usr/bin/env python3
"""
🚀 DEPLOY SIMPLIFICADO VCM DASHBOARD
===================================

Script para testar as 3 abordagens de deployment simplificado:
1. Full-Stack Server (Python serve frontend + API)
2. Next.js API Routes (tudo em Next.js)
3. Container Híbrido (build completo)

Escolha a melhor opção para seu caso de uso.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_fullstack_server():
    """Opção 1: Servidor Python que serve frontend + API"""
    print("🎪 OPÇÃO 1: Full-Stack Server")
    print("=" * 50)
    
    # Verificar se existe build do frontend
    build_dir = Path("out")
    if not build_dir.exists():
        print("📦 Buildando frontend...")
        subprocess.run(["npm", "run", "build"], check=True)
        subprocess.run(["npm", "run", "export"], check=False)  # Pode falhar em algumas versões
    
    print("🚀 Iniciando servidor full-stack...")
    try:
        subprocess.run([sys.executable, "vcm_fullstack_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado.")

def run_nextjs_only():
    """Opção 2: Apenas Next.js com API routes"""
    print("🔗 OPÇÃO 2: Next.js com API Routes")
    print("=" * 50)
    
    # Atualizar configuração para usar API routes locais
    env_content = """
# Configuração para usar API routes do Next.js
NEXT_PUBLIC_API_URL=
VCM_ENVIRONMENT=development
"""
    
    with open(".env.local", "w") as f:
        f.write(env_content)
    
    print("🚀 Iniciando servidor Next.js...")
    try:
        subprocess.run(["npm", "run", "dev"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor encerrado.")

def build_container():
    """Opção 3: Build container híbrido"""
    print("🐳 OPÇÃO 3: Container Híbrido")
    print("=" * 50)
    
    print("📦 Buildando container full-stack...")
    build_cmd = [
        "docker", "build", 
        "-f", "Dockerfile.fullstack",
        "-t", "vcm-dashboard:latest",
        "."
    ]
    
    subprocess.run(build_cmd, check=True)
    
    print("🚀 Executando container...")
    run_cmd = [
        "docker", "run",
        "-p", "8000:8000",
        "--env-file", ".env",
        "vcm-dashboard:latest"
    ]
    
    try:
        subprocess.run(run_cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Container encerrado.")

def main():
    print("🎯 VCM DASHBOARD - DEPLOY SIMPLIFICADO")
    print("=" * 50)
    print()
    print("Escolha uma opção:")
    print("1. 🎪 Full-Stack Server (Python + Frontend)")
    print("2. 🔗 Next.js Only (API Routes)")
    print("3. 🐳 Container Híbrido (Docker)")
    print("0. ❌ Sair")
    print()
    
    while True:
        choice = input("Digite sua escolha (0-3): ").strip()
        
        if choice == "0":
            print("👋 Saindo...")
            break
        elif choice == "1":
            run_fullstack_server()
            break
        elif choice == "2":
            run_nextjs_only()
            break
        elif choice == "3":
            build_container()
            break
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Deploy cancelado.")
    except Exception as e:
        print(f"❌ Erro: {e}")