#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Virtual Company Generator - Versão de Projeto Individual
Cria empresas virtuais DENTRO da pasta de cada projeto específico
"""

import json
import os
from pathlib import Path
from datetime import datetime
import sys

class VirtualCompanyGenerator:
    """Gerador de empresas virtuais para projetos individuais"""
    
    def __init__(self, project_path=None):
        """
        Inicializa o gerador para um projeto específico
        
        Args:
            project_path: Caminho da pasta do projeto onde será criada a empresa
        """
        if project_path:
            self.project_path = Path(project_path).resolve()
        else:
            # Se não informado, usa a pasta atual
            self.project_path = Path.cwd().resolve()
            
        self.company_info = {}
        
        # Indústrias suportadas
        self.industries = {
            "1": "healthcare",
            "2": "education", 
            "3": "consulting",
            "4": "immigration",
            "5": "ecommerce",
            "6": "automotive",
            "7": "technology",
            "8": "finance",
            "9": "real_estate",
            "10": "food_service"
        }
        
        # Templates de personas por setor
        self.industry_templates = {
            "healthcare": {
                "focus": "saúde e bem-estar",
                "executivos": ["COMERCIAL", "CLINICO", "OPERACIONAL"],
                "specialties": ["VENDAS", "ATENDIMENTO", "PROCESSOS"]
            },
            "education": {
                "focus": "educação e desenvolvimento",
                "executivos": ["ACADEMICO", "COMERCIAL", "OPERACIONAL"], 
                "specialties": ["PEDAGOGICO", "VENDAS", "PROCESSOS"]
            },
            "consulting": {
                "focus": "consultoria e estratégia",
                "executivos": ["COMERCIAL", "ESTRATEGICO", "OPERACIONAL"],
                "specialties": ["VENDAS", "ANALISE", "PROCESSOS"] 
            },
            "immigration": {
                "focus": "imigração e legalização",
                "executivos": ["COMERCIAL", "JURIDICO", "OPERACIONAL"],
                "specialties": ["VENDAS", "LEGAL", "PROCESSOS"]
            },
            "ecommerce": {
                "focus": "comércio eletrônico",
                "executivos": ["COMERCIAL", "DIGITAL", "OPERACIONAL"],
                "specialties": ["VENDAS", "MARKETING_DIGITAL", "LOGISTICA"]
            },
            "automotive": {
                "focus": "automotivo e mobilidade", 
                "executivos": ["COMERCIAL", "TECNICO", "OPERACIONAL"],
                "specialties": ["VENDAS", "MANUTENCAO", "PROCESSOS"]
            },
            "technology": {
                "focus": "tecnologia e inovação",
                "executivos": ["COMERCIAL", "TECNICO", "OPERACIONAL"],
                "specialties": ["VENDAS", "DESENVOLVIMENTO", "PROCESSOS"]
            },
            "finance": {
                "focus": "serviços financeiros",
                "executivos": ["COMERCIAL", "FINANCEIRO", "OPERACIONAL"],
                "specialties": ["VENDAS", "ANALISE_CREDITO", "PROCESSOS"]
            },
            "real_estate": {
                "focus": "mercado imobiliário", 
                "executivos": ["COMERCIAL", "AVALIACOES", "OPERACIONAL"],
                "specialties": ["VENDAS", "CORRETAGEM", "PROCESSOS"]
            },
            "food_service": {
                "focus": "alimentação e gastronomia",
                "executivos": ["COMERCIAL", "CULINARIO", "OPERACIONAL"], 
                "specialties": ["VENDAS", "PRODUCAO", "PROCESSOS"]
            }
        }

    def collect_company_info(self):
        """Coleta informações da empresa"""
        print("🏢 GERADOR DE EMPRESA VIRTUAL")
        print("=" * 50)
        print(f"📁 Pasta do projeto: {self.project_path}")
        print("=" * 50)
        
        # Nome da empresa
        company_name = input("\n📝 Nome da empresa: ").strip()
        if not company_name:
            print("❌ Nome da empresa é obrigatório!")
            sys.exit(1)
            
        # Setor
        print("\n🏭 Setores disponíveis:")
        for key, value in self.industries.items():
            print(f"  {key}. {value.replace('_', ' ').title()}")
        
        industry_choice = input("\n🎯 Escolha o setor (número): ").strip()
        if industry_choice not in self.industries:
            print("❌ Setor inválido!")
            sys.exit(1)
            
        industry = self.industries[industry_choice]
        
        # Informações adicionais
        description = input("\n📋 Descrição da empresa (opcional): ").strip()
        if not description:
            template = self.industry_templates.get(industry, {})
            focus = template.get("focus", "negócios")
            description = f"Empresa especializada em {focus}"
        
        # Armazena as informações
        self.company_info = {
            "name": company_name,
            "industry": industry,
            "description": description,
            "creation_date": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "personas_count": 16
        }
        
        print(f"\n✅ Empresa '{company_name}' configurada para o setor '{industry}'")
        return True

    def generate_personas(self):
        """Gera todas as 16 personas da empresa"""
        company_name = self.company_info["name"]
        industry = self.company_info["industry"]
        template = self.industry_templates.get(industry, self.industry_templates["technology"])
        
        personas = {}
        
        # 1. CEO (1 persona)
        ceo = {
            "name": "Maria Silva",
            "role": "CEO", 
            "department": "CEO",
            "level": "C-Level",
            "responsibilities": [
                "Liderança estratégica da empresa",
                "Tomada de decisões executivas",
                "Representação institucional",
                "Gestão de resultados gerais"
            ],
            "skills": [
                "Liderança executiva",
                "Visão estratégica", 
                "Comunicação institucional",
                "Gestão de performance"
            ]
        }
        personas["CEO"] = {"Maria_Silva_CEO": ceo}
        
        # 2. EXECUTIVOS (3 personas)
        executive_names = ["Carlos Santos", "Ana Costa", "Pedro Oliveira"]
        executive_roles = template["executivos"]
        
        personas["EXECUTIVOS"] = {}
        for i, (name, role) in enumerate(zip(executive_names, executive_roles)):
            key = f"{name.replace(' ', '_')}_EXECUTIVO_{role}"
            persona = {
                "name": name,
                "role": f"EXECUTIVO {role}",
                "department": "EXECUTIVOS", 
                "level": "Executive",
                "responsibilities": [
                    f"Gestão estratégica da área {role.lower()}",
                    f"Supervisão de equipes {role.lower()}",
                    f"Planejamento {role.lower()}",
                    "Reporting para CEO"
                ],
                "skills": [
                    f"Expertise em {role.lower()}",
                    "Gestão de equipes",
                    "Planejamento estratégico", 
                    "Análise de performance"
                ]
            }
            personas["EXECUTIVOS"][key] = persona
        
        # 3. ASSISTENTES (3 personas)  
        assistant_names = ["Julia Ferreira", "Lucas Pereira", "Sofia Lima"]
        
        personas["ASSISTENTES"] = {}
        for i, (name, exec_role) in enumerate(zip(assistant_names, executive_roles)):
            key = f"{name.replace(' ', '_')}_ASSISTENTE_{exec_role}"
            persona = {
                "name": name,
                "role": f"ASSISTENTE {exec_role}",
                "department": "ASSISTENTES",
                "level": "Support",
                "responsibilities": [
                    f"Apoio ao executivo {exec_role.lower()}",
                    f"Coordenação de atividades {exec_role.lower()}",
                    "Organização de agenda e reuniões",
                    "Comunicação interna"
                ],
                "skills": [
                    "Organização e planejamento",
                    f"Conhecimento em {exec_role.lower()}",
                    "Comunicação efetiva",
                    "Gestão de tempo"
                ]
            }
            personas["ASSISTENTES"][key] = persona
        
        # 4. ESPECIALISTAS (3 personas)
        specialist_names = ["Roberto Mendes", "Camila Rocha", "Diego Alves"] 
        specialist_roles = template["specialties"]
        
        personas["ESPECIALISTAS"] = {}
        for i, (name, role) in enumerate(zip(specialist_names, specialist_roles)):
            key = f"{name.replace(' ', '_')}_ESPECIALISTA_{role}"
            persona = {
                "name": name,
                "role": f"ESPECIALISTA {role}",
                "department": "ESPECIALISTAS",
                "level": "Specialist", 
                "responsibilities": [
                    f"Execução especializada em {role.lower()}",
                    f"Otimização de processos {role.lower()}",
                    "Treinamento de equipes",
                    "Inovação e melhoria contínua"
                ],
                "skills": [
                    f"Especialização técnica em {role.lower()}",
                    "Resolução de problemas",
                    "Treinamento e capacitação",
                    "Análise e otimização"
                ]
            }
            personas["ESPECIALISTAS"][key] = persona
        
        # 5. SUPORTE (6 personas)
        support_data = [
            ("Fernanda Cruz", "CLIENTE", "Atendimento ao cliente"),
            ("Rafael Souza", "TECNICO", "Suporte técnico"),
            ("Beatriz Martins", "FINANCEIRO", "Suporte financeiro"),
            ("Thiago Barbosa", "RH", "Recursos humanos"),
            ("Larissa Gomes", "JURIDICO", "Suporte jurídico"),
            ("Gabriel Silva", "TI", "Tecnologia da informação")
        ]
        
        personas["SUPORTE"] = {}
        for name, role, area in support_data:
            key = f"{name.replace(' ', '_')}_SUPORTE_{role}"
            persona = {
                "name": name,
                "role": f"SUPORTE {role}",
                "department": "SUPORTE",
                "level": "Support",
                "responsibilities": [
                    f"Suporte especializado em {area.lower()}",
                    f"Resolução de demandas {area.lower()}",
                    "Atendimento interno e externo",
                    "Documentação e processos"
                ],
                "skills": [
                    f"Conhecimento técnico em {area.lower()}",
                    "Atendimento ao cliente",
                    "Resolução de problemas",
                    "Comunicação clara"
                ]
            }
            personas["SUPORTE"][key] = persona
        
        return personas

    def create_folder_structure(self, personas):
        """Cria estrutura de pastas DENTRO do projeto"""
        company_name = self.company_info["name"]
        
        # Pasta da empresa DENTRO do projeto atual
        company_folder = self.project_path / f"{company_name}_virtual_company"
        
        print(f"\n📁 Criando estrutura em: {company_folder}")
        
        # Estrutura de pastas
        folders = [
            "config",
            "personas/CEO", 
            "personas/EXECUTIVOS",
            "personas/ASSISTENTES", 
            "personas/ESPECIALISTAS",
            "personas/SUPORTE",
            "workflows/comercial",
            "workflows/marketing", 
            "workflows/operacional",
            "workflows/suporte",
            "docs",
            "logs"
        ]
        
        # Cria todas as pastas
        for folder in folders:
            folder_path = company_folder / folder
            folder_path.mkdir(parents=True, exist_ok=True)
        
        # 1. Salva configuração da empresa
        config_file = company_folder / "config" / "company_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.company_info, f, ensure_ascii=False, indent=2)
        
        # 2. Salva personas por categoria
        for category, category_personas in personas.items():
            category_folder = company_folder / "personas" / category
            
            for persona_key, persona_data in category_personas.items():
                persona_file = category_folder / f"{persona_key}.json"
                with open(persona_file, 'w', encoding='utf-8') as f:
                    json.dump(persona_data, f, ensure_ascii=False, indent=2)
        
        # 3. Configuração das personas
        personas_config = {
            "company": company_name,
            "total_personas": 16,
            "categories": {
                "CEO": 1,
                "EXECUTIVOS": 3, 
                "ASSISTENTES": 3,
                "ESPECIALISTAS": 3,
                "SUPORTE": 6
            },
            "created_date": datetime.now().isoformat()
        }
        
        personas_config_file = company_folder / "config" / "personas_config.json"
        with open(personas_config_file, 'w', encoding='utf-8') as f:
            json.dump(personas_config, f, ensure_ascii=False, indent=2)
        
        # 4. Documentação da empresa
        company_profile = f"""# {company_name} - Perfil da Empresa

