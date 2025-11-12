#!/usr/bin/env python3
"""
🎯 FORMULÁRIO AVANÇADO DE SETUP DE EMPRESA
==========================================

Formulário interativo completo com perguntas demográficas para
geração automática de personas com biografias detalhadas.

Versão: 2.0.0
Autor: Sergio Castro
Data: November 2025
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Importar o gerador de biografias
sys.path.append(str(Path(__file__).parent))
from auto_biografia_generator import AutoBiografiaGenerator

class AdvancedCompanySetup:
    def __init__(self):
        """Inicializar setup avançado de empresa"""
        
        self.bio_generator = AutoBiografiaGenerator()
        
        # Opções de nacionalidades
        self.nacionalidades_opcoes = {
            "1": ("europeus", "🇪🇺 Europeus (França, Alemanha, Itália, Espanha, Reino Unido, etc.)"),
            "2": ("latinos", "🌎 Latinos (Brasil, México, Argentina, Colômbia, Chile, etc.)"),
            "3": ("asiaticos", "🌏 Asiáticos (Japão, Coreia, China, Singapura, Taiwan, etc.)"),
            "4": ("oriente_medio", "🕌 Oriente Médio (Emirados Árabes, Israel, Turquia, Líbano, etc.)"),
            "5": ("balcas", "⛰️ Balcãs (Sérvia, Croácia, Bósnia, Montenegro, Eslovênia, etc.)"),
            "6": ("nordicos", "❄️ Nórdicos (Suécia, Noruega, Dinamarca, Finlândia, Islândia)")
        }
        
        # Opções de indústrias
        self.industrias_opcoes = {
            "1": ("tecnologia", "💻 Tecnologia e Software"),
            "2": ("financas", "💰 Finanças e Investimentos"),
            "3": ("saude", "🏥 Saúde e Biotecnologia"),
            "4": ("educacao", "🎓 Educação e Treinamento"),
            "5": ("ecommerce", "🛒 E-commerce e Retail"),
            "6": ("consultoria", "📊 Consultoria e Serviços"),
            "7": ("marketing", "📢 Marketing e Publicidade"),
            "8": ("alimentacao", "🍽️ Alimentação e Nutrição"),
            "9": ("sustentabilidade", "🌱 Sustentabilidade e Energia"),
            "10": ("entretenimento", "🎬 Entretenimento e Mídia")
        }
        
        # Idiomas extras disponíveis
        self.idiomas_extras = [
            "alemão", "italiano", "japonês", "coreano", "mandarim", 
            "árabe", "russo", "hindi", "holandês", "sueco"
        ]
    
    def show_welcome(self):
        """Exibir tela de boas-vindas"""
        
        print("\n" + "="*80)
        print("🚀 VIRTUAL COMPANY GENERATOR - SETUP AVANÇADO v2.0.0")
        print("="*80)
        print("📋 Criação Completa de Empresa Virtual com Biografias Automáticas")
        print("✨ Agora com geração automática de personas detalhadas!")
        print("="*80)
        
    def collect_basic_info(self) -> Dict:
        """Coletar informações básicas da empresa"""
        
        print("\n📋 INFORMAÇÕES BÁSICAS DA EMPRESA")
        print("-"*50)
        
        company_info = {}
        
        # Nome da empresa
        while True:
            nome = input("🏢 Nome da empresa: ").strip()
            if nome:
                company_info["name"] = nome
                break
            print("❌ Nome da empresa é obrigatório!")
        
        # Domínio
        while True:
            dominio = input("🌐 Domínio da empresa (ex: minhaempresa.com): ").strip()
            if dominio:
                company_info["domain"] = dominio
                break
            print("❌ Domínio é obrigatório!")
        
        # Indústria
        print("\n🏭 Escolha a indústria da empresa:")
        for key, (value, desc) in self.industrias_opcoes.items():
            print(f"   {key}. {desc}")
        
        while True:
            escolha = input("\nIndústria (1-10): ").strip()
            if escolha in self.industrias_opcoes:
                industry_code, industry_desc = self.industrias_opcoes[escolha]
                company_info["industry"] = industry_code
                company_info["industry_desc"] = industry_desc
                break
            print("❌ Opção inválida!")
        
        # Descrição
        descricao = input("\n📝 Descrição breve da empresa: ").strip()
        company_info["description"] = descricao or f"Empresa inovadora no setor de {industry_code}"
        
        # Público-alvo
        publico = input("👥 Público-alvo principal: ").strip()
        company_info["target_audience"] = publico or "Empresas e profissionais do mercado"
        
        return company_info
    
    def collect_demographic_info(self) -> Dict:
        """Coletar informações demográficas das personas"""
        
        print("\n👥 CONFIGURAÇÃO DEMOGRÁFICA DAS PERSONAS")
        print("-"*50)
        
        demo_info = {}
        
        # Nacionalidade
        print("\n🌍 Escolha a nacionalidade predominante das personas:")
        for key, (value, desc) in self.nacionalidades_opcoes.items():
            print(f"   {key}. {desc}")
        
        while True:
            escolha = input("\nNacionalidade (1-6): ").strip()
            if escolha in self.nacionalidades_opcoes:
                nac_code, nac_desc = self.nacionalidades_opcoes[escolha]
                demo_info["nacionalidade"] = nac_code
                demo_info["nacionalidade_desc"] = nac_desc
                break
            print("❌ Opção inválida!")
        
        # CEO - Gênero
        print("\n👔 CEO da empresa:")
        while True:
            ceo_genero = input("O CEO será homem ou mulher? (H/M): ").strip().upper()
            if ceo_genero in ["H", "M"]:
                demo_info["ceo_genero"] = "masculino" if ceo_genero == "H" else "feminino"
                break
            print("❌ Digite H para homem ou M para mulher!")
        
        # Executivos
        print("\n👥 EXECUTIVOS (além do CEO):")
        demo_info["executivos_homens"] = self.get_number_input("Quantos executivos homens? ", 0, 5, default=2)
        demo_info["executivos_mulheres"] = self.get_number_input("Quantas executivas mulheres? ", 0, 5, default=2)
        
        # Assistentes
        total_executives = 1 + demo_info["executivos_homens"] + demo_info["executivos_mulheres"]
        print(f"\n👨‍💼 ASSISTENTES EXECUTIVOS (sugerido: {total_executives} para cobrir todos os executivos):")
        demo_info["assistentes_homens"] = self.get_number_input("Quantos assistentes homens? ", 0, 8, default=2)
        demo_info["assistentes_mulheres"] = self.get_number_input("Quantas assistentes mulheres? ", 0, 8, default=total_executives-2)
        
        # Especialistas
        print(f"\n🎯 ESPECIALISTAS (6 áreas fixas: HR, YouTube, Mídias Sociais, Marketing, Financeiro, Tecnologia):")
        demo_info["especialistas_homens"] = self.get_number_input("Quantos especialistas homens? ", 0, 6, default=3)
        demo_info["especialistas_mulheres"] = self.get_number_input("Quantas especialistas mulheres? ", 0, 6, default=3)
        
        # Validação de especialistas
        total_espec = demo_info["especialistas_homens"] + demo_info["especialistas_mulheres"]
        if total_espec != 6:
            print(f"⚠️ Aviso: Total de especialistas ({total_espec}) diferente de 6. Ajustando automaticamente...")
            if total_espec > 6:
                demo_info["especialistas_mulheres"] = max(0, 6 - demo_info["especialistas_homens"])
            else:
                demo_info["especialistas_mulheres"] = 6 - demo_info["especialistas_homens"]
        
        return demo_info
    
    def collect_language_info(self, nacionalidade: str) -> List[str]:
        """Coletar informações sobre idiomas"""
        
        print(f"\n🌐 IDIOMAS DAS PERSONAS")
        print("-"*50)
        
        # Idiomas padrão
        idiomas_padrao = ["inglês", "espanhol", "português", "francês"]
        idiomas_regionais = self.bio_generator.idiomas_regionais.get(nacionalidade, [])
        
        print("📋 Idiomas padrão incluídos:")
        for idioma in idiomas_padrao:
            print(f"   ✅ {idioma.capitalize()}")
        
        if idiomas_regionais:
            print(f"\n🌍 Idiomas regionais para {nacionalidade}:")
            for idioma in idiomas_regionais:
                if idioma not in idiomas_padrao:
                    print(f"   ✅ {idioma.capitalize()}")
        
        # Idiomas extras
        print(f"\n➕ Idiomas extras disponíveis:")
        for i, idioma in enumerate(self.idiomas_extras, 1):
            print(f"   {i}. {idioma.capitalize()}")
        
        extras_escolhidos = []
        while True:
            escolha = input("\nEscolha idiomas extras (números separados por vírgula, ou Enter para pular): ").strip()
            
            if not escolha:
                break
                
            try:
                numeros = [int(x.strip()) for x in escolha.split(",")]
                for num in numeros:
                    if 1 <= num <= len(self.idiomas_extras):
                        idioma = self.idiomas_extras[num-1]
                        if idioma not in extras_escolhidos:
                            extras_escolhidos.append(idioma)
                    else:
                        print(f"❌ Número inválido: {num}")
                        continue
                break
                        
            except ValueError:
                print("❌ Digite números válidos separados por vírgula!")
        
        if extras_escolhidos:
            print(f"\n✅ Idiomas extras selecionados: {', '.join(extras_escolhidos)}")
        
        return extras_escolhidos
    
    def get_number_input(self, prompt: str, min_val: int, max_val: int, default: int = None) -> int:
        """Helper para input de números com validação"""
        
        while True:
            if default is not None:
                user_input = input(f"{prompt}(padrão: {default}): ").strip()
                if not user_input:
                    return default
            else:
                user_input = input(prompt).strip()
            
            try:
                number = int(user_input)
                if min_val <= number <= max_val:
                    return number
                else:
                    print(f"❌ Digite um número entre {min_val} e {max_val}!")
            except ValueError:
                print("❌ Digite um número válido!")
    
    def show_configuration_summary(self, config: Dict):
        """Exibir resumo da configuração"""
        
        print("\n📋 RESUMO DA CONFIGURAÇÃO")
        print("="*60)
        
        print(f"🏢 Empresa: {config['name']}")
        print(f"🌐 Domínio: {config['domain']}")
        print(f"🏭 Indústria: {config['industry_desc']}")
        print(f"📝 Descrição: {config['description']}")
        print(f"👥 Público-alvo: {config['target_audience']}")
        
        print(f"\n🌍 Demografia:")
        print(f"   Nacionalidade: {config['nacionalidade_desc']}")
        print(f"   CEO: {config['ceo_genero'].capitalize()}")
        
        print(f"\n👥 Distribuição de Personas:")
        print(f"   📊 CEO: 1 pessoa")
        print(f"   👔 Executivos: {config['executivos_homens']} homens + {config['executivos_mulheres']} mulheres = {config['executivos_homens'] + config['executivos_mulheres']}")
        print(f"   👨‍💼 Assistentes: {config['assistentes_homens']} homens + {config['assistentes_mulheres']} mulheres = {config['assistentes_homens'] + config['assistentes_mulheres']}")
        print(f"   🎯 Especialistas: {config['especialistas_homens']} homens + {config['especialistas_mulheres']} mulheres = {config['especialistas_homens'] + config['especialistas_mulheres']}")
        
        total_personas = 1 + config['executivos_homens'] + config['executivos_mulheres'] + config['assistentes_homens'] + config['assistentes_mulheres'] + config['especialistas_homens'] + config['especialistas_mulheres']
        print(f"\n🎯 TOTAL: {total_personas} personas")
        
        if config.get('idiomas_extras'):
            print(f"\n🌐 Idiomas extras: {', '.join(config['idiomas_extras'])}")
        
        print("="*60)
    
    def run_setup(self) -> Dict:
        """Executar setup completo"""
        
        self.show_welcome()
        
        # Coletar informações
        company_info = self.collect_basic_info()
        demo_info = self.collect_demographic_info()
        idiomas_extras = self.collect_language_info(demo_info["nacionalidade"])
        
        # Combinar configurações
        full_config = {**company_info, **demo_info}
        full_config["idiomas_extras"] = idiomas_extras
        full_config["created_at"] = datetime.now().isoformat()
        
        # Mostrar resumo
        self.show_configuration_summary(full_config)
        
        # Confirmar
        while True:
            confirmacao = input("\n✅ Confirma esta configuração? (S/N): ").strip().upper()
            if confirmacao in ["S", "N"]:
                break
            print("❌ Digite S para Sim ou N para Não!")
        
        if confirmacao == "N":
            print("❌ Configuração cancelada!")
            return None
            
        return full_config
    
    def create_company_with_bios(self, config: Dict, output_path: Path):
        """Criar empresa completa com biografias automáticas"""
        
        print(f"\n🚀 CRIANDO EMPRESA COMPLETA: {config['name']}")
        print("="*60)
        
        # Criar estrutura base
        empresa_path = output_path / f"EMPRESA_{config['name'].replace(' ', '_').upper()}"
        empresa_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Pasta criada: {empresa_path}")
        
        # Criar estrutura de pastas organizadas
        pastas_estrutura = [
            "01_DOCUMENTACAO_GERAL",
            "02_SCRIPTS_AUTOMACAO", 
            "03_N8N_WORKFLOWS",
            "04_PERSONAS_SCRIPTS_1_2_3",
            "05_TEMPLATES_SISTEMA",
            "06_LOGS_E_RELATORIOS",
            "07_RAG_KNOWLEDGE_BASE",
            "08_EMAIL_TEMPLATES",
            "09_TASKTODO_WORKFLOWS"
        ]
        
        for pasta in pastas_estrutura:
            (empresa_path / pasta).mkdir(exist_ok=True)
            
        print("📋 Estrutura de pastas criada")
        
        # Gerar personas com biografias
        print("\n🎭 Gerando personas com biografias automáticas...")
        personas_config = self.bio_generator.generate_personas_config(config)
        
        # Salvar biografias
        self.bio_generator.save_personas_biografias(personas_config, empresa_path)
        
        # Salvar configuração da empresa
        config_file = empresa_path / "company_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        # Criar README da empresa
        self.create_company_readme(config, personas_config, empresa_path)
        
        print(f"\n🎉 EMPRESA CRIADA COM SUCESSO!")
        print(f"📁 Localização: {empresa_path}")
        print(f"📋 Total de personas: {len([p for cat in personas_config.values() if isinstance(cat, dict) for p in cat.values()]) + (1 if 'ceo' in personas_config else 0)}")
        print(f"📖 Configuração salva em: {config_file}")
        
        return empresa_path
        
    def create_company_readme(self, config: Dict, personas_config: Dict, empresa_path: Path):
        """Criar README da empresa"""
        
        total_personas = len([p for cat in personas_config.values() if isinstance(cat, dict) for p in cat.values()]) + (1 if 'ceo' in personas_config else 0)
        
        readme_content = f"""# 🏢 {config['name']}

