#!/usr/bin/env python3
"""
Script para testar conectividade com a API VCM
"""

import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    # Teste 1: Health Check
    print("🏥 Testando Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health Check OK\n")
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}\n")
        return
    
    # Teste 2: Status de Execução
    print("📊 Testando Status de Execução...")
    try:
        response = requests.get(f"{base_url}/execution-status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Status OK\n")
    except Exception as e:
        print(f"❌ Erro no Status: {e}\n")
    
    # Teste 3: Lista de Outputs
    print("📋 Testando Lista de Outputs...")
    try:
        response = requests.get(f"{base_url}/outputs")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Outputs OK\n")
    except Exception as e:
        print(f"❌ Erro nos Outputs: {e}\n")

if __name__ == "__main__":
    test_api()