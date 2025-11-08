#!/usr/bin/env python3
"""
📚 SCRIPT 3 - GERADOR DE RAG PERSONALIZADO
===========================================

Gera bases de conhecimento RAG personalizadas baseadas em bio, competências e tech specs.

Input: bio/ + competencias/ + tech_specs/
Output: rag/ (knowledge base personalizada)

Versão: 1.0.0
Autor: Sergio Castro
Data: November 2025
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class RAGGenerator:
    def __init__(self, base_path: str = None):
        """Inicializar gerador de RAG"""
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent
        
        self.personas_path = self.base_path / "04_PERSONAS_COMPLETAS"
        
        # Templates de knowledge base por área de especialização
        self.knowledge_templates = {
            "nutrição": {
                "core_topics": [
                    "Carnivore Diet Fundamentals",
                    "Nutritional Analysis",
                    "Meal Planning Strategies",
                    "Macronutrient Balance",
                    "Health Benefits Research",
                    "Common Deficiencies Prevention",
                    "Meal Timing Optimization"
                ],
                "procedures": [
                    "Nutritional Assessment Protocol",
                    "Meal Plan Creation Steps",
                    "Client Consultation Guidelines",
                    "Progress Monitoring Methods"
                ],
                "tools_knowledge": [
                    "Food tracking applications",
                    "Nutritional databases",
                    "Meal planning software",
                    "Health monitoring devices"
                ]
            },
            "marketing": {
                "core_topics": [
                    "Digital Marketing Strategy",
                    "Social Media Best Practices",
                    "Content Creation Guidelines",
                    "Brand Voice and Messaging",
                    "Campaign Performance Metrics",
                    "Audience Segmentation",
                    "Growth Hacking Techniques"
                ],
                "procedures": [
                    "Campaign Planning Process",
                    "Content Approval Workflow",
                    "Social Media Posting Schedule",
                    "Performance Analysis Methods"
                ],
                "tools_knowledge": [
                    "Social media management platforms",
                    "Analytics and tracking tools",
                    "Design and content creation software",
                    "Marketing automation systems"
                ]
            },
            "youtube": {
                "core_topics": [
                    "YouTube Algorithm Optimization",
                    "Video Content Strategy",
                    "Engagement Techniques",
                    "SEO for YouTube",
                    "Thumbnail and Title Optimization",
                    "Community Building",
                    "Monetization Strategies"
                ],
                "procedures": [
                    "Video Production Workflow",
                    "Content Planning Calendar",
                    "Publishing and Promotion Process",
                    "Analytics Review Protocol"
                ],
                "tools_knowledge": [
                    "Video editing software",
                    "YouTube Studio features",
                    "SEO optimization tools",
                    "Analytics platforms"
                ]
            },
            "assistente": {
                "core_topics": [
                    "Executive Support Best Practices",
                    "Communication Protocols",
                    "Task Prioritization Methods",
                    "Client Relationship Management",
                    "Documentation Standards",
                    "Meeting Coordination",
                    "Follow-up Procedures"
                ],
                "procedures": [
                    "Task Management Workflow",
                    "Client Communication Guidelines",
                    "Escalation Procedures",
                    "Information Organization Methods"
                ],
                "tools_knowledge": [
                    "Calendar management systems",
                    "Communication platforms",
                    "Document management tools",
                    "Task tracking applications"
                ]
            },
            "executivo": {
                "core_topics": [
                    "Strategic Planning",
                    "Team Leadership",
                    "Decision Making Frameworks",
                    "Performance Management",
                    "Stakeholder Communication",
                    "Business Development",
                    "Market Analysis"
                ],
                "procedures": [
                    "Strategic Planning Process",
                    "Team Performance Reviews",
                    "Client Relationship Management",
                    "Business Growth Strategies"
                ],
                "tools_knowledge": [
                    "Business intelligence platforms",
                    "CRM systems",
                    "Project management tools",
                    "Analytics dashboards"
                ]
            },
            "suporte": {
                "core_topics": [
                    "Customer Service Excellence",
                    "Problem Resolution Techniques",
                    "Communication Best Practices",
                    "Knowledge Base Management",
                    "Escalation Guidelines",
                    "Quality Assurance",
                    "Customer Satisfaction"
                ],
                "procedures": [
                    "Ticket Resolution Workflow",
                    "Customer Interaction Guidelines",
                    "Quality Control Process",
                    "Knowledge Base Updates"
                ],
                "tools_knowledge": [
                    "Help desk software",
                    "Communication channels",
                    "Knowledge management systems",
                    "Customer feedback tools"
                ]
            }
        }
        
        # Knowledge base geral da empresa
        self.company_knowledge = {
            "carntrack_fundamentals": [
                "CarnTrack Mission and Vision",
                "Carnivore Diet Philosophy",
                "Target Audience Characteristics",
                "Health Benefits Documentation",
                "Scientific Research Base",
                "Success Stories and Testimonials"
            ],
            "products_services": [
                "Daily Food and Health Tracking",
                "Personalized Meal Plans",
                "Daily Metabolic Control",
                "Scheduled Fasts and Alerts",
                "Physical Activity Monitoring"
            ],
            "policies_procedures": [
                "Customer Privacy Policy",
                "Data Security Guidelines",
                "Communication Standards",
                "Quality Assurance Procedures",
                "Escalation Protocols"
            ]
        }
    
    def load_persona_data(self, persona_path: Path) -> Dict:
        """Carregar todos os dados da persona"""
        data = {
            "bio_info": {},
            "competencias": {},
            "tech_specs": {},
            "persona_name": persona_path.name
        }
        
        # Carregar biografia
        bio_files = list(persona_path.glob("*_bio.md"))
        if bio_files:
            with open(bio_files[0], 'r', encoding='utf-8') as f:
                bio_content = f.read()
                data["bio_info"] = self.extract_bio_info(bio_content)
        
        # Carregar competências
        comp_file = persona_path / "competencias" / "competencias_core.json"
        if comp_file.exists():
            with open(comp_file, 'r', encoding='utf-8') as f:
                data["competencias"] = json.load(f)
        
        # Carregar tech specs
        ai_config_file = persona_path / "tech_specs" / "ai_config.json"
        tools_config_file = persona_path / "tech_specs" / "tools_config.json"
        
        if ai_config_file.exists():
            with open(ai_config_file, 'r', encoding='utf-8') as f:
                data["tech_specs"]["ai_config"] = json.load(f)
        
        if tools_config_file.exists():
            with open(tools_config_file, 'r', encoding='utf-8') as f:
                data["tech_specs"]["tools_config"] = json.load(f)
        
        return data
    
    def extract_bio_info(self, bio_content: str) -> Dict:
        """Extrair informações da biografia"""
        info = {}
        
        # Extrair especialização
        espec_match = re.search(r'\*\*Especialização:\*\*\s*(.+)', bio_content)
        if espec_match:
            info["especializacao"] = espec_match.group(1).strip()
        
        # Extrair idiomas
        idiomas_match = re.search(r'\*\*Idiomas:\*\*\s*(.+)', bio_content)
        if idiomas_match:
            info["idiomas"] = idiomas_match.group(1).strip()
        
        return info
    
    def determine_specialization_area(self, persona_data: Dict) -> str:
        """Determinar área de especialização baseada nos dados"""
        
        # Verificar especialização na bio
        especializacao = persona_data.get("bio_info", {}).get("especializacao", "").lower()
        
        if "nutrição" in especializacao or "nutrition" in especializacao:
            return "nutrição"
        elif "marketing" in especializacao or "social" in especializacao:
            return "marketing"
        elif "youtube" in especializacao or "video" in especializacao:
            return "youtube"
        
        # Verificar competências
        competencias = persona_data.get("competencias", {}).get("competencias", {})
        all_comps = []
        
        for comp_type in ["competencias_tecnicas", "competencias_personalizadas"]:
            if comp_type in competencias:
                all_comps.extend(competencias[comp_type])
        
        comp_text = " ".join(all_comps).lower()
        
        if "nutrição" in comp_text or "nutricional" in comp_text:
            return "nutrição"
        elif "marketing" in comp_text or "redes sociais" in comp_text:
            return "marketing"
        elif "youtube" in comp_text or "vídeo" in comp_text:
            return "youtube"
        
        # Determinar por role type
        role_type = persona_data.get("competencias", {}).get("persona_info", {}).get("role_type", "")
        
        if role_type == "assistente":
            return "assistente"
        elif role_type == "executivo":
            return "executivo"
        elif role_type == "suporte":
            return "suporte"
        
        return "assistente"  # default
    
    def generate_knowledge_base(self, persona_data: Dict, specialization: str) -> Dict:
        """Gerar base de conhecimento personalizada"""
        
        # Template base da especialização
        spec_template = self.knowledge_templates.get(specialization, self.knowledge_templates["assistente"])
        
        knowledge_base = {
            "core_knowledge": {
                "company_fundamentals": self.company_knowledge["carntrack_fundamentals"],
                "products_services": self.company_knowledge["products_services"],
                "specialization_topics": spec_template["core_topics"]
            },
            "procedures": {
                "company_policies": self.company_knowledge["policies_procedures"],
                "role_procedures": spec_template["procedures"]
            },
            "tools_and_systems": {
                "specialization_tools": spec_template["tools_knowledge"],
                "available_tools": self.extract_available_tools(persona_data)
            },
            "access_configuration": self.generate_access_config(persona_data, specialization),
            "personalization": self.generate_personalization(persona_data, specialization)
        }
        
        return knowledge_base
    
    def extract_available_tools(self, persona_data: Dict) -> List[str]:
        """Extrair ferramentas disponíveis das tech specs"""
        
        ai_config = persona_data.get("tech_specs", {}).get("ai_config", {})
        ai_configuration = ai_config.get("ai_configuration", {})
        
        return ai_configuration.get("tools_available", [])
    
    def generate_access_config(self, persona_data: Dict, specialization: str) -> Dict:
        """Gerar configuração de acesso ao RAG"""
        
        tools_config = persona_data.get("tech_specs", {}).get("tools_config", {})
        rag_access = tools_config.get("rag_access_level", {})
        
        return {
            "access_level": rag_access.get("level", "basic"),
            "priority": rag_access.get("priority", "medium"),
            "categories": rag_access.get("categories", ["general"]),
            "specialization_focus": specialization,
            "contextual_search": True,
            "cross_reference": True
        }
    
    def generate_personalization(self, persona_data: Dict, specialization: str) -> Dict:
        """Gerar personalização baseada no perfil"""
        
        bio_info = persona_data.get("bio_info", {})
        competencias = persona_data.get("competencias", {})
        
        return {
            "language_preferences": self.extract_language_preferences(bio_info),
            "expertise_level": self.determine_expertise_level(competencias, specialization),
            "communication_style": self.determine_communication_style(persona_data),
            "focus_areas": self.extract_focus_areas(competencias),
            "learning_preferences": self.determine_learning_preferences(specialization)
        }
    
    def extract_language_preferences(self, bio_info: Dict) -> List[str]:
        """Extrair preferências de idioma"""
        
        idiomas = bio_info.get("idiomas", "")
        if not idiomas:
            return ["português", "inglês"]
        
        languages = []
        if "espanhol" in idiomas.lower() or "spanish" in idiomas.lower():
            languages.append("espanhol")
        if "inglês" in idiomas.lower() or "english" in idiomas.lower():
            languages.append("inglês")
        if "português" in idiomas.lower() or "portuguese" in idiomas.lower():
            languages.append("português")
        if "francês" in idiomas.lower() or "french" in idiomas.lower():
            languages.append("francês")
        
        return languages if languages else ["português", "inglês"]
    
    def determine_expertise_level(self, competencias: Dict, specialization: str) -> str:
        """Determinar nível de expertise"""
        
        comp_data = competencias.get("competencias", {})
        total_comps = len(comp_data.get("competencias_tecnicas", []))
        personalized_comps = len(comp_data.get("competencias_personalizadas", []))
        
        if personalized_comps > 3 and total_comps > 5:
            return "expert"
        elif personalized_comps > 1 and total_comps > 3:
            return "advanced"
        else:
            return "intermediate"
    
    def determine_communication_style(self, persona_data: Dict) -> str:
        """Determinar estilo de comunicação"""
        
        role_type = persona_data.get("competencias", {}).get("persona_info", {}).get("role_type", "")
        
        if role_type == "executivo":
            return "strategic_focused"
        elif role_type == "especialista":
            return "technical_detailed"
        elif role_type == "gestor":
            return "leadership_oriented"
        elif role_type == "suporte":
            return "customer_friendly"
        else:
            return "collaborative_supportive"
    
    def extract_focus_areas(self, competencias: Dict) -> List[str]:
        """Extrair áreas de foco das competências"""
        
        comp_data = competencias.get("competencias", {})
        focus_areas = []
        
        # Analisar competências personalizadas
        personalized = comp_data.get("competencias_personalizadas", [])
        for comp in personalized:
            comp_lower = comp.lower()
            if "nutrição" in comp_lower:
                focus_areas.append("nutrition_expertise")
            elif "marketing" in comp_lower:
                focus_areas.append("marketing_strategy")
            elif "youtube" in comp_lower or "vídeo" in comp_lower:
                focus_areas.append("content_creation")
            elif "multilíngue" in comp_lower or "comunicação" in comp_lower:
                focus_areas.append("multilingual_communication")
        
        return focus_areas if focus_areas else ["general_support"]
    
    def determine_learning_preferences(self, specialization: str) -> Dict:
        """Determinar preferências de aprendizado"""
        
        preferences = {
            "nutrição": {
                "content_types": ["research_papers", "case_studies", "practical_guides"],
                "update_frequency": "weekly",
                "depth_level": "detailed"
            },
            "marketing": {
                "content_types": ["trend_analysis", "best_practices", "campaign_examples"],
                "update_frequency": "daily",
                "depth_level": "strategic"
            },
            "youtube": {
                "content_types": ["algorithm_updates", "creator_tips", "trend_analysis"],
                "update_frequency": "daily",
                "depth_level": "practical"
            },
            "assistente": {
                "content_types": ["procedures", "templates", "best_practices"],
                "update_frequency": "monthly",
                "depth_level": "procedural"
            },
            "executivo": {
                "content_types": ["strategic_insights", "market_data", "leadership_guides"],
                "update_frequency": "weekly",
                "depth_level": "strategic"
            },
            "suporte": {
                "content_types": ["faqs", "troubleshooting", "customer_scenarios"],
                "update_frequency": "weekly",
                "depth_level": "practical"
            }
        }
        
        return preferences.get(specialization, preferences["assistente"])
    
    def create_rag_structure(self, persona_path: Path) -> bool:
        """Criar estrutura RAG para uma persona"""
        
        # Verificar dependências
        if not (persona_path / "tech_specs").exists():
            print(f"❌ Tech Specs não encontradas em {persona_path}")
            return False
        
        # Carregar dados
        persona_data = self.load_persona_data(persona_path)
        specialization = self.determine_specialization_area(persona_data)
        
        # Gerar knowledge base
        knowledge_base = self.generate_knowledge_base(persona_data, specialization)
        
        # Criar pasta rag
        rag_path = persona_path / "rag"
        rag_path.mkdir(exist_ok=True)
        
        # Salvar knowledge base principal
        kb_file = rag_path / "knowledge_base.json"
        with open(kb_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "persona_name": persona_data["persona_name"],
                    "specialization": specialization,
                    "generated_at": datetime.now().isoformat(),
                    "script_version": "3.0.0"
                },
                "knowledge_base": knowledge_base
            }, f, indent=2, ensure_ascii=False)
        
        # Salvar regras de contexto
        context_rules = self.generate_context_rules(persona_data, specialization, knowledge_base)
        rules_file = rag_path / "context_rules.md"
        with open(rules_file, 'w', encoding='utf-8') as f:
            f.write(context_rules)
        
        # Salvar configuração de busca
        search_config = self.generate_search_config(persona_data, specialization)
        search_file = rag_path / "search_config.json"
        with open(search_file, 'w', encoding='utf-8') as f:
            json.dump(search_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ RAG gerado para {persona_data['persona_name']} (especialização: {specialization})")
        print(f"   📚 {kb_file}")
        print(f"   📋 {rules_file}")
        print(f"   🔍 {search_file}")
        
        return True
    
    def generate_context_rules(self, persona_data: Dict, specialization: str, knowledge_base: Dict) -> str:
        """Gerar regras de contexto em MD"""
        
        persona_name = persona_data["persona_name"]
        access_config = knowledge_base["access_configuration"]
        personalization = knowledge_base["personalization"]
        
        rules_content = f"""# 📋 REGRAS DE CONTEXTO RAG - {persona_name.upper().replace('_', ' ')}