> **{config['description']}**

## 📋 **INFORMAÇÕES DA EMPRESA**

- **🌐 Domínio:** {config['domain']}
- **🏭 Indústria:** {config['industry_desc']}
- **👥 Público-alvo:** {config['target_audience']}
- **🌍 Demografia:** {config['nacionalidade_desc']}
- **👥 Total de Personas:** {total_personas}

## 👥 **EQUIPE EXECUTIVA**

### 👔 **CEO**
- **{personas_config['ceo']['nome_completo']}** - Chief Executive Officer

### 👨‍💼 **Executivos**
"""
        
        if 'executivos' in personas_config:
            for persona_id, persona in personas_config['executivos'].items():
                readme_content += f"- **{persona['nome_completo']}** - {persona['role']}\n"
        
        readme_content += f"""
### 👨‍💼 **Assistentes Executivos**
"""
        
        if 'assistentes' in personas_config:
            for persona_id, persona in personas_config['assistentes'].items():
                readme_content += f"- **{persona['nome_completo']}** - {persona['role']}\n"
        
        readme_content += f"""
### 🎯 **Especialistas**
"""
        
        if 'especialistas' in personas_config:
            for persona_id, persona in personas_config['especialistas'].items():
                readme_content += f"- **{persona['nome_completo']}** - {persona['especializacao']}\n"
        
        readme_content += f"""
