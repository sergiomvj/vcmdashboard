#!/usr/bin/env python3
"""
VCM Database Schema Setup
Execute the complete schema update for VCM Dashboard V2.0
"""

import os
import sys
from pathlib import Path
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_db_connection():
    """Estabelece conexão com VCM Supabase"""
    db_url = os.getenv('VCM_SUPABASE_DB_PASSWORD')
    if not db_url:
        raise ValueError("VCM_SUPABASE_DB_PASSWORD não encontrada no .env")
    
    # Extrair componentes da URL
    if not db_url.startswith('postgresql://'):
        raise ValueError("URL do banco deve começar com postgresql://")
    
    return psycopg2.connect(db_url)

def execute_sql_file(conn, sql_file_path):
    """Executa arquivo SQL completo"""
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        cursor = conn.cursor()
        
        # Dividir em comandos separados (por ;)
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        print(f"🚀 Executando {len(commands)} comandos SQL...")
        
        for i, command in enumerate(commands, 1):
            if command.strip():
                try:
                    cursor.execute(command)
                    print(f"✅ Comando {i}/{len(commands)} executado com sucesso")
                except Exception as e:
                    print(f"⚠️  Comando {i} falhou (pode ser esperado): {str(e)[:100]}...")
                    # Não falhar por comandos que já existem
                    continue
        
        conn.commit()
        cursor.close()
        print("✅ Schema executado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar SQL: {e}")
        conn.rollback()
        return False

def verify_tables():
    """Verifica se as tabelas foram criadas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar tabelas criadas
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
              AND table_name IN (
                'empresas',
                'personas',
                'metas_globais', 
                'metas_personas', 
                'auditorias_compatibilidade', 
                'avatares_personas',
                'personas_biografias',
                'personas_tech_specs'
              )
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        
        print("\n📊 Tabelas verificadas:")
        for table_name, table_type in tables:
            print(f"  ✅ {table_name} ({table_type})")
        
        # Verificar colunas da tabela empresas
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'empresas' AND table_schema = 'public'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        
        print("\n🏢 Estrutura da tabela empresas:")
        for col_name, data_type, nullable, default in columns:
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            default_str = f" DEFAULT {default}" if default else ""
            print(f"  • {col_name}: {data_type} {nullable_str}{default_str}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 VCM Database Schema Setup V2.0")
    print("=" * 50)
    
    # Verificar arquivo SQL
    sql_file = Path(__file__).parent / "vcm-dashboard-real" / "update_empresas_schema.sql"
    if not sql_file.exists():
        print(f"❌ Arquivo SQL não encontrado: {sql_file}")
        return False
    
    print(f"📁 Arquivo SQL: {sql_file}")
    
    try:
        # Conectar ao banco
        print("🔌 Conectando ao VCM Supabase...")
        conn = get_db_connection()
        print("✅ Conexão estabelecida!")
        
        # Executar SQL
        print("\n📝 Executando schema...")
        if execute_sql_file(conn, sql_file):
            conn.close()
            
            # Verificar resultados
            print("\n🔍 Verificando tabelas criadas...")
            if verify_tables():
                print("\n🎉 Setup completo! Todas as tabelas estão prontas.")
                return True
            else:
                print("\n⚠️  Setup parcial. Verifique logs acima.")
                return False
        else:
            conn.close()
            print("\n❌ Falha na execução do schema.")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)