#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Debug LifewayUSA Personas Structure
=====================================

Script para investigar a estrutura real dos dados das personas no banco RAG da LifewayUSA
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client

# Carregar ambiente
base_path = Path(__file__).parent
env_path = base_path / '.env'
load_dotenv(env_path)

# Conectar ao banco LifewayUSA RAG
lifeway_url = os.getenv('LIFEWAY_SUPABASE_URL')
lifeway_key = os.getenv('LIFEWAY_SUPABASE_SERVICE_KEY')

if not lifeway_url or not lifeway_key:
    print("❌ Credenciais LifewayUSA não encontradas no .env")
    exit(1)

lifeway_client = create_client(lifeway_url, lifeway_key)

print("🔍 Investigando estrutura das personas LifewayUSA...")
print("=" * 60)

try:
    # Buscar uma persona para análise
    response = lifeway_client.table('personas').select('*').limit(1).execute()
    
    if response.data:
        persona_sample = response.data[0]
        print("📋 ESTRUTURA DE UMA PERSONA (primeira encontrada):")
        print("=" * 60)
        
        for key, value in persona_sample.items():
            value_type = type(value).__name__
            value_preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            print(f"🔹 {key:20} | {value_type:10} | {value_preview}")
        
        print("\n" + "=" * 60)
        print("📄 JSON COMPLETO DA PERSONA:")
        print("=" * 60)
        print(json.dumps(persona_sample, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 60)
        print("🎯 CAMPOS RELEVANTES PARA SINCRONIZAÇÃO:")
        print("=" * 60)
        
        # Identificar campos de nome
        name_fields = [k for k in persona_sample.keys() if any(term in k.lower() for term in ['name', 'nome', 'full'])]
        print(f"📝 Campos de nome: {name_fields}")
        
        # Identificar campos de cargo/role
        role_fields = [k for k in persona_sample.keys() if any(term in k.lower() for term in ['role', 'cargo', 'position', 'posicao'])]
        print(f"💼 Campos de cargo: {role_fields}")
        
        # Verificar campos obrigatórios
        required_fields = ['id', 'empresa_id']
        missing_required = [f for f in required_fields if f not in persona_sample]
        print(f"⚠️ Campos obrigatórios faltando: {missing_required}")
        
    else:
        print("❌ Nenhuma persona encontrada no banco LifewayUSA")
        
    # Contar total de personas
    count_response = lifeway_client.table('personas').select('id').execute()
    total_personas = len(count_response.data) if count_response.data else 0
    print(f"\n📊 Total de personas no banco LifewayUSA: {total_personas}")
    
except Exception as e:
    print(f"❌ Erro ao investigar estrutura: {e}")

print("\n🔍 Investigação concluída!")