#!/usr/bin/env python3
"""
🎯 GERADOR AUTOMÁTICO DE BIOGRAFIAS DE PERSONAS
===============================================

Gera biografias completas e detalhadas automaticamente baseado nos 
parâmetros demográficos e configurações da empresa.

Versão: 1.0.0
Autor: Sergio Castro  
Data: November 2025
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class AutoBiografiaGenerator:
    def __init__(self):
        """Inicializar gerador automático de biografias"""
        
        # Configurações demográficas
        self.nacionalidades = {
            "europeus": {
                "paises": ["França", "Alemanha", "Itália", "Espanha", "Reino Unido", "Holanda", "Suécia"],
                "nomes_masculinos": ["Pierre", "Hans", "Marco", "Carlos", "James", "Erik", "Anders"],
                "nomes_femininos": ["Marie", "Greta", "Sofia", "Carmen", "Emma", "Anna", "Astrid"],
                "sobrenomes": ["Dubois", "Schmidt", "Rossi", "Garcia", "Smith", "Van Der Berg", "Andersson"]
            },
            "latinos": {
                "paises": ["Brasil", "México", "Argentina", "Colômbia", "Chile", "Peru", "Venezuela"],
                "nomes_masculinos": ["João", "Diego", "Mateo", "Carlos", "Sebastián", "Luis", "Rafael"],
                "nomes_femininos": ["Ana", "Sofia", "Isabella", "Camila", "Valentina", "Lucia", "Carmen"],
                "sobrenomes": ["Silva", "Rodriguez", "Gonzalez", "Martinez", "Lopez", "Perez", "Sanchez"]
            },
            "asiaticos": {
                "paises": ["Japão", "Coreia do Sul", "China", "Singapura", "Taiwan", "Hong Kong", "Tailândia"],
                "nomes_masculinos": ["Hiroshi", "Min-jun", "Wei", "Kai", "Chen", "Akira", "Somchai"],
                "nomes_femininos": ["Yuki", "So-young", "Li", "Mei", "Lin", "Sakura", "Ploy"],
                "sobrenomes": ["Tanaka", "Kim", "Wang", "Lee", "Chen", "Yamamoto", "Sato"]
            },
            "oriente_medio": {
                "paises": ["Emirados Árabes Unidos", "Israel", "Turquia", "Líbano", "Jordânia", "Qatar"],
                "nomes_masculinos": ["Ahmed", "David", "Mehmet", "Omar", "Khalil", "Rashid"],
                "nomes_femininos": ["Fatima", "Sarah", "Ayşe", "Layla", "Noor", "Zara"],
                "sobrenomes": ["Al-Rashid", "Cohen", "Özkan", "Khoury", "Al-Zahra", "Al-Maktoum"]
            },
            "balcas": {
                "paises": ["Sérvia", "Croácia", "Bósnia", "Montenegro", "Eslovênia", "Macedônia"],
                "nomes_masculinos": ["Miloš", "Marko", "Stefan", "Aleksandar", "Nikola", "Luka"],
                "nomes_femininos": ["Ana", "Milica", "Jovana", "Marija", "Teodora", "Nevena"],
                "sobrenomes": ["Petrović", "Nikolić", "Marković", "Đorđević", "Stojanović", "Ilić"]
            },
            "nordicos": {
                "paises": ["Suécia", "Noruega", "Dinamarca", "Finlândia", "Islândia"],
                "nomes_masculinos": ["Erik", "Lars", "Magnus", "Bjørn", "Olaf", "Gunnar"],
                "nomes_femininos": ["Astrid", "Ingrid", "Sigrid", "Helga", "Freya", "Solveig"],
                "sobrenomes": ["Andersson", "Hansen", "Nielsen", "Virtanen", "Eriksson", "Olsen"]
            }
        }
        
        # Idiomas por região
        self.idiomas_regionais = {
            "europeus": ["inglês", "francês", "alemão", "italiano", "espanhol"],
            "latinos": ["espanhol", "português", "inglês", "francês"],
            "asiaticos": ["inglês", "japonês", "coreano", "chinês", "tailandês"],
            "oriente_medio": ["inglês", "árabe", "hebraico", "turco"],
            "balcas": ["inglês", "sérvio", "croata", "bósnio", "esloveno"],
            "nordicos": ["inglês", "sueco", "norueguês", "dinamarquês", "finlandês"]
        }
        
        # Templates de especialidades
        self.especialidades = {
            "hr": "Recursos Humanos e Gestão de Talentos",
            "youtube": "Criação de Conteúdo e YouTube Marketing",
            "midias_sociais": "Marketing Digital e Mídias Sociais", 
            "marketing": "Marketing Estratégico e Growth Hacking",
            "financeiro": "Análise Financeira e Controladoria",
            "tecnologia": "Desenvolvimento de Sistemas e DevOps"
        }
        
        # Templates de educação por área
        self.educacao_templates = {
            "executivo": [
                "MBA em Administração de Empresas pela Harvard Business School",
                "Mestrado em Gestão Estratégica pela INSEAD", 
                "Bacharelado em Economia pela Universidade de Stanford",
                "MBA em Liderança pela Wharton School"
            ],
            "assistente": [
                "Bacharelado em Administração de Empresas",
                "Tecnólogo em Gestão Comercial",
                "Curso Superior em Secretariado Executivo",
                "Bacharelado em Comunicação Social"
            ],
            "especialista": {
                "hr": "Bacharelado em Psicologia Organizacional e MBA em Gestão de Pessoas",
                "youtube": "Bacharelado em Comunicação Social com especialização em Marketing Digital",
                "midias_sociais": "Bacharelado em Marketing Digital e Certificação Google Analytics",
                "marketing": "Bacharelado em Marketing e MBA em Growth Marketing",
                "financeiro": "Bacharelado em Ciências Contábeis e CFA Charter",
                "tecnologia": "Bacharelado em Ciência da Computação e Certificações AWS"
            }
        }
        
    def generate_personas_config(self, company_config: Dict) -> Dict:
        """Gera configuração completa de personas baseado nos parâmetros"""
        
        # Extrair configurações
        nacionalidade = company_config.get("nacionalidade", "latinos")
        ceo_genero = company_config.get("ceo_genero", "masculino")
        exec_homens = int(company_config.get("executivos_homens", 2))
        exec_mulheres = int(company_config.get("executivos_mulheres", 2))
        assist_homens = int(company_config.get("assistentes_homens", 2))
        assist_mulheres = int(company_config.get("assistentes_mulheres", 3))  # +1 pelo CEO
        espec_homens = int(company_config.get("especialistas_homens", 3))
        espec_mulheres = int(company_config.get("especialistas_mulheres", 3))
        idiomas_extras = company_config.get("idiomas_extras", [])
        
        # Idiomas padrão + extras
        idiomas_base = ["inglês", "espanhol", "português", "francês"]
        idiomas_regionais = self.idiomas_regionais.get(nacionalidade, ["inglês"])
        todos_idiomas = list(set(idiomas_base + idiomas_regionais + idiomas_extras))
        
        personas_config = {}
        
        # 1. CEO
        ceo = self.generate_persona_bio(
            role="CEO", 
            categoria="executivos",
            genero=ceo_genero,
            nacionalidade=nacionalidade,
            idiomas=todos_idiomas,
            company_config=company_config,
            is_ceo=True
        )
        personas_config["ceo"] = ceo
        
        # 2. Executivos
        personas_config["executivos"] = {}
        
        # Executivos homens
        for i in range(exec_homens):
            exec_persona = self.generate_persona_bio(
                role="Executivo",
                categoria="executivos", 
                genero="masculino",
                nacionalidade=nacionalidade,
                idiomas=todos_idiomas,
                company_config=company_config
            )
            personas_config["executivos"][f"executivo_m_{i+1}"] = exec_persona
            
        # Executivos mulheres  
        for i in range(exec_mulheres):
            exec_persona = self.generate_persona_bio(
                role="Executiva",
                categoria="executivos",
                genero="feminino", 
                nacionalidade=nacionalidade,
                idiomas=todos_idiomas,
                company_config=company_config
            )
            personas_config["executivos"][f"executiva_f_{i+1}"] = exec_persona
        
        # 3. Assistentes
        personas_config["assistentes"] = {}
        
        # Assistentes homens
        for i in range(assist_homens):
            assist_persona = self.generate_persona_bio(
                role="Assistente Executivo",
                categoria="assistentes",
                genero="masculino",
                nacionalidade=nacionalidade, 
                idiomas=todos_idiomas,
                company_config=company_config
            )
            personas_config["assistentes"][f"assistente_m_{i+1}"] = assist_persona
            
        # Assistentes mulheres
        for i in range(assist_mulheres):
            assist_persona = self.generate_persona_bio(
                role="Assistente Executiva", 
                categoria="assistentes",
                genero="feminino",
                nacionalidade=nacionalidade,
                idiomas=todos_idiomas,
                company_config=company_config
            )
            personas_config["assistentes"][f"assistente_f_{i+1}"] = assist_persona
        
        # 4. Especialistas (6 áreas fixas)
        personas_config["especialistas"] = {}
        especialidades_lista = list(self.especialidades.keys())
        
        # Distribuir especialidades entre homens e mulheres
        total_especialistas = espec_homens + espec_mulheres
        especialidades_distribuidas = []
        
        for i, especialidade in enumerate(especialidades_lista):
            genero = "masculino" if i < espec_homens else "feminino"
            
            espec_persona = self.generate_persona_bio(
                role=f"Especialista {self.especialidades[especialidade]}",
                categoria="especialistas",
                genero=genero,
                nacionalidade=nacionalidade,
                idiomas=todos_idiomas, 
                company_config=company_config,
                especialidade=especialidade
            )
            personas_config["especialistas"][f"especialista_{especialidade}"] = espec_persona
        
        return personas_config
    
    def generate_persona_bio(self, role: str, categoria: str, genero: str, 
                           nacionalidade: str, idiomas: List[str], 
                           company_config: Dict, is_ceo: bool = False,
                           especialidade: str = None) -> Dict:
        """Gera biografia completa de uma persona"""
        
        # Dados demográficos da nacionalidade
        nac_data = self.nacionalidades.get(nacionalidade, self.nacionalidades["latinos"])
        
        # Gerar nome
        if genero == "masculino":
            primeiro_nome = random.choice(nac_data["nomes_masculinos"])
        else:
            primeiro_nome = random.choice(nac_data["nomes_femininos"])
            
        sobrenome = random.choice(nac_data["sobrenomes"])
        nome_completo = f"{primeiro_nome} {sobrenome}"
        
        # Gerar idade baseada no role
        if is_ceo:
            idade = random.randint(35, 50)
        elif categoria == "executivos":
            idade = random.randint(30, 45)
        elif categoria == "assistentes": 
            idade = random.randint(25, 35)
        else:  # especialistas
            idade = random.randint(28, 40)
            
        # País de origem
        pais_origem = random.choice(nac_data["paises"])
        
        # Educação baseada na categoria
        if categoria == "executivos":
            educacao = random.choice(self.educacao_templates["executivo"])
        elif categoria == "assistentes":
            educacao = random.choice(self.educacao_templates["assistente"])
        else:  # especialistas
            if especialidade in self.educacao_templates["especialista"]:
                educacao = self.educacao_templates["especialista"][especialidade]
            else:
                educacao = "Bacharelado em área específica com especializações relevantes"
        
        # Experiência baseada na idade
        anos_experiencia = max(idade - 22, 3)  # Mínimo 3 anos
        
        # Idiomas (selecionar subset dos disponíveis)
        num_idiomas = random.randint(3, min(6, len(idiomas)))
        idiomas_persona = random.sample(idiomas, num_idiomas)
        
        # Especialização específica
        if is_ceo:
            especializacao = "Liderança Executiva e Gestão Estratégica"
        elif categoria == "executivos":
            especializacoes_exec = [
                "Gestão de Operações e Processos",
                "Desenvolvimento de Negócios e Estratégia", 
                "Gestão de Projetos e Inovação",
                "Gestão Comercial e Vendas"
            ]
            especializacao = random.choice(especializacoes_exec)
        elif categoria == "assistentes":
            especializacao = "Suporte Executivo e Gestão Administrativa"
        else:  # especialistas
            especializacao = self.especialidades.get(especialidade, "Especialização Técnica")
        
        # Gerar biografia em markdown
        biografia_md = self.generate_biografia_markdown(
            nome_completo, idade, pais_origem, role, especializacao,
            educacao, anos_experiencia, idiomas_persona, company_config
        )
        
        return {
            "nome_completo": nome_completo,
            "primeiro_nome": primeiro_nome,
            "sobrenome": sobrenome,
            "idade": idade,
            "genero": genero,
            "pais_origem": pais_origem,
            "nacionalidade": nacionalidade,
            "role": role,
            "categoria": categoria,
            "especializacao": especializacao,
            "educacao": educacao,
            "anos_experiencia": anos_experiencia,
            "idiomas": idiomas_persona,
            "biografia_md": biografia_md,
            "especialidade": especialidade,
            "is_ceo": is_ceo
        }
    
    def generate_biografia_markdown(self, nome: str, idade: int, pais: str, 
                                  role: str, especializacao: str, educacao: str,
                                  experiencia: int, idiomas: List[str], 
                                  company_config: Dict) -> str:
        """Gera biografia em formato markdown"""
        
        empresa_nome = company_config.get("name", "Empresa")
        industria = company_config.get("industry", "tecnologia") 
        
        # Determinar pronome
        genero_pronome = "ele" if any(x in nome.lower() for x in ["joão", "carlos", "diego", "luis", "ahmed", "erik"]) else "ela"
        
        biografia = f"""# 👤 {nome}