> *Gerado automaticamente pelo Script 3 - Generate RAG*

## 🎯 **CONFIGURAÇÃO DE ACESSO**

- **Nível de Acesso:** {access_config['access_level']}
- **Prioridade:** {access_config['priority']}
- **Especialização:** {specialization}
- **Busca Contextual:** {'Ativa' if access_config['contextual_search'] else 'Desativa'}
- **Referência Cruzada:** {'Ativa' if access_config['cross_reference'] else 'Desativa'}

### **Categorias Permitidas:**
"""
        
        for cat in access_config['categories']:
            rules_content += f"- {cat}\n"
        
        rules_content += f"""
## 🗣️ **PERSONALIZAÇÃO**

### **Preferências de Idioma:**
"""
        
        for lang in personalization['language_preferences']:
            rules_content += f"- {lang}\n"
        
        rules_content += f"""
### **Perfil de Expertise:**
- **Nível:** {personalization['expertise_level']}
- **Estilo de Comunicação:** {personalization['communication_style']}

### **Áreas de Foco:**
"""
        
        for area in personalization['focus_areas']:
            rules_content += f"- {area}\n"
        
        learning_prefs = personalization['learning_preferences']
        rules_content += f"""
### **Preferências de Aprendizado:**
- **Tipos de Conteúdo:** {', '.join(learning_prefs['content_types'])}
- **Frequência de Atualização:** {learning_prefs['update_frequency']}
- **Nível de Detalhamento:** {learning_prefs['depth_level']}