## 📋 Informações Gerais
- **Nome**: {company_name}
- **Setor**: {self.company_info['industry'].replace('_', ' ').title()}
- **Descrição**: {self.company_info['description']}
- **Data de Criação**: {datetime.now().strftime('%d/%m/%Y')}
- **Pasta do Projeto**: {self.project_path}

## 👥 Estrutura Organizacional
- **CEO**: 1 persona
- **EXECUTIVOS**: 3 personas  
- **ASSISTENTES**: 3 personas
- **ESPECIALISTAS**: 3 personas
- **SUPORTE**: 6 personas
- **TOTAL**: 16 personas

## 📁 Estrutura de Arquivos
```
{company_name}_virtual_company/
├── config/                    (configurações)
├── personas/                  (16 personas organizadas)
├── workflows/                 (fluxos de trabalho)
├── docs/                      (documentação)
└── logs/                      (registros)
```

## 🎯 Próximos Passos
1. Revisar personas criadas em `personas/`
2. Configurar workflows específicos em `workflows/`
3. Personalizar documentação em `docs/`
4. Implementar integrações necessárias
"""
        
        profile_file = company_folder / "docs" / "EMPRESA_PROFILE.md"
        with open(profile_file, 'w', encoding='utf-8') as f:
            f.write(company_profile)
        
        # 5. Log de criação
        log_entry = {
            "action": "company_creation",
            "company": company_name,
            "project_path": str(self.project_path),
            "company_folder": str(company_folder),
            "personas_created": 16,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        log_file = company_folder / "logs" / f"creation_log_{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)
        
        return company_folder

    def generate_company(self):
        """Processo principal de geração da empresa"""
        try:
            print(f"🚀 Iniciando geração de empresa virtual...")
            print(f"📍 Local: {self.project_path}")
            
            # 1. Coleta informações
            if not self.collect_company_info():
                return False
            
            # 2. Gera personas
            print("\n👥 Gerando 16 personas...")
            personas = self.generate_personas()
            
            # 3. Cria estrutura
            print("\n📁 Criando estrutura de arquivos...")
            company_folder = self.create_folder_structure(personas)
            
            # 4. Sucesso
            print("\n" + "=" * 60)
            print("✅ EMPRESA VIRTUAL CRIADA COM SUCESSO!")
            print("=" * 60)
            print(f"📊 Empresa: {self.company_info['name']}")
            print(f"🏭 Setor: {self.company_info['industry']}")
            print(f"👥 Personas: 16 criadas")
            print(f"📁 Local: {company_folder}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Erro durante criação: {str(e)}")
            return False

def main():
    """Função principal"""
    # Pode receber caminho do projeto como argumento
    project_path = None
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    
    # Cria o gerador
    generator = VirtualCompanyGenerator(project_path)
    
    # Gera a empresa
    generator.generate_company()

if __name__ == "__main__":
    main()