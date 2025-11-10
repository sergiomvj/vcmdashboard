"""
VCM Avatar Generator - Nano Banana Integration
Serviço para geração de avatares realistas usando Nano Banana API
Author: VCM Team
Date: November 2024
"""

import os
import json
import logging
import asyncio
import aiohttp
import base64
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import time
import hashlib

# Setup logging
logger = logging.getLogger(__name__)

@dataclass
class AvatarRequest:
    description: str
    gender: str
    ethnicity: str
    age_range: str
    style: str = "professional"
    size: str = "512x512"

@dataclass
class AvatarResponse:
    image_url: Optional[str]
    image_base64: Optional[str]
    success: bool
    cost_usd: float
    generation_time_ms: int
    error: Optional[str] = None

class AvatarStyle(Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    CORPORATE = "corporate"
    CREATIVE = "creative"

class NanoBananaClient:
    """
    Cliente para integração com Nano Banana API
    Geração de avatares realistas para personas do VCM
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.load_environment()
        self.setup_client()
        
    def load_environment(self):
        """Carrega configurações do ambiente"""
        # Tenta encontrar .env na pasta raiz do projeto
        env_paths = [
            self.base_path / '.env',  # Pasta AUTOMACAO
            self.base_path.parent / '.env',  # Pasta raiz vcm_vite_react
            Path.cwd() / '.env'  # Diretório atual
        ]
        
        env_loaded = False
        for env_file in env_paths:
            if env_file.exists():
                logger.info(f"Carregando .env de: {env_file}")
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key] = value
                env_loaded = True
                break
        
        if not env_loaded:
            logger.warning("Nenhum arquivo .env encontrado")
        
        # Por enquanto usamos uma API key placeholder
        # Será configurada quando tivermos acesso ao Nano Banana
        self.api_key = os.getenv('NANO_BANANA_API_KEY', 'placeholder-key')
        self.base_url = "https://api.nanobanana.com/v1"  # URL placeholder
        
    def setup_client(self):
        """Setup do cliente"""
        self.session = None
        self.cost_tracker = AvatarCostTracker()
        
    async def generate_avatar(self, request: AvatarRequest) -> AvatarResponse:
        """
        Gera avatar usando Nano Banana API
        """
        start_time = time.time()
        
        try:
            # Por enquanto, vamos simular a resposta
            # Quando tivermos acesso real ao Nano Banana, implementaremos a API real
            if self.api_key == 'placeholder-key':
                return await self._simulate_avatar_generation(request, start_time)
            else:
                return await self._call_nano_banana_api(request, start_time)
                
        except Exception as e:
            logger.error(f"Erro na geração de avatar: {str(e)}")
            return AvatarResponse(
                image_url=None,
                image_base64=None,
                success=False,
                cost_usd=0.0,
                generation_time_ms=int((time.time() - start_time) * 1000),
                error=str(e)
            )
    
    async def _simulate_avatar_generation(self, request: AvatarRequest, start_time: float) -> AvatarResponse:
        """
        Simula geração de avatar para desenvolvimento
        Retorna placeholder até termos acesso real ao Nano Banana
        """
        # Simula tempo de processamento
        await asyncio.sleep(1.5)
        
        # Gera URL placeholder baseada nos parâmetros
        description_hash = hashlib.md5(request.description.encode()).hexdigest()[:8]
        placeholder_url = f"https://api.dicebear.com/7.x/avataaars/svg?seed={description_hash}&backgroundColor=transparent"
        
        # Simula custo (Nano Banana deve ser barato para avatares)
        simulated_cost = 0.05  # $0.05 per avatar
        
        generation_time = int((time.time() - start_time) * 1000)
        
        response = AvatarResponse(
            image_url=placeholder_url,
            image_base64=None,  # Placeholder não gera base64
            success=True,
            cost_usd=simulated_cost,
            generation_time_ms=generation_time,
            error=None
        )
        
        self.cost_tracker.track_generation(response)
        
        logger.info(f"Avatar simulado gerado - Custo: ${simulated_cost:.3f}, Tempo: {generation_time}ms")
        
        return response
    
    async def _call_nano_banana_api(self, request: AvatarRequest, start_time: float) -> AvatarResponse:
        """
        Chamada real para Nano Banana API
        Implementar quando tivermos acesso à API
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Monta payload para Nano Banana
        payload = {
            "prompt": self._build_nano_banana_prompt(request),
            "style": request.style,
            "size": request.size,
            "format": "url",  # ou "base64"
            "quality": "high"
        }
        
        url = f"{self.base_url}/generate/avatar"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Nano Banana API error {response.status}: {error_text}")
                
                result = await response.json()
                generation_time = int((time.time() - start_time) * 1000)
                
                avatar_response = AvatarResponse(
                    image_url=result.get('image_url'),
                    image_base64=result.get('image_base64'),
                    success=True,
                    cost_usd=result.get('cost', 0.05),  # Default cost
                    generation_time_ms=generation_time,
                    error=None
                )
                
                self.cost_tracker.track_generation(avatar_response)
                
                return avatar_response
    
    def _build_nano_banana_prompt(self, request: AvatarRequest) -> str:
        """
        Constrói prompt otimizado para Nano Banana
        """
        prompt_parts = []
        
        # Descrição base
        prompt_parts.append(request.description)
        
        # Características demográficas
        if request.gender:
            prompt_parts.append(f"gender: {request.gender}")
        
        if request.ethnicity:
            prompt_parts.append(f"ethnicity: {request.ethnicity}")
            
        if request.age_range:
            prompt_parts.append(f"age: {request.age_range}")
        
        # Estilo profissional
        style_prompts = {
            "professional": "professional business attire, office background, confident pose",
            "casual": "casual clothing, relaxed pose, friendly expression",
            "corporate": "formal business suit, executive style, professional lighting",
            "creative": "creative outfit, artistic background, expressive pose"
        }
        
        if request.style in style_prompts:
            prompt_parts.append(style_prompts[request.style])
        
        # Qualidade geral
        prompt_parts.append("high quality, realistic, professional photography")
        
        return ", ".join(prompt_parts)
    
    async def generate_avatar_for_persona(self, persona_data: Dict[str, Any]) -> AvatarResponse:
        """
        Gera avatar baseado nos dados da persona
        """
        # Extrai informações da biografia
        nome = persona_data.get('nome_completo', '')
        idade = persona_data.get('idade', 35)
        genero = self._extract_gender_from_name(nome)
        nacionalidade = persona_data.get('background_cultural', 'brasileira')
        cargo = persona_data.get('cargo', 'funcionário')
        
        # Monta descrição para o avatar
        description = persona_data.get('avatar_description', '')
        if not description:
            description = self._generate_description_from_persona(persona_data)
        
        # Determina etnicity baseado na nacionalidade
        ethnicity = self._map_nationality_to_ethnicity(nacionalidade)
        
        # Determina faixa etária
        age_range = self._get_age_range(idade)
        
        # Determina estilo baseado no cargo
        style = self._get_style_for_cargo(cargo)
        
        request = AvatarRequest(
            description=description,
            gender=genero,
            ethnicity=ethnicity,
            age_range=age_range,
            style=style
        )
        
        return await self.generate_avatar(request)
    
    def _extract_gender_from_name(self, nome: str) -> str:
        """Extrai gênero do nome (implementação básica)"""
        # Implementação simplificada - em produção usaríamos uma biblioteca mais robusta
        nome_lower = nome.lower()
        
        # Terminações femininas comuns em português
        femininas = ['a', 'ana', 'ina', 'ela', 'isa', 'ria']
        for fem in femininas:
            if nome_lower.endswith(fem):
                return "female"
        
        return "male"  # Default
    
    def _map_nationality_to_ethnicity(self, nacionalidade: str) -> str:
        """Mapeia nacionalidade para ethnicity"""
        mapping = {
            'brasileira': 'latin',
            'latina': 'latin',
            'americana': 'caucasian',
            'europeia': 'caucasian',
            'asiatica': 'asian',
            'africana': 'african',
            'arabe': 'middle_eastern'
        }
        
        return mapping.get(nacionalidade.lower(), 'latin')
    
    def _get_age_range(self, idade: int) -> str:
        """Converte idade em faixa etária"""
        if idade < 25:
            return "young_adult"
        elif idade < 40:
            return "adult"
        elif idade < 55:
            return "middle_aged"
        else:
            return "senior"
    
    def _get_style_for_cargo(self, cargo: str) -> str:
        """Determina estilo baseado no cargo"""
        cargo_lower = cargo.lower()
        
        if any(term in cargo_lower for term in ['ceo', 'diretor', 'gerente', 'executivo']):
            return "corporate"
        elif any(term in cargo_lower for term in ['designer', 'criativo', 'marketing']):
            return "creative"
        elif any(term in cargo_lower for term in ['desenvolvedor', 'analista', 'técnico']):
            return "professional"
        else:
            return "professional"
    
    def _generate_description_from_persona(self, persona_data: Dict[str, Any]) -> str:
        """Gera descrição de avatar baseada na persona"""
        nome = persona_data.get('nome_completo', '')
        cargo = persona_data.get('cargo', '')
        personalidade = persona_data.get('personalidade', '')
        
        # Extrai características físicas da personalidade se disponível
        description_parts = []
        
        # Características profissionais
        if 'ceo' in cargo.lower() or 'diretor' in cargo.lower():
            description_parts.append("confident executive appearance")
        elif 'desenvolvedor' in cargo.lower():
            description_parts.append("tech professional appearance")
        
        # Características de personalidade
        if 'extrovertido' in personalidade.lower():
            description_parts.append("friendly and approachable expression")
        elif 'analítico' in personalidade.lower():
            description_parts.append("thoughtful and focused expression")
        
        # Base description
        if not description_parts:
            description_parts.append("professional business appearance")
        
        return ", ".join(description_parts)

class AvatarCostTracker:
    """Rastreamento de custos para geração de avatares"""
    
    def __init__(self):
        self.daily_costs = {}
        self.generation_log = []
        
    def track_generation(self, response: AvatarResponse):
        """Registra geração de avatar"""
        today = time.strftime('%Y-%m-%d')
        
        if today not in self.daily_costs:
            self.daily_costs[today] = {'cost': 0.0, 'generations': 0}
        
        self.daily_costs[today]['cost'] += response.cost_usd
        self.daily_costs[today]['generations'] += 1
        
        self.generation_log.append({
            'timestamp': time.time(),
            'cost': response.cost_usd,
            'generation_time': response.generation_time_ms,
            'success': response.success
        })
        
        logger.info(f"Avatar gerado - Custo: ${response.cost_usd:.3f}, "
                   f"Tempo: {response.generation_time_ms}ms")
    
    def get_daily_summary(self, date: str = None) -> Dict[str, Any]:
        """Resumo diário de gerações"""
        if not date:
            date = time.strftime('%Y-%m-%d')
        
        return self.daily_costs.get(date, {'cost': 0.0, 'generations': 0})

# Instância global do cliente
avatar_client = NanoBananaClient()

# Funções de conveniência
async def generate_avatar_for_persona(persona_data: Dict[str, Any]) -> AvatarResponse:
    """Gera avatar para persona específica"""
    return await avatar_client.generate_avatar_for_persona(persona_data)

async def generate_custom_avatar(description: str, gender: str, ethnicity: str) -> AvatarResponse:
    """Gera avatar customizado"""
    request = AvatarRequest(
        description=description,
        gender=gender,
        ethnicity=ethnicity,
        age_range="adult"
    )
    return await avatar_client.generate_avatar(request)

def get_avatar_cost_summary() -> Dict[str, Any]:
    """Resumo de custos de avatar"""
    return avatar_client.cost_tracker.get_daily_summary()

# Teste do serviço
if __name__ == "__main__":
    async def test_avatar_service():
        """Teste básico do serviço de avatar"""
        
        # Dados de persona de exemplo
        persona_test = {
            'nome_completo': 'Maria Silva Santos',
            'idade': 32,
            'cargo': 'Desenvolvedora Senior',
            'background_cultural': 'brasileira',
            'personalidade': 'Extrovertida e analítica',
            'avatar_description': 'Professional software developer, confident smile, modern office background'
        }
        
        print("🎨 Testando Avatar Generator...")
        
        response = await generate_avatar_for_persona(persona_test)
        
        if response.success:
            print(f"✅ Avatar gerado com sucesso!")
            print(f"🖼️ URL: {response.image_url}")
            print(f"💰 Custo: ${response.cost_usd:.3f}")
            print(f"⚡ Tempo: {response.generation_time_ms}ms")
        else:
            print(f"❌ Falha na geração: {response.error}")
        
        # Resumo de custos
        summary = get_avatar_cost_summary()
        print(f"\n📊 Resumo do dia: ${summary['cost']:.3f} - {summary['generations']} avatares")
    
    # Executa teste
    asyncio.run(test_avatar_service())