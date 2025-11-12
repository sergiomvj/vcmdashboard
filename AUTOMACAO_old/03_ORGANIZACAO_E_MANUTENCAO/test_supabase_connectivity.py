#!/usr/bin/env python3
"""
🔗 TESTE DE CONECTIVIDADE SUPABASE
==================================

Testa a conectividade com os bancos de dados Supabase configurados:
- VCM Central
- LifewayUSA RAG

Versão: 1.0.0
Data: November 2025
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Adicionar pasta pai ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from supabase import create_client, Client
    print("✅ Biblioteca supabase-py disponível")
except ImportError:
    print("❌ Biblioteca supabase-py não encontrada!")
    print("💡 Instale com: pip install supabase")
    sys.exit(1)

def load_env_variables():
    """Carrega variáveis de ambiente do arquivo .env"""
    # O .env está na raiz do projeto, não na pasta AUTOMACAO
    env_file = Path(__file__).parent.parent.parent / ".env"
    
    if not env_file.exists():
        print(f"❌ Arquivo .env não encontrado em: {env_file}")
        return False
    
    env_vars = {}
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
                os.environ[key] = value
    
    print(f"✅ Carregadas {len(env_vars)} variáveis de ambiente do .env")
    return True

def test_vcm_connection():
    """Testa conexão com VCM Central Supabase"""
    print("\n🎯 TESTANDO VCM CENTRAL SUPABASE")
    print("=" * 50)
    
    url = os.getenv("VCM_SUPABASE_URL")
    anon_key = os.getenv("VCM_SUPABASE_ANON_KEY")
    service_key = os.getenv("VCM_SUPABASE_SERVICE_ROLE_KEY")
    
    if not all([url, anon_key, service_key]):
        print("❌ Credenciais VCM não encontradas no .env")
        return False
    
    print(f"🔗 URL: {url}")
    print(f"🔑 Anon Key: {anon_key[:20]}...")
    print(f"🔑 Service Key: {service_key[:20]}...")
    
    try:
        # Teste com service role para administrativo
        supabase: Client = create_client(url, service_key)
        
        # Teste simples: listar tabelas
        response = supabase.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
        
        if response.data:
            print(f"✅ Conexão VCM bem-sucedida!")
            print(f"📊 Tabelas públicas encontradas: {len(response.data)}")
            for table in response.data[:5]:  # Mostrar primeiras 5
                print(f"   - {table['table_name']}")
            if len(response.data) > 5:
                print(f"   ... e mais {len(response.data) - 5} tabelas")
            return True
        else:
            print("⚠️ Conexão estabelecida, mas nenhuma tabela encontrada")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão VCM: {str(e)}")
        return False

def test_lifeway_connection():
    """Testa conexão com LifewayUSA RAG Database"""
    print("\n🎯 TESTANDO LIFEWAY RAG DATABASE")
    print("=" * 50)
    
    url = os.getenv("LIFEWAY_SUPABASE_URL")
    service_key = os.getenv("LIFEWAY_SUPABASE_SERVICE_KEY")
    
    if not all([url, service_key]):
        print("❌ Credenciais LifewayUSA não encontradas no .env")
        return False
    
    print(f"🔗 URL: {url}")
    print(f"🔑 Service Key: {service_key[:20]}...")
    
    try:
        # Teste com service role
        supabase: Client = create_client(url, service_key)
        
        # Teste simples: listar tabelas
        response = supabase.table("information_schema.tables").select("table_name").eq("table_schema", "public").execute()
        
        if response.data:
            print(f"✅ Conexão LifewayUSA bem-sucedida!")
            print(f"📊 Tabelas públicas encontradas: {len(response.data)}")
            for table in response.data[:5]:  # Mostrar primeiras 5
                print(f"   - {table['table_name']}")
            if len(response.data) > 5:
                print(f"   ... e mais {len(response.data) - 5} tabelas")
            return True
        else:
            print("⚠️ Conexão estabelecida, mas nenhuma tabela encontrada")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão LifewayUSA: {str(e)}")
        return False

def test_basic_operations():
    """Testa operações básicas no VCM Central"""
    print("\n🎯 TESTANDO OPERAÇÕES BÁSICAS VCM")
    print("=" * 50)
    
    url = os.getenv("VCM_SUPABASE_URL")
    service_key = os.getenv("VCM_SUPABASE_SERVICE_ROLE_KEY")
    
    try:
        supabase: Client = create_client(url, service_key)
        
        # Verificar se existe tabela de empresas
        try:
            empresas_response = supabase.table("empresas").select("*").limit(1).execute()
            print("✅ Tabela 'empresas' acessível")
        except Exception as e:
            print(f"⚠️ Tabela 'empresas' não encontrada ou inacessível: {str(e)}")
        
        # Verificar se existe tabela de personas
        try:
            personas_response = supabase.table("personas").select("*").limit(1).execute()
            print("✅ Tabela 'personas' acessível")
        except Exception as e:
            print(f"⚠️ Tabela 'personas' não encontrada ou inacessível: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas operações básicas: {str(e)}")
        return False

def main():
    """Função principal de teste"""
    print("🔗 TESTE DE CONECTIVIDADE SUPABASE")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # 1. Carregar variáveis de ambiente
    if not load_env_variables():
        return
    
    # 2. Testar VCM Central
    vcm_ok = test_vcm_connection()
    
    # 3. Testar LifewayUSA
    lifeway_ok = test_lifeway_connection()
    
    # 4. Testar operações básicas
    operations_ok = test_basic_operations()
    
    # 5. Resumo final
    print("\n🎯 RESUMO DOS TESTES")
    print("=" * 50)
    print(f"📊 VCM Central: {'✅ CONECTADO' if vcm_ok else '❌ FALHOU'}")
    print(f"📊 LifewayUSA: {'✅ CONECTADO' if lifeway_ok else '❌ FALHOU'}")
    print(f"📊 Operações: {'✅ FUNCIONANDO' if operations_ok else '❌ FALHOU'}")
    
    total_tests = sum([vcm_ok, lifeway_ok, operations_ok])
    print(f"\n🎉 Resultado: {total_tests}/3 testes passaram")
    
    if total_tests == 3:
        print("✅ Sistema completamente conectado ao Supabase!")
    elif total_tests >= 1:
        print("⚠️ Conectividade parcial - alguns problemas detectados")
    else:
        print("❌ Sistema desconectado - verificar configurações")

if __name__ == "__main__":
    main()