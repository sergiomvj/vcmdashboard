#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Script de Sincronização LifewayUSA Personas
==============================================

Este script sincroniza as personas da LifewayUSA do banco RAG para o banco VCM Central.
É uma solução pontual para empresas criadas antes do sistema de sincronização automática.

Autor: VCM System
Data: 2025-11-10
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
import uuid
from vcm_database_strategy import get_database_strategy, DatabaseStrategy

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync_lifeway_personas.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class LifewaySyncManager:
    def __init__(self):
        """Inicializar o gerenciador de sincronização"""
        self.base_path = Path(__file__).parent
        self.load_environment()
        self.setup_database_strategy()
        self.setup_clients()
        
    def load_environment(self):
        """Carregar variáveis de ambiente"""
        env_path = self.base_path / '.env'
        if not env_path.exists():
            raise FileNotFoundError(f"Arquivo .env não encontrado: {env_path}")
        
        load_dotenv(env_path)
        logger.info("✅ Variáveis de ambiente carregadas")
        
    def setup_database_strategy(self):
        """Configurar estratégia de banco de dados para LifewayUSA"""
        self.db_config = get_database_strategy("LifewayUSA")
        
        if self.db_config.strategy != DatabaseStrategy.LEGACY_SEPARATE:
            raise ValueError("LifewayUSA deve usar estratégia LEGACY_SEPARATE")
        
        logger.info(f"✅ Estratégia de banco: {self.db_config.strategy.value}")
        logger.info(f"📋 Requer sincronização: {self.db_config.requires_sync}")
        
    def setup_clients(self):
        """Configurar clientes Supabase usando a estratégia detectada"""
        
        if not all([self.db_config.vcm_url, self.db_config.vcm_key, 
                   self.db_config.rag_url, self.db_config.rag_key]):
            missing = []
            if not self.db_config.vcm_url: missing.append('VCM_SUPABASE_URL')
            if not self.db_config.vcm_key: missing.append('VCM_SUPABASE_SERVICE_ROLE_KEY')
            if not self.db_config.rag_url: missing.append('LIFEWAY_SUPABASE_URL')
            if not self.db_config.rag_key: missing.append('LIFEWAY_SUPABASE_SERVICE_KEY')
            raise ValueError(f"Variáveis de ambiente faltando: {missing}")
        
        # Criar clientes usando a configuração da estratégia
        self.vcm_client: Client = create_client(self.db_config.vcm_url, self.db_config.vcm_key)
        self.lifeway_client: Client = create_client(self.db_config.rag_url, self.db_config.rag_key)
        
        logger.info("✅ Clientes Supabase configurados via estratégia")
        
    def cleanup_existing_lifeway_personas(self, empresa_id):
        """Limpar personas LifewayUSA existentes no VCM Central antes da nova sincronização"""
        try:
            # Buscar personas existentes da LifewayUSA
            response = self.vcm_client.table('personas').select('id, persona_code').eq('empresa_id', empresa_id).execute()
            
            if response.data:
                logger.info(f"🧹 Encontradas {len(response.data)} personas existentes para limpeza")
                
                # Deletar cada persona
                for persona in response.data:
                    delete_response = self.vcm_client.table('personas').delete().eq('id', persona['id']).execute()
                    if delete_response.data:
                        logger.info(f"🗑️ Persona {persona['persona_code']} removida")
                    else:
                        logger.warning(f"⚠️ Falha ao remover persona {persona['persona_code']}")
                
                logger.info(f"✅ Limpeza concluída: {len(response.data)} personas removidas")
            else:
                logger.info("ℹ️ Nenhuma persona existente encontrada para limpeza")
                
        except Exception as e:
            logger.error(f"❌ Erro durante limpeza: {e}")
            
    def get_lifeway_company_id(self):
        """Obter ID da empresa LifewayUSA no banco VCM Central"""
        try:
            response = self.vcm_client.table('empresas').select('id').eq('nome', 'LifewayUSA').execute()
            
            if not response.data:
                logger.error("❌ Empresa LifewayUSA não encontrada no banco VCM Central")
                return None
                
            company_id = response.data[0]['id']
            logger.info(f"✅ ID da empresa LifewayUSA: {company_id}")
            return company_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar empresa LifewayUSA: {e}")
            return None
    
    def get_lifeway_personas(self):
        """Obter personas da LifewayUSA do banco RAG"""
        try:
            response = self.lifeway_client.table('personas').select('*').execute()
            
            if not response.data:
                logger.warning("⚠️ Nenhuma persona encontrada no banco RAG da LifewayUSA")
                return []
                
            logger.info(f"✅ Encontradas {len(response.data)} personas no banco RAG da LifewayUSA")
            return response.data
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar personas do banco RAG: {e}")
            return []
    
    def check_existing_personas(self, empresa_id):
        """Verificar personas existentes no VCM Central para evitar duplicatas"""
        try:
            response = self.vcm_client.table('personas').select('persona_code').eq('empresa_id', empresa_id).execute()
            existing_codes = {persona['persona_code'] for persona in response.data}
            logger.info(f"✅ {len(existing_codes)} personas já existem no VCM Central")
            return existing_codes
            
        except Exception as e:
            logger.error(f"❌ Erro ao verificar personas existentes: {e}")
            return set()
    
    def transform_persona_data(self, rag_persona, empresa_id):
        """Transformar dados da persona do formato RAG para VCM Central"""
        try:
            # Mapear campos do RAG para VCM Central
            # IMPORTANTE: banco LifewayUSA RAG já usa os nomes corretos dos campos
            vcm_persona = {
                'id': str(uuid.uuid4()),
                'persona_code': rag_persona.get('persona_code', f"LIFEWAY_{rag_persona.get('id', 'UNKNOWN')}"),
                'full_name': rag_persona.get('full_name', 'Nome não definido'),
                'role': rag_persona.get('role', 'Cargo não definido'),
                'specialty': rag_persona.get('specialty', ''),
                'department': rag_persona.get('department', ''),
                'email': rag_persona.get('email', ''),
                'whatsapp': rag_persona.get('whatsapp', ''),
                'empresa_id': empresa_id,
                'biografia_completa': rag_persona.get('biografia_completa', ''),
                'personalidade': rag_persona.get('personalidade', {}),
                'experiencia_anos': rag_persona.get('experiencia_anos', 0),
                'ia_config': rag_persona.get('ia_config', {}),
                'temperatura_ia': rag_persona.get('temperatura_ia', 0.7),
                'max_tokens': rag_persona.get('max_tokens', 2000),
                'system_prompt': rag_persona.get('system_prompt', ''),
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'last_sync': datetime.now().isoformat()
            }
            
            # Log para debug
            logger.info(f"🔄 Mapeando: {rag_persona.get('full_name', 'SEM_NOME')} -> {vcm_persona['full_name']}")
            
            return vcm_persona
            
        except Exception as e:
            logger.error(f"❌ Erro ao transformar dados da persona {rag_persona.get('id')}: {e}")
            return None
    
    def sync_personas(self, empresa_id, rag_personas, existing_codes):
        """Sincronizar personas do RAG para VCM Central"""
        synced_count = 0
        skipped_count = 0
        error_count = 0
        
        for rag_persona in rag_personas:
            try:
                persona_code = rag_persona.get('codigo_persona', f"LIFEWAY_{rag_persona.get('id', 'UNKNOWN')}")
                
                # Pular se já existe
                if persona_code in existing_codes:
                    logger.info(f"⏭️ Persona {persona_code} já existe, pulando...")
                    skipped_count += 1
                    continue
                
                # Transformar dados
                vcm_persona = self.transform_persona_data(rag_persona, empresa_id)
                if not vcm_persona:
                    error_count += 1
                    continue
                
                # Inserir no VCM Central
                response = self.vcm_client.table('personas').insert(vcm_persona).execute()
                
                if response.data:
                    logger.info(f"✅ Persona {persona_code} sincronizada com sucesso")
                    synced_count += 1
                else:
                    logger.error(f"❌ Falha ao sincronizar persona {persona_code}")
                    error_count += 1
                    
            except Exception as e:
                logger.error(f"❌ Erro ao sincronizar persona {rag_persona.get('id', 'UNKNOWN')}: {e}")
                error_count += 1
        
        return synced_count, skipped_count, error_count
    
    def update_empresa_count(self, empresa_id, total_personas):
        """Atualizar contador de personas na empresa"""
        try:
            response = self.vcm_client.table('empresas').update({
                'total_personas': total_personas,
                'updated_at': datetime.now().isoformat()
            }).eq('id', empresa_id).execute()
            
            if response.data:
                logger.info(f"✅ Contador de personas atualizado: {total_personas}")
            else:
                logger.warning("⚠️ Falha ao atualizar contador de personas")
                
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar contador de personas: {e}")
    
    def run_sync(self):
        """Executar sincronização completa"""
        logger.info("🔄 Iniciando sincronização de personas LifewayUSA...")
        
        try:
            # 1. Obter ID da empresa LifewayUSA
            empresa_id = self.get_lifeway_company_id()
            if not empresa_id:
                return False
            
            # 2. Limpar personas existentes incorretas
            logger.info("🧹 Limpando personas existentes...")
            self.cleanup_existing_lifeway_personas(empresa_id)
            
            # 3. Obter personas do banco RAG
            rag_personas = self.get_lifeway_personas()
            if not rag_personas:
                logger.warning("⚠️ Nenhuma persona encontrada para sincronizar")
                return True
            
            # 4. Verificar personas existentes (deve estar vazio após limpeza)
            existing_codes = self.check_existing_personas(empresa_id)
            
            # 5. Sincronizar personas
            synced, skipped, errors = self.sync_personas(empresa_id, rag_personas, existing_codes)
            
            # 6. Atualizar contador na empresa
            total_personas = synced + len(existing_codes)
            self.update_empresa_count(empresa_id, total_personas)
            
            # 7. Relatório final
            logger.info("=" * 50)
            logger.info("📊 RELATÓRIO DE SINCRONIZAÇÃO")
            logger.info("=" * 50)
            logger.info(f"✅ Personas sincronizadas: {synced}")
            logger.info(f"⏭️ Personas já existentes: {skipped}")
            logger.info(f"❌ Erros: {errors}")
            logger.info(f"📊 Total de personas na empresa: {total_personas}")
            logger.info("=" * 50)
            
            if errors > 0:
                logger.warning(f"⚠️ Sincronização completada com {errors} erros")
            else:
                logger.info("🎉 Sincronização completada com sucesso!")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro durante a sincronização: {e}")
            return False

def main():
    """Função principal"""
    print("🔄 Script de Sincronização LifewayUSA Personas")
    print("=" * 50)
    
    try:
        sync_manager = LifewaySyncManager()
        success = sync_manager.run_sync()
        
        if success:
            print("\n✅ Sincronização concluída!")
            print("📋 Verifique o arquivo 'sync_lifeway_personas.log' para detalhes")
        else:
            print("\n❌ Sincronização falhou!")
            print("📋 Verifique o arquivo 'sync_lifeway_personas.log' para detalhes")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Sincronização cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()