## 📁 **ESTRUTURA DE ARQUIVOS**

```
{empresa_path.name}/
├── 01_DOCUMENTACAO_GERAL/      # Documentação e políticas
├── 02_SCRIPTS_AUTOMACAO/       # Scripts de processamento
├── 03_N8N_WORKFLOWS/           # Workflows de automação
├── 04_PERSONAS_SCRIPTS_1_2_3/  # Personas e outputs dos scripts
├── 05_TEMPLATES_SISTEMA/       # Templates reutilizáveis
├── 06_LOGS_E_RELATORIOS/      # Logs e relatórios
├── 07_RAG_KNOWLEDGE_BASE/     # Base de conhecimento
├── 08_EMAIL_TEMPLATES/        # Templates de email
└── 09_TASKTODO_WORKFLOWS/     # Workflows TaskTodo
```

## 🚀 **PRÓXIMOS PASSOS**

1. **✅ Biografias criadas automaticamente**
2. **⚡ Executar Scripts 1-5 sequencialmente:**
   - Script 1: Competências (baseado nas biografias)
   - Script 2: Tech Specs (especificações técnicas)
   - Script 3: RAG Knowledge Base
   - Script 4: TaskTodo Analysis
   - Script 5: Workflows N8N

3. **🔍 Validar outputs** de cada script
4. **🎯 Customizar** conforme necessário

## 📊 **STATUS DO PROJETO**

- [x] ✅ Empresa criada
- [x] ✅ Estrutura de pastas configurada
- [x] ✅ Personas e biografias geradas
- [ ] ⏳ Scripts 1-5 executados
- [ ] ⏳ Workflows N8N configurados
- [ ] ⏳ Sistema RAG implementado

---

*Empresa criada automaticamente pelo Virtual Company Generator v2.0.0*  
*Data: {datetime.now().strftime('%d/%m/%Y às %H:%M')}*"""
        
        readme_file = empresa_path / "README_EMPRESA.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print(f"📖 README criado: {readme_file}")

def main():
    """Função principal"""
    
    setup = AdvancedCompanySetup()
    config = setup.run_setup()
    
    if config:
        # Definir pasta de output
        output_path = Path(__file__).parent.parent.parent / "output"
        output_path.mkdir(exist_ok=True)
        
        # Criar empresa
        empresa_path = setup.create_company_with_bios(config, output_path)
        
        print(f"\n🎯 Para processar as personas, use:")
        print(f"   python virtual_company_master.py")
        print(f"   → Opção 2: Executar Scripts em Empresa Existente")
        print(f"   → Caminho: {empresa_path}")

if __name__ == "__main__":
    main()