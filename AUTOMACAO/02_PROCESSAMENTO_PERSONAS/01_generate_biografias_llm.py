"""
VCM Script 1 - LLM Biografia Generator 
Gerador de biografias usando Google AI (primary) + OpenAI (fallback)
Author: VCM Team
Date: November 2024
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import time

# Import dos serviços LLM e Avatar
try:
    from llm_service import generate_biografia, LLMResponse, ContentType
    from avatar_service import generate_avatar_for_persona, AvatarResponse
except ImportError as e:
    print(f"Erro ao importar serviços LLM: {e}")
    # Fallback para desenvolvimento
    generate_biografia = None
    generate_avatar_for_persona = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('biografia_llm.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BiografiaLLMGenerator:
    """
    Gerador de biografias usando LLM
    Integra Google AI + OpenAI + Nano Banana para resultados realistas
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.output_path = self.base_path / "01_SETUP_E_CRIACAO" / "test_biografias_output"
        self.output_path.mkdir(exist_ok=True)
        
        # Configurações do sistema
        self.personas_config = self.load_personas_config()
        self.generation_stats = {
            'total_generated': 0,
            'successful': 0,
            'failed': 0,
            'total_cost': 0.0,
            'avatar_cost': 0.0,
            'start_time': time.time()
        }
        
    def load_personas_config(self) -> Dict[str, Any]:
        """Carrega configuração de personas"""
        config_file = self.output_path / "personas_config.json"
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Cria configuração padrão se não existir
            return self.create_default_config()
    
    def create_default_config(self) -> Dict[str, Any]:
        """Cria configuração padrão de personas"""
        config = {
            "empresa": {
                "nome": "TechStart Brasil",
                "setor": "tecnologia",
                "nacionalidade": "brasileira",
                "cultura": "inovadora e colaborativa"
            },
            "personas": [
                {
                    "id": 1,
                    "cargo": "CEO",
                    "nivel": "executivo",
                    "categoria": "executivos",
                    "is_ceo": True,
                    "genero": "feminino"
                },
                {
                    "id": 2,
                    "cargo": "CTO",
                    "nivel": "executivo", 
                    "categoria": "executivos",
                    "is_ceo": False,
                    "genero": "masculino"
                },
                {
                    "id": 3,
                    "cargo": "Desenvolvedor Senior",
                    "nivel": "senior",
                    "categoria": "especialistas",
                    "is_ceo": False,
                    "genero": "feminino"
                },
                {
                    "id": 4,
                    "cargo": "Designer UX",
                    "nivel": "pleno",
                    "categoria": "especialistas", 
                    "is_ceo": False,
                    "genero": "masculino"
                },
                {
                    "id": 5,
                    "cargo": "Analista de Marketing",
                    "nivel": "junior",
                    "categoria": "assistentes",
                    "is_ceo": False,
                    "genero": "feminino"
                }
            ]
        }
        
        # Salva configuração padrão
        config_file = self.output_path / "personas_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        return config
    
    def _format_nacionalidades_info(self, nacionalidades: List[Dict[str, Any]]) -> str:
        """
        Formata lista de nacionalidades com percentuais em texto para LLM
        """
        if not nacionalidades:
            return "brasileira (100%)"
        
        if len(nacionalidades) == 1:
            nac = nacionalidades[0]
            return f"{nac['tipo']} (100%)"
        
        # Múltiplas nacionalidades
        formatted_parts = []
        for nac in nacionalidades:
            formatted_parts.append(f"{nac['tipo']} ({nac['percentual']}%)")
        
        return "Composição diversificada: " + ", ".join(formatted_parts)
    
    async def generate_all_biografias(self, empresa_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Gera todas as biografias usando LLM
        """
        logger.info("🚀 Iniciando geração de biografias com LLM")
        
        if empresa_data:
            self.personas_config["empresa"].update(empresa_data)
        
        empresa = self.personas_config["empresa"]
        personas = self.personas_config["personas"]
        
        results = {
            "empresa": empresa,
            "biografias": [],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "2.0.0-llm",
                "total_personas": len(personas),
                "generation_method": "llm_integrated"
            }
        }
        
        # Gera biografias sequencialmente para melhor controle
        for i, persona in enumerate(personas, 1):
            logger.info(f"📝 Gerando biografia {i}/{len(personas)} - {persona['cargo']}")
            
            biografia = await self.generate_single_biografia(empresa, persona)
            
            if biografia:
                results["biografias"].append(biografia)
                self.generation_stats['successful'] += 1
                logger.info(f"✅ Biografia gerada: {biografia['nome_completo']}")
            else:
                self.generation_stats['failed'] += 1
                logger.error(f"❌ Falha na geração: {persona['cargo']}")
            
            self.generation_stats['total_generated'] += 1
            
            # Pausa pequena entre gerações para evitar rate limiting
            await asyncio.sleep(1)
        
        # Salva resultados
        await self.save_results(results)
        
        # Log de estatísticas
        self.log_generation_stats()
        
        return results
    
    async def generate_single_biografia(self, empresa: Dict[str, Any], persona: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Gera biografia individual usando LLM
        """
        try:
            # Processa múltiplas nacionalidades em formato textual
            nacionalidades_info = self._format_nacionalidades_info(empresa.get('nacionalidades', [{'tipo': 'brasileira', 'percentual': 100}]))
            
            # Monta contexto para o LLM
            context = {
                'empresa_nome': empresa['nome'],
                'empresa_setor': empresa['setor'],
                'cargo': persona['cargo'],
                'nivel': persona['nivel'],
                'nacionalidades_info': nacionalidades_info,
                'genero': persona['genero'],
                'is_ceo': persona['is_ceo']
            }
            
            # Gera biografia usando LLM
            llm_response = await generate_biografia(context)
            
            if not llm_response.success:
                logger.error(f"LLM falhou para {persona['cargo']}: {llm_response.error}")
                return None
            
            # Parse da resposta JSON
            try:
                biografia_data = json.loads(llm_response.content)
            except json.JSONDecodeError as e:
                logger.error(f"Erro no parse JSON para {persona['cargo']}: {e}")
                # Tenta extrair JSON do texto
                biografia_data = self.extract_json_from_text(llm_response.content)
                if not biografia_data:
                    return None
            
            # Valida dados obrigatórios
            if not self.validate_biografia_data(biografia_data):
                logger.error(f"Dados inválidos para {persona['cargo']}")
                return None
            
            # Adiciona metadados da geração
            biografia_data.update({
                'id': persona['id'],
                'cargo': persona['cargo'],
                'nivel': persona['nivel'],
                'categoria': persona['categoria'],
                'is_ceo': persona['is_ceo'],
                'metadata': {
                    'llm_provider': llm_response.provider.value,
                    'generation_cost': llm_response.cost_usd,
                    'quality_score': llm_response.quality_score,
                    'tokens_used': llm_response.tokens_used,
                    'generation_time_ms': llm_response.latency_ms,
                    'generated_at': datetime.now().isoformat()
                }
            })
            
            # Gera avatar (em background, não bloqueia)
            avatar_task = asyncio.create_task(self.generate_avatar_for_biografia(biografia_data))
            
            # Atualiza estatísticas de custo
            self.generation_stats['total_cost'] += llm_response.cost_usd
            
            # Aguarda avatar (com timeout)
            try:
                avatar_response = await asyncio.wait_for(avatar_task, timeout=30.0)
                if avatar_response and avatar_response.success:
                    biografia_data['avatar_url'] = avatar_response.image_url
                    biografia_data['metadata']['avatar_cost'] = avatar_response.cost_usd
                    biografia_data['metadata']['avatar_generation_time'] = avatar_response.generation_time_ms
                    self.generation_stats['avatar_cost'] += avatar_response.cost_usd
                else:
                    biografia_data['avatar_url'] = None
                    biografia_data['metadata']['avatar_error'] = avatar_response.error if avatar_response else "Timeout"
            except asyncio.TimeoutError:
                biografia_data['avatar_url'] = None
                biografia_data['metadata']['avatar_error'] = "Timeout na geração"
            
            return biografia_data
            
        except Exception as e:
            logger.error(f"Erro na geração de biografia para {persona['cargo']}: {str(e)}")
            return None
    
    async def generate_avatar_for_biografia(self, biografia_data: Dict[str, Any]) -> Optional[AvatarResponse]:
        """Gera avatar para a biografia"""
        try:
            return await generate_avatar_for_persona(biografia_data)
        except Exception as e:
            logger.error(f"Erro na geração de avatar: {str(e)}")
            return None
    
    def extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extrai JSON de texto que pode conter outros conteúdos"""
        try:
            # Procura por { e } para extrair JSON
            start = text.find('{')
            end = text.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
                
        except Exception as e:
            logger.error(f"Erro ao extrair JSON: {e}")
            
        return None
    
    def validate_biografia_data(self, data: Dict[str, Any]) -> bool:
        """Valida se os dados da biografia estão completos"""
        required_fields = [
            'nome_completo',
            'idade', 
            'formacao_academica',
            'experiencia_profissional'
        ]
        
        for field in required_fields:
            if field not in data or not data[field]:
                logger.warning(f"Campo obrigatório ausente: {field}")
                return False
        
        # Validações específicas
        if not isinstance(data['idade'], int) or data['idade'] < 18 or data['idade'] > 70:
            logger.warning(f"Idade inválida: {data['idade']}")
            return False
        
        return True
    
    async def save_results(self, results: Dict[str, Any]):
        """Salva resultados da geração"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salva arquivo principal
        main_file = self.output_path / f"biografias_llm_{timestamp}.json"
        with open(main_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Salva também como arquivo latest
        latest_file = self.output_path / "biografias_latest.json"
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Atualiza personas_config.json com informações atualizadas
        self.personas_config.update({
            'last_generation': timestamp,
            'generation_stats': self.generation_stats
        })
        
        config_file = self.output_path / "personas_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.personas_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Resultados salvos em {main_file}")
    
    def log_generation_stats(self):
        """Log das estatísticas de geração"""
        total_time = time.time() - self.generation_stats['start_time']
        
        logger.info("📊 ESTATÍSTICAS DE GERAÇÃO")
        logger.info("=" * 50)
        logger.info(f"Total de personas: {self.generation_stats['total_generated']}")
        logger.info(f"Sucessos: {self.generation_stats['successful']}")
        logger.info(f"Falhas: {self.generation_stats['failed']}")
        logger.info(f"Taxa de sucesso: {(self.generation_stats['successful']/self.generation_stats['total_generated']*100):.1f}%")
        logger.info(f"Custo LLM: ${self.generation_stats['total_cost']:.4f}")
        logger.info(f"Custo Avatar: ${self.generation_stats['avatar_cost']:.4f}")
        logger.info(f"Custo Total: ${(self.generation_stats['total_cost'] + self.generation_stats['avatar_cost']):.4f}")
        logger.info(f"Tempo total: {total_time:.1f}s")
        logger.info(f"Tempo médio por persona: {(total_time/self.generation_stats['total_generated']):.1f}s")

# Função principal para execução standalone
async def main():
    """Execução principal do script"""
    print("🧬 VCM - Gerador de Biografias LLM v2.0")
    print("=" * 50)
    
    generator = BiografiaLLMGenerator()
    
    # Dados de empresa (opcional - pode vir do formulário)
    empresa_data = {
        "nome": "InnovaTech Solutions",
        "setor": "tecnologia",
        "nacionalidade": "brasileira",
        "cultura": "inovadora, colaborativa e centrada no cliente"
    }
    
    try:
        results = await generator.generate_all_biografias(empresa_data)
        
        print(f"\n✅ Geração concluída!")
        print(f"📝 {len(results['biografias'])} biografias geradas")
        print(f"💰 Custo total: ${generator.generation_stats['total_cost'] + generator.generation_stats['avatar_cost']:.4f}")
        print(f"📁 Arquivos salvos em: {generator.output_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro na execução principal: {str(e)}")
        print(f"❌ Erro: {str(e)}")
        return False

# Função para integração com API
async def generate_biografias_api(empresa_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função para integração com API do dashboard
    """
    generator = BiografiaLLMGenerator()
    return await generator.generate_all_biografias(empresa_data)

# Execução standalone
if __name__ == "__main__":
    asyncio.run(main())