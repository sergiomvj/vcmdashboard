#!/usr/bin/env python3
"""
TESTE DE CONECTIVIDADE - VCM System
Testa conexões com Supabase e valida configuração
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests
import json

# Carregar variáveis de ambiente
load_dotenv()

def test_env_config():
    """Testa se todas as variáveis de ambiente estão configuradas"""
    print("🔧 TESTANDO CONFIGURAÇÃO DO AMBIENTE")
    print("=" * 50)
    
    required_vars = [
        'VCM_SUPABASE_URL',
        'VCM_SUPABASE_ANON_KEY',
        'VCM_SUPABASE_SERVICE_ROLE_KEY',
        'LIFEWAY_SUPABASE_URL',
        'LIFEWAY_SUPABASE_SERVICE_KEY',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mostrar apenas os primeiros caracteres para segurança
            display_value = f"{value[:10]}..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: NÃO CONFIGURADA")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️ Variáveis faltando: {', '.join(missing_vars)}")
        return False
    
    print("\n✅ Todas as variáveis de ambiente estão configuradas!")
    return True

def test_supabase_connection(name, url, service_key):
    """Testa conexão com uma instância do Supabase"""
    print(f"\n🔗 TESTANDO CONEXÃO: {name}")
    print(f"URL: {url}")
    
    try:
        # Testar endpoint de health check
        headers = {
            'apikey': service_key,
            'Authorization': f'Bearer {service_key}',
            'Content-Type': 'application/json'
        }
        
        # Fazer uma requisição simples para testar conectividade
        response = requests.get(
            f"{url}/rest/v1/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ {name}: Conexão OK (Status: {response.status_code})")
            return True
        else:
            print(f"⚠️ {name}: Conexão com problemas (Status: {response.status_code})")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {name}: Erro de conexão - {str(e)}")
        return False

def test_personas_config():
    """Testa se o arquivo personas_config.json existe e está válido"""
    print("\n📋 TESTANDO PERSONAS_CONFIG.JSON")
    print("=" * 50)
    
    personas_path = Path("AUTOMACAO/01_SETUP_E_CRIACAO/test_biografias_output/personas_config.json")
    
    if not personas_path.exists():
        print(f"❌ Arquivo não encontrado: {personas_path}")
        return False
    
    try:
        with open(personas_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar estrutura básica
        if 'ceo' in data:
            ceo = data['ceo']
            print(f"✅ CEO: {ceo.get('nome_completo', 'N/A')} ({ceo.get('pais_origem', 'N/A')})")
        
        if 'executivos' in data:
            exec_count = len(data['executivos'])
            print(f"✅ Executivos: {exec_count} personas")
        
        if 'especialistas' in data:
            esp_count = len(data['especialistas'])
            print(f"✅ Especialistas: {esp_count} personas")
        
        if 'assistentes' in data:
            ass_count = len(data['assistentes'])
            print(f"✅ Assistentes: {ass_count} personas")
        
        total_personas = 1  # CEO
        total_personas += len(data.get('executivos', {}))
        total_personas += len(data.get('especialistas', {}))
        total_personas += len(data.get('assistentes', {}))
        
        print(f"\n📊 Total de personas: {total_personas}")
        print("✅ Arquivo personas_config.json válido!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 INICIANDO TESTES DO VCM SYSTEM")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Configuração do ambiente
    results.append(test_env_config())
    
    # Teste 2: Conexões Supabase
    if results[0]:  # Só testa se env está OK
        vcm_url = os.getenv('VCM_SUPABASE_URL')
        vcm_key = os.getenv('VCM_SUPABASE_SERVICE_ROLE_KEY')
        results.append(test_supabase_connection("VCM Central", vcm_url, vcm_key))
        
        lifeway_url = os.getenv('LIFEWAY_SUPABASE_URL')
        lifeway_key = os.getenv('LIFEWAY_SUPABASE_SERVICE_KEY')
        results.append(test_supabase_connection("LifewayUSA RAG", lifeway_url, lifeway_key))
    
    # Teste 3: Personas Config
    results.append(test_personas_config())
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Testes aprovados: {passed}/{total}")
    
    if passed == total:
        print("🎉 SISTEMA VCM PRONTO PARA USO!")
        print("\n🚀 Próximos passos:")
        print("1. Rodar cascade de processamento (Scripts 1-5)")
        print("2. Testar dashboard React")
        print("3. Verificar sincronização com bases de dados")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("Verifique as configurações antes de prosseguir.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)