## 🔍 **REGRAS DE BUSCA**

### **Priorização de Resultados:**
1. **Especialização específica** ({specialization})
2. **Conhecimento da empresa** (CarnTrack)
3. **Procedimentos do role** ({persona_data.get('competencias', {}).get('persona_info', {}).get('role_type', 'N/A')})
4. **Conhecimento geral**

### **Filtros Aplicados:**
- Relevância mínima: 70%
- Máximo de resultados: 10
- Priorizar conteúdo atualizado
- Incluir contexto relacionado

### **Exclusões:**
- Conteúdo de outras especializações não relacionadas
- Informações confidenciais fora do escopo
- Dados desatualizados (>6 meses para {specialization})

## 🎯 **CONTEXTO DE RESPOSTA**

### **Sempre Incluir:**
- Fundamentais da CarnTrack
- Procedimentos específicos do role
- Melhores práticas da especialização

### **Adaptar Baseado em:**
- Nível de expertise da persona
- Preferências de idioma
- Estilo de comunicação
- Áreas de foco específicas

---

*Arquivo gerado pelo Virtual Company Generator Master v2.0.0*  
📅 **Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
🔄 **Script:** 3 - Generate RAG v1.0.0
"""
        
        return rules_content
    
    def generate_search_config(self, persona_data: Dict, specialization: str) -> Dict:
        """Gerar configuração de busca"""
        
        return {
            "search_parameters": {
                "relevance_threshold": 0.7,
                "max_results": 10,
                "include_related": True,
                "boost_specialization": 2.0,
                "boost_company_knowledge": 1.5
            },
            "filters": {
                "specialization": specialization,
                "role_type": persona_data.get("competencias", {}).get("persona_info", {}).get("role_type", ""),
                "language_preferences": persona_data.get("bio_info", {}).get("idiomas", "").split(","),
                "expertise_level": "auto_detect"
            },
            "ranking_factors": [
                {"factor": "specialization_match", "weight": 0.4},
                {"factor": "company_relevance", "weight": 0.3},
                {"factor": "role_relevance", "weight": 0.2},
                {"factor": "recency", "weight": 0.1}
            ],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "persona_name": persona_data["persona_name"],
                "specialization": specialization
            }
        }
    
    def process_all_personas(self) -> Dict:
        """Processar todas as personas"""
        
        print("\n" + "="*60)
        print("📚 SCRIPT 3 - GERADOR DE RAG PERSONALIZADO")
        print("="*60)
        print(f"📍 Base: {self.base_path}")
        print(f"👥 Personas: {self.personas_path}")
        
        results = {
            "processed": [],
            "failed": [],
            "total": 0,
            "specializations": {}
        }
        
        # Buscar todas as pastas de personas
        for role_folder in self.personas_path.iterdir():
            if role_folder.is_dir():
                print(f"\n📁 Processando {role_folder.name}...")
                
                for persona_folder in role_folder.iterdir():
                    if persona_folder.is_dir():
                        results["total"] += 1
                        
                        if self.create_rag_structure(persona_folder):
                            results["processed"].append(str(persona_folder))
                            
                            # Contar especializações
                            persona_data = self.load_persona_data(persona_folder)
                            spec = self.determine_specialization_area(persona_data)
                            results["specializations"][spec] = results["specializations"].get(spec, 0) + 1
                        else:
                            results["failed"].append(str(persona_folder))
        
        # Relatório final
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO FINAL")
        print(f"{'='*60}")
        print(f"✅ Processadas: {len(results['processed'])}")
        print(f"❌ Falharam: {len(results['failed'])}")
        print(f"📊 Total: {results['total']}")
        
        print(f"\n📈 Especializações Detectadas:")
        for spec, count in results["specializations"].items():
            print(f"   • {spec}: {count} persona(s)")
        
        if results["failed"]:
            print(f"\n❌ Falhas:")
            for failed in results["failed"]:
                print(f"   - {failed}")
        
        return results


def main():
    """Função principal"""
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = None
    
    # Executar gerador
    generator = RAGGenerator(base_path)
    results = generator.process_all_personas()
    
    # Exit code baseado no resultado
    if results["failed"]:
        sys.exit(1)
    else:
        print(f"\n🎉 SCRIPT 3 CONCLUÍDO COM SUCESSO!")
        print(f"📚 {len(results['processed'])} bases de conhecimento RAG criadas!")
        sys.exit(0)


if __name__ == "__main__":
    main()