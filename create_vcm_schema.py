#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Execução do Schema VCM V2.0
==============================

Executa o SQL completo para criar todas as novas tabelas no Supabase VCM.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Executar criação das tabelas no Supabase"""
    
    # Carregar variáveis de ambiente
    base_path = Path(__file__).parent
    env_path = base_path / '.env'
    
    if not env_path.exists():
        logger.error(f"❌ Arquivo .env não encontrado: {env_path}")
        return False
        
    load_dotenv(env_path)
    
    # Configurar cliente Supabase
    vcm_url = os.getenv('VCM_SUPABASE_URL')
    vcm_key = os.getenv('VCM_SUPABASE_SERVICE_ROLE_KEY')
    
    if not vcm_url or not vcm_key:
        logger.error("❌ Credenciais VCM Supabase não encontradas no .env")
        return False
    
    logger.info("🔗 Conectando ao Supabase VCM Central...")
    supabase_client = create_client(vcm_url, vcm_key)
    
    # Ler arquivo SQL
    sql_file = base_path / "vcm-dashboard-real" / "update_empresas_schema.sql"
    
    if not sql_file.exists():
        logger.error(f"❌ Arquivo SQL não encontrado: {sql_file}")
        return False
    
    logger.info(f"📂 Lendo arquivo SQL: {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Dividir em comandos individuais (por ponto e vírgula + quebra de linha)
    sql_commands = [cmd.strip() for cmd in sql_content.split(';\n') if cmd.strip() and not cmd.strip().startswith('--')]
    
    logger.info(f"📋 Encontrados {len(sql_commands)} comandos SQL para executar")
    
    success_count = 0
    error_count = 0
    
    for i, command in enumerate(sql_commands, 1):
        if not command or command.isspace():
            continue
            
        try:
            logger.info(f"⚙️ Executando comando {i}/{len(sql_commands)}...")
            
            # Executar via RPC ou diretamente
            result = supabase_client.rpc('exec_sql', {'sql': command}).execute()
            
            logger.info(f"✅ Comando {i} executado com sucesso")
            success_count += 1
            
        except Exception as e:
            logger.warning(f"⚠️ Erro no comando {i}: {str(e)}")
            logger.info(f"📋 Comando que falhou: {command[:100]}...")
            error_count += 1
            # Continuar com próximo comando
    
    # Relatório final
    logger.info("=" * 50)
    logger.info("📊 RELATÓRIO DE EXECUÇÃO SQL")
    logger.info("=" * 50)
    logger.info(f"✅ Comandos executados com sucesso: {success_count}")
    logger.info(f"⚠️ Comandos com erro: {error_count}")
    logger.info(f"📊 Total de comandos: {len(sql_commands)}")
    
    if error_count == 0:
        logger.info("🎉 Todas as tabelas foram criadas com sucesso!")
    else:
        logger.warning(f"⚠️ {error_count} comandos falharam - verifique os logs acima")
    
    return error_count == 0

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Schema VCM V2.0 criado com sucesso!")
        else:
            print("\n❌ Houve problemas na criação do schema")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        sys.exit(1)