## 📋 **INFORMAÇÕES BÁSICAS**
- **Nome:** {nome}
- **Idade:** {idade} anos
- **Nacionalidade:** {pais}
- **Cargo:** {role}
- **Especialização:** {especializacao}

## 🎓 **FORMAÇÃO ACADÊMICA**
{educacao}

## 💼 **EXPERIÊNCIA PROFISSIONAL**
Com {experiencia} anos de experiência na área de {especializacao.lower()}, {nome} traz uma perspectiva única e valiosa para a {empresa_nome}. 

Ao longo de sua carreira, {genero_pronome} desenvolveu competências sólidas em:
- Gestão estratégica e operacional
- Liderança de equipes multiculturais
- Desenvolvimento e implementação de processos
- Análise e otimização de resultados
- Comunicação executiva eficaz

## 🌍 **COMPETÊNCIAS LINGUÍSTICAS**
**Idiomas:** {', '.join(idiomas)}

## 🎯 **RESPONSABILIDADES NA {empresa_nome.upper()}**
Como {role}, {nome} é responsável por:
- Suporte direto às operações estratégicas da empresa
- Coordenação de atividades relacionadas à {especializacao.lower()}
- Implementação de melhores práticas na área de {industria}
- Colaboração com equipes internas e stakeholders externos
- Desenvolvimento e execução de iniciativas de crescimento

## 💡 **COMPETÊNCIAS TÉCNICAS**
- Domínio de ferramentas de gestão empresarial
- Conhecimento avançado em metodologias ágeis
- Experiência com sistemas de CRM e ERP
- Análise de dados e KPIs
- Gestão de projetos complexos

## 🤝 **COMPETÊNCIAS COMPORTAMENTAIS**
- Liderança inspiradora e colaborativa
- Comunicação assertiva e empática
- Adaptabilidade e flexibilidade
- Pensamento estratégico
- Orientação para resultados
- Trabalho em equipe multicultural

## 📈 **OBJETIVOS E METAS**
{nome} está focado(a) em contribuir para o crescimento sustentável da {empresa_nome}, aplicando sua experiência em {especializacao.lower()} para:
- Otimizar processos e aumentar a eficiência operacional
- Desenvolver soluções inovadoras para desafios do setor de {industria}
- Fortalecer a cultura organizacional e o engajamento da equipe
- Expandir a presença da empresa no mercado internacional

---
*Biografia gerada automaticamente pelo Virtual Company Generator*
*Data: {datetime.now().strftime('%d/%m/%Y')}*"""

        return biografia
    
    def save_personas_biografias(self, personas_config: Dict, output_path: Path):
        """Salva todas as biografias no formato de arquivos"""
        
        print(f"\n📝 Salvando biografias em: {output_path}")
        
        # Criar estrutura de pastas
        for categoria, personas in personas_config.items():
            if categoria == "ceo":
                # CEO vai para executivos
                cat_path = output_path / "04_PERSONAS_SCRIPTS_1_2_3" / "executivos"
                cat_path.mkdir(parents=True, exist_ok=True)
                
                persona = personas
                persona_name = persona["nome_completo"].replace(" ", "_")
                persona_path = cat_path / persona_name
                persona_path.mkdir(parents=True, exist_ok=True)
                
                # Salvar biografia
                bio_file = persona_path / f"{persona_name}_bio.md"
                with open(bio_file, 'w', encoding='utf-8') as f:
                    f.write(persona["biografia_md"])
                    
                print(f"   ✅ CEO: {persona['nome_completo']}")
                
            else:
                cat_path = output_path / "04_PERSONAS_SCRIPTS_1_2_3" / categoria
                cat_path.mkdir(parents=True, exist_ok=True)
                
                for persona_id, persona in personas.items():
                    persona_name = persona["nome_completo"].replace(" ", "_")
                    persona_path = cat_path / persona_name
                    persona_path.mkdir(parents=True, exist_ok=True)
                    
                    # Salvar biografia
                    bio_file = persona_path / f"{persona_name}_bio.md"
                    with open(bio_file, 'w', encoding='utf-8') as f:
                        f.write(persona["biografia_md"])
                        
                    print(f"   ✅ {categoria.capitalize()}: {persona['nome_completo']}")
        
        # Salvar configuração JSON
        config_file = output_path / "personas_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(personas_config, f, ensure_ascii=False, indent=2)
            
        print(f"\n📋 Configuração salva em: {config_file}")

def main():
    """Função principal para teste do gerador"""
    
    print("🎯 GERADOR AUTOMÁTICO DE BIOGRAFIAS DE PERSONAS")
    print("=" * 60)
    
    generator = AutoBiografiaGenerator()
    
    # Configuração de exemplo
    company_config = {
        "name": "TechVision Solutions",
        "industry": "tecnologia",
        "nacionalidade": "latinos",
        "ceo_genero": "feminino",
        "executivos_homens": 2,
        "executivos_mulheres": 2,
        "assistentes_homens": 2,
        "assistentes_mulheres": 3,
        "especialistas_homens": 3,
        "especialistas_mulheres": 3,
        "idiomas_extras": ["alemão", "japonês"]
    }
    
    print("📋 Configuração de teste:")
    for key, value in company_config.items():
        print(f"   {key}: {value}")
    
    print("\n🔄 Gerando personas...")
    personas_config = generator.generate_personas_config(company_config)
    
    print(f"\n✅ {len([p for cat in personas_config.values() if isinstance(cat, dict) for p in cat.values()]) + (1 if 'ceo' in personas_config else 0)} personas geradas!")
    
    # Salvar em pasta de teste
    test_output = Path("test_biografias_output")
    generator.save_personas_biografias(personas_config, test_output)
    
    print(f"\n🎉 Biografias salvas em: {test_output}")

if __name__ == "__main__":
    main()