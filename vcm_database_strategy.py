#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏗️ VCM Database Strategy Manager
===============================

Gerencia diferentes estratégias de banco de dados para empresas legadas vs novas.

LifewayUSA (Legado): Banco RAG separado + sincronização complexa
Novas Empresas: Banco unificado + sincronização simples

Autor: VCM System  
Data: 2025-11-10
"""

import os
from enum import Enum
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

class DatabaseStrategy(Enum):
    """Estratégias de banco de dados disponíveis"""
    LEGACY_SEPARATE = "legacy_separate"  # LifewayUSA - banco RAG separado
    UNIFIED_SINGLE = "unified_single"    # Novas empresas - banco único

@dataclass
class DatabaseConfig:
    """Configuração de banco de dados por empresa"""
    strategy: DatabaseStrategy
    vcm_url: str
    vcm_key: str
    company_url: Optional[str] = None
    company_key: Optional[str] = None
    rag_url: Optional[str] = None
    rag_key: Optional[str] = None
    requires_sync: bool = False

class VCMDatabaseManager:
    """Gerenciador de estratégias de banco de dados"""
    
    # Configurações de empresas legadas
    LEGACY_COMPANIES = {
        'LifewayUSA': {
            'company_url_env': 'LIFEWAY_SUPABASE_URL',
            'company_key_env': 'LIFEWAY_SUPABASE_SERVICE_KEY',
            'rag_url_env': 'LIFEWAY_SUPABASE_URL',  # Mesmo banco para RAG
            'rag_key_env': 'LIFEWAY_SUPABASE_SERVICE_KEY',
            'requires_sync': True
        }
    }
    
    def __init__(self):
        """Inicializar gerenciador"""
        self.vcm_url = os.getenv('VCM_SUPABASE_URL')
        self.vcm_key = os.getenv('VCM_SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.vcm_url or not self.vcm_key:
            raise ValueError("VCM database credentials not found in environment")
    
    def get_database_config(self, company_name: str) -> DatabaseConfig:
        """
        Obter configuração de banco para uma empresa específica
        
        Args:
            company_name: Nome da empresa
            
        Returns:
            DatabaseConfig com a estratégia apropriada
        """
        
        # Verificar se é empresa legada
        if company_name in self.LEGACY_COMPANIES:
            return self._get_legacy_config(company_name)
        else:
            return self._get_unified_config(company_name)
    
    def _get_legacy_config(self, company_name: str) -> DatabaseConfig:
        """Configuração para empresas legadas (ex: LifewayUSA)"""
        legacy_config = self.LEGACY_COMPANIES[company_name]
        
        company_url = os.getenv(legacy_config['company_url_env'])
        company_key = os.getenv(legacy_config['company_key_env'])
        rag_url = os.getenv(legacy_config['rag_url_env'])
        rag_key = os.getenv(legacy_config['rag_key_env'])
        
        return DatabaseConfig(
            strategy=DatabaseStrategy.LEGACY_SEPARATE,
            vcm_url=self.vcm_url,
            vcm_key=self.vcm_key,
            company_url=company_url,
            company_key=company_key,
            rag_url=rag_url,
            rag_key=rag_key,
            requires_sync=legacy_config['requires_sync']
        )
    
    def _get_unified_config(self, company_name: str) -> DatabaseConfig:
        """Configuração para novas empresas (banco unificado)"""
        # Para novas empresas, assumimos variáveis de ambiente padrão
        company_env_prefix = company_name.upper().replace(' ', '_')
        
        company_url = os.getenv(f'{company_env_prefix}_SUPABASE_URL')
        company_key = os.getenv(f'{company_env_prefix}_SUPABASE_SERVICE_KEY')
        
        return DatabaseConfig(
            strategy=DatabaseStrategy.UNIFIED_SINGLE,
            vcm_url=self.vcm_url,
            vcm_key=self.vcm_key,
            company_url=company_url,
            company_key=company_key,
            rag_url=company_url,  # Mesmo banco para RAG
            rag_key=company_key,  # Mesma chave para RAG
            requires_sync=False   # Sincronização mais simples
        )
    
    def list_strategies(self) -> Dict[str, str]:
        """Listar estratégias disponíveis por empresa"""
        strategies = {}
        
        # Empresas legadas
        for company in self.LEGACY_COMPANIES.keys():
            strategies[company] = DatabaseStrategy.LEGACY_SEPARATE.value
        
        # Novas empresas seriam detectadas dinamicamente
        # baseado nas variáveis de ambiente disponíveis
        
        return strategies
    
    def validate_config(self, config: DatabaseConfig) -> Tuple[bool, str]:
        """
        Validar configuração de banco de dados
        
        Returns:
            (is_valid, error_message)
        """
        if not config.vcm_url or not config.vcm_key:
            return False, "VCM database credentials missing"
        
        if config.strategy == DatabaseStrategy.LEGACY_SEPARATE:
            if not config.company_url or not config.company_key:
                return False, "Company database credentials missing for legacy strategy"
            if not config.rag_url or not config.rag_key:
                return False, "RAG database credentials missing for legacy strategy"
        
        elif config.strategy == DatabaseStrategy.UNIFIED_SINGLE:
            if not config.company_url or not config.company_key:
                return False, "Unified database credentials missing"
        
        return True, "Configuration valid"

def get_database_strategy(company_name: str) -> DatabaseConfig:
    """
    Função helper para obter estratégia de banco de dados
    
    Args:
        company_name: Nome da empresa
        
    Returns:
        DatabaseConfig apropriada para a empresa
    """
    manager = VCMDatabaseManager()
    return manager.get_database_config(company_name)

# Exemplo de uso
if __name__ == "__main__":
    manager = VCMDatabaseManager()
    
    # Testar LifewayUSA (legado)
    lifeway_config = manager.get_database_config("LifewayUSA")
    print(f"LifewayUSA Strategy: {lifeway_config.strategy.value}")
    print(f"Requires Sync: {lifeway_config.requires_sync}")
    
    # Testar nova empresa hipotética
    new_company_config = manager.get_database_config("NovaEmpresa")
    print(f"NovaEmpresa Strategy: {new_company_config.strategy.value}")
    print(f"Requires Sync: {new_company_config.requires_sync}")
    
    # Listar estratégias
    strategies = manager.list_strategies()
    print(f"Available strategies: {strategies}")