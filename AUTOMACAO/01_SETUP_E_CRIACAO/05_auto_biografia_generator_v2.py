#!/usr/bin/env python3
"""
🎯 GERADOR AUTOMÁTICO DE BIOGRAFIAS DE PERSONAS - VERSÃO MELHORADA
===================================================================

Gera biografias completas e detalhadas automaticamente com nomes únicos
para evitar repetições irreais em uma empresa.

Melhorias:
- Sistema de nomes únicos
- Combinações de nomes mais realistas
- Controle de duplicatas
- Melhor distribuição demográfica

Versão: 2.0.0
Autor: Sergio Castro  
Data: November 2025
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set

class AutoBiografiaGeneratorV2:
    def __init__(self):
        """Inicializar gerador automático de biografias com controle de nomes únicos"""
        
        # Configurações demográficas expandidas
        self.nacionalidades = {
            "europeus": {
                "paises": ["França", "Alemanha", "Itália", "Espanha", "Reino Unido", "Holanda", "Suécia", "Bélgica", "Áustria", "Suíça"],
                "nomes_masculinos": ["Pierre", "Hans", "Marco", "Carlos", "James", "Erik", "Anders", "Philippe", "Stefan", "François", "Antonio", "Miguel", "William", "Lars", "Jean"],
                "nomes_femininos": ["Marie", "Greta", "Sofia", "Carmen", "Emma", "Anna", "Astrid", "Camille", "Elena", "Françoise", "Isabella", "Patricia", "Catherine", "Ingrid", "Christine"],
                "sobrenomes": ["Dubois", "Schmidt", "Rossi", "Garcia", "Smith", "Van Der Berg", "Andersson", "Mueller", "Ferrari", "Blanc", "Torres", "Wilson", "Nielsen", "Larsson", "Bernard"]
            },
            "latinos": {
                "paises": ["Brasil", "México", "Argentina", "Colômbia", "Chile", "Peru", "Venezuela", "Uruguai", "Equador", "Costa Rica"],
                "nomes_masculinos": ["João", "Diego", "Mateo", "Carlos", "Sebastián", "Luis", "Rafael", "André", "Fernando", "Gabriel", "Ricardo", "Alejandro", "Eduardo", "Pablo", "Manuel"],
                "nomes_femininos": ["Ana", "Sofia", "Isabella", "Camila", "Valentina", "Lucia", "Carmen", "Maria", "Fernanda", "Gabriela", "Paola", "Andrea", "Carolina", "Adriana", "Patricia"],
                "sobrenomes": ["Silva", "Rodriguez", "Gonzalez", "Martinez", "Lopez", "Perez", "Sanchez", "Fernandez", "Costa", "Oliveira", "Santos", "Ramos", "Castro", "Mendoza", "Herrera"]
            },
            "asiaticos": {
                "paises": ["Japão", "Coreia do Sul", "China", "Singapura", "Taiwan", "Hong Kong", "Tailândia", "Malásia", "Vietnã", "Filipinas"],
                "nomes_masculinos": ["Hiroshi", "Min-jun", "Wei", "Kai", "Chen", "Akira", "Somchai", "Takeshi", "Kenji", "Ryu", "Zhang", "Liu", "Park", "Tanaka", "Wong"],
                "nomes_femininos": ["Yuki", "So-young", "Li", "Mei", "Lin", "Sakura", "Ploy", "Aiko", "Yuki", "Hana", "Wang", "Kim", "Lee", "Sato", "Chan"],
                "sobrenomes": ["Tanaka", "Kim", "Wang", "Lee", "Chen", "Yamamoto", "Sato", "Zhang", "Liu", "Park", "Wong", "Lim", "Ng", "Takahashi", "Watanabe"]
            },
            "oriente_medio": {
                "paises": ["Emirados Árabes Unidos", "Israel", "Turquia", "Líbano", "Jordânia", "Qatar", "Kuwait", "Bahrain"],
                "nomes_masculinos": ["Ahmed", "David", "Mehmet", "Omar", "Khalil", "Rashid", "Ali", "Hassan", "Ibrahim", "Yusuf", "Mustafa", "Salim", "Fares", "Karim", "Samir"],
                "nomes_femininos": ["Fatima", "Sarah", "Ayşe", "Layla", "Noor", "Zara", "Amira", "Leila", "Yasmin", "Rania", "Dina", "Mira", "Salma", "Hala", "Rana"],
                "sobrenomes": ["Al-Rashid", "Cohen", "Özkan", "Khoury", "Al-Zahra", "Al-Maktoum", "Hassan", "Al-Ahmad", "Mansour", "Khalil", "Saleh", "Farouk", "Nasr", "Qasemi", "Sharif"]
            },
            "balcas": {
                "paises": ["Sérvia", "Croácia", "Bósnia", "Montenegro", "Eslovênia", "Macedônia", "Albânia", "Kosovo"],
                "nomes_masculinos": ["Miloš", "Marko", "Stefan", "Aleksandar", "Nikola", "Luka", "Petar", "Milan", "Zoran", "Dragan", "Vladimir", "Igor", "Bojan", "Dusan", "Nemanja"],
                "nomes_femininos": ["Ana", "Milica", "Jovana", "Marija", "Teodora", "Nevena", "Jelena", "Tamara", "Ivana", "Sonja", "Dragana", "Gordana", "Biljana", "Svetlana", "Vesna"],
                "sobrenomes": ["Petrović", "Nikolić", "Marković", "Đorđević", "Stojanović", "Ilić", "Jovanović", "Milenković", "Stanković", "Popović", "Mladenović", "Stefanović", "Mitrović", "Radović", "Simić"]
            },
            "nordicos": {
                "paises": ["Suécia", "Noruega", "Dinamarca", "Finlândia", "Islândia"],
                "nomes_masculinos": ["Erik", "Lars", "Magnus", "Bjørn", "Olaf", "Gunnar", "Nils", "Sven", "Arne", "Knut", "Johan", "Anders", "Mikael", "Fredrik", "Henrik"],
                "nomes_femininos": ["Astrid", "Ingrid", "Sigrid", "Helga", "Freya", "Solveig", "Birgitta", "Margareta", "Elin", "Karin", "Annika", "Lena", "Maja", "Sara", "Linnea"],
                "sobrenomes": ["Andersson", "Hansen", "Nielsen", "Virtanen", "Eriksson", "Olsen", "Johansson", "Svensson", "Petersen", "Carlsson", "Lindberg", "Gustafsson", "Møller", "Berg", "Dahl"]
            }
        }
        
        # Controle de nomes únicos
        self.nomes_usados: Set[str] = set()
        self.combinacoes_usadas: Set[tuple] = set()
        
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
                "MBA em Liderança pela Wharton School",
                "Mestrado em Negócios Internacionais pela London Business School",
                "MBA Executivo pela Kellogg School of Management",
                "Mestrado em Estratégia Empresarial pela Cambridge Judge Business School"
            ],
            "assistente": [
                "Bacharelado em Administração de Empresas",
                "Tecnólogo em Gestão Comercial",
                "Curso Superior em Secretariado Executivo",
                "Bacharelado em Comunicação Social",
                "Tecnólogo em Processos Gerenciais",
                "Bacharelado em Relações Públicas",
                "Curso Superior em Gestão de Recursos Humanos"
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
    
    def reset_nomes_usados(self):
        """Reset o controle de nomes para uma nova empresa"""
        self.nomes_usados.clear()
        self.combinacoes_usadas.clear()
    
    def generate_unique_name(self, genero: str, nacionalidade: str, max_attempts: int = 50) -> Tuple[str, str, str]:
        """
        Gera um nome único que não foi usado ainda na empresa
        """
        nac_data = self.nacionalidades.get(nacionalidade, self.nacionalidades["latinos"])
        
        for attempt in range(max_attempts):
            # Selecionar nome baseado no gênero
            if genero == "masculino":
                primeiro_nome = random.choice(nac_data["nomes_masculinos"])
            else:
                primeiro_nome = random.choice(nac_data["nomes_femininos"])
            
            sobrenome = random.choice(nac_data["sobrenomes"])
            nome_completo = f"{primeiro_nome} {sobrenome}"
            
            # Verificar se a combinação não foi usada
            combinacao = (primeiro_nome, sobrenome, nacionalidade)
            
            if nome_completo not in self.nomes_usados and combinacao not in self.combinacoes_usadas:
                # Marcar como usado
                self.nomes_usados.add(nome_completo)
                self.combinacoes_usadas.add(combinacao)
                return primeiro_nome, sobrenome, nome_completo
        
        # Se não conseguiu gerar um nome único, adiciona sufixo
        base_nome = f"{primeiro_nome} {sobrenome}"
        for i in range(1, 100):
            nome_com_sufixo = f"{primeiro_nome} {sobrenome} {chr(65+i)}"  # A, B, C...
            if nome_com_sufixo not in self.nomes_usados:
                self.nomes_usados.add(nome_com_sufixo)
                return primeiro_nome, f"{sobrenome} {chr(65+i)}", nome_com_sufixo
        
        # Fallback final
        timestamp = str(int(datetime.now().timestamp()))[-3:]
        nome_final = f"{primeiro_nome} {sobrenome}{timestamp}"
        self.nomes_usados.add(nome_final)
        return primeiro_nome, f"{sobrenome}{timestamp}", nome_final
    
    def generate_personas_config(self, company_config: Dict) -> Dict:
        """Gera configuração completa de personas baseado nos parâmetros"""
        
        # Reset nomes para nova empresa
        self.reset_nomes_usados()
        
        # Extrair configurações
        nacionalidade = company_config.get("nacionalidade", "latinos")
        ceo_genero = company_config.get("ceo_genero", "masculino")
        exec_homens = int(company_config.get("executivos_homens", 2))
        exec_mulheres = int(company_config.get("executivos_mulheres", 2))
        assist_homens = int(company_config.get("assistentes_homens", 2))
        assist_mulheres = int(company_config.get("assistentes_mulheres", 3))
        espec_homens = int(company_config.get("especialistas_homens", 3))
        espec_mulheres = int(company_config.get("especialistas_mulheres", 3))
        idiomas_extras = company_config.get("idiomas_extras", [])
        
        # Idiomas padrão + extras
        idiomas_base = ["inglês", "espanhol", "português", "francês"]
        idiomas_regionais = self.idiomas_regionais.get(nacionalidade, ["inglês"])
        todos_idiomas = list(set(idiomas_base + idiomas_regionais + idiomas_extras))
        
        personas_config = {}
        
        print(f"\n🎯 Gerando personas com nomes únicos para {company_config.get('name', 'Empresa')}...")
        
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
        print(f"   👑 CEO: {ceo['nome_completo']}")
        
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
            print(f"   👔 Executivo: {exec_persona['nome_completo']}")
            
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
            print(f"   👩‍💼 Executiva: {exec_persona['nome_completo']}")
        
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
            print(f"   📋 Assistente: {assist_persona['nome_completo']}")
            
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
            print(f"   📋 Assistente: {assist_persona['nome_completo']}")
        
        # 4. Especialistas (6 áreas fixas)
        personas_config["especialistas"] = {}
        especialidades_lista = list(self.especialidades.keys())
        
        # Distribuir especialidades entre homens e mulheres
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
            print(f"   🎯 Especialista: {espec_persona['nome_completo']} ({especialidade})")
        
        print(f"\n✅ Total de personas únicas geradas: {len(self.nomes_usados)}")
        
        return personas_config
    
    def generate_persona_bio(self, role: str, categoria: str, genero: str, 
                           nacionalidade: str, idiomas: List[str], 
                           company_config: Dict, is_ceo: bool = False,
                           especialidade: str = None) -> Dict:
        """Gera biografia completa de uma persona com nome único"""
        
        # Gerar nome único
        primeiro_nome, sobrenome, nome_completo = self.generate_unique_name(genero, nacionalidade)
        
        # Dados demográficos da nacionalidade
        nac_data = self.nacionalidades.get(nacionalidade, self.nacionalidades["latinos"])
        
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
        
        # Determinar pronome baseado em nomes conhecidos
        nomes_masculinos = ["joão", "carlos", "diego", "luis", "ahmed", "erik", "pierre", "hans", "marco", "james", "hiroshi", "min-jun", "wei", "mehmet", "omar", "miloš", "marko", "stefan", "lars", "magnus"]
        genero_pronome = "ele" if any(x in nome.lower() for x in nomes_masculinos) else "ela"
        
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
*Biografia gerada automaticamente pelo Virtual Company Generator v2.0.0*
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
        print(f"🎉 Total de nomes únicos gerados: {len(self.nomes_usados)}")
        
        # Salvar relatório de nomes únicos
        names_report = {
            "total_personas": len(self.nomes_usados),
            "nomes_gerados": sorted(list(self.nomes_usados)),
            "combinacoes_unicas": len(self.combinacoes_usadas),
            "timestamp": datetime.now().isoformat()
        }
        
        report_file = output_path / "unique_names_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(names_report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 Relatório de nomes únicos salvo em: {report_file}")

def main():
    """Função principal para teste do gerador melhorado"""
    
    print("🎯 GERADOR AUTOMÁTICO DE BIOGRAFIAS DE PERSONAS v2.0.0")
    print("=" * 70)
    print("✨ Melhorias: Nomes únicos, sem repetições!")
    
    generator = AutoBiografiaGeneratorV2()
    
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
    
    print("\n🔄 Gerando personas com controle de nomes únicos...")
    personas_config = generator.generate_personas_config(company_config)
    
    total_personas = len([p for cat in personas_config.values() if isinstance(cat, dict) for p in cat.values()]) + (1 if 'ceo' in personas_config else 0)
    print(f"\n✅ {total_personas} personas geradas com nomes únicos!")
    
    # Salvar em pasta de teste
    test_output = Path("test_biografias_output_v2")
    generator.save_personas_biografias(personas_config, test_output)
    
    print(f"\n🎉 Biografias salvas em: {test_output}")
    print("🔍 Verifique o arquivo 'unique_names_report.json' para confirmar unicidade dos nomes!")

if __name__ == "__main__":
    main()