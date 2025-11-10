#!/usr/bin/env python3
"""
⚙️ SCRIPT 2 - GERADOR DE ESPECIFICAÇÕES TÉCNICAS DAS PERSONAS
=============================================================

Gera especificações técnicas de IA para cada persona baseadas em:
- Biografias completas das personas
- Competências e habilidades
- Perfil de responsabilidades

OBJETIVO: Criar configurações técnicas de IA (modelos, parâmetros, ferramentas)
         para cada persona funcionar de forma otimizada

Input: 
- bio/ (biografias das personas)
- competencias/ (habilidades e competências) 
Output: 
- tech_specs/ (configurações técnicas de IA)

Versão: 2.0.0
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

class TechSpecsGenerator:
    def __init__(self, base_path: str = None):
        """Inicializar gerador de tech specs"""
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent
        
        self.personas_path = self.base_path / "04_PERSONAS_COMPLETAS"
        
        # Templates de configurações por role type
        self.ai_configs_templates = {
            "assistente": {
                "ai_model": "gpt-4-turbo-preview",
                "max_tokens": 1500,
                "temperature": 0.6,
                "response_format": "structured",
                "priority_level": "medium",
                "decision_authority": "operational",
                "access_scope": "assigned_executive",
                "base_tools": [
                    "email",
                    "calendar", 
                    "supabase",
                    "n8n_webhooks",
                    "scheduling",
                    "documentation",
                    "follow_up"
                ]
            },
            "executivo": {
                "ai_model": "gpt-4-turbo-preview",
                "max_tokens": 2000,
                "temperature": 0.7,
                "response_format": "structured",
                "priority_level": "high",
                "decision_authority": "department",
                "access_scope": "department_systems",
                "base_tools": [
                    "email",
                    "calendar",
                    "supabase", 
                    "n8n_webhooks",
                    "crm",
                    "proposals",
                    "client_portal",
                    "analytics"
                ]
            },
            "especialista": {
                "ai_model": "gpt-4-turbo-preview",
                "max_tokens": 2000,
                "temperature": 0.7,
                "response_format": "structured",
                "priority_level": "high",
                "decision_authority": "technical",
                "access_scope": "specialization_area",
                "base_tools": [
                    "email",
                    "calendar",
                    "supabase",
                    "n8n_webhooks", 
                    "technical_tools",
                    "analysis",
                    "reporting"
                ]
            },
            "gestor": {
                "ai_model": "gpt-4-turbo-preview",
                "max_tokens": 2500,
                "temperature": 0.8,
                "response_format": "structured",
                "priority_level": "maximum",
                "decision_authority": "full",
                "access_scope": "all_systems",
                "base_tools": [
                    "email",
                    "calendar",
                    "supabase",
                    "n8n_webhooks",
                    "admin_panel",
                    "reporting",
                    "analytics",
                    "strategic_tools"
                ]
            },
            "suporte": {
                "ai_model": "gpt-4-turbo-preview",
                "max_tokens": 1200,
                "temperature": 0.5,
                "response_format": "structured",
                "priority_level": "medium",
                "decision_authority": "routing",
                "access_scope": "customer_facing",
                "base_tools": [
                    "email",
                    "calendar",
                    "supabase",
                    "n8n_webhooks",
                    "helpdesk",
                    "chat",
                    "routing",
                    "knowledge_base"
                ]
            }
        }
        
        # Mapeamento de competências para ferramentas específicas
        self.competencia_to_tools = {
            "nutrição": ["nutrition_analysis", "meal_planning"],
            "marketing": ["social_media_tools", "campaign_management", "analytics_platforms"],
            "youtube": ["video_editing_tools", "youtube_studio", "seo_tools"],
            "design": ["design_tools", "graphic_software"],
            "analytics": ["data_analysis", "reporting_tools", "bi_platforms"],
            "comunicação": ["communication_tools", "translation_services"],
            "vendas": ["crm_advanced", "sales_pipeline", "proposal_tools"],
            "multilíngue": ["translation_tools", "language_services"],
            "programação": ["development_tools", "code_analysis"],
            "financeiro": ["financial_tools", "accounting_software"]
        }
        
    def load_persona_data(self, persona_path: Path) -> Dict:
        """Carregar dados da biografia e competências"""
        data = {
            "bio_info": {},
            "competencias": {},
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
        
        # Extrair idade
        idade_match = re.search(r'\*\*Idade[^:]*:\*\*\s*(.+)', bio_content)
        if idade_match:
            info["idade"] = idade_match.group(1).strip()
            
        return info
    
    def determine_role_type(self, persona_path: Path) -> str:
        """Determinar tipo de role baseado no caminho"""
        path_str = str(persona_path)
        
        if "assistente" in path_str:
            return "assistente"
        elif "executivo" in path_str:
            return "executivo"
        elif "especialista" in path_str:
            return "especialista" 
        elif "gestor" in path_str:
            return "gestor"
        elif "suporte" in path_str:
            return "suporte"
        else:
            return "assistente"  # default
    
    def generate_ai_config(self, persona_data: Dict, role_type: str) -> Dict:
        """Gerar configuração de IA baseada nos dados da persona"""
        
        # Template base
        base_config = self.ai_configs_templates[role_type].copy()
        
        # Personalizar baseado nas competências
        competencias = persona_data.get("competencias", {}).get("competencias", {})
        tools = base_config["base_tools"].copy()
        
        # Adicionar ferramentas específicas baseadas nas competências
        all_competencias = []
        if "competencias_tecnicas" in competencias:
            all_competencias.extend(competencias["competencias_tecnicas"])
        if "competencias_personalizadas" in competencias:
            all_competencias.extend(competencias["competencias_personalizadas"])
        
        # Mapear competências para ferramentas
        for comp in all_competencias:
            comp_lower = comp.lower()
            for key, tools_list in self.competencia_to_tools.items():
                if key in comp_lower:
                    tools.extend(tools_list)
        
        # Remover duplicatas
        tools = list(set(tools))
        
        # Ajustar parâmetros baseado no perfil
        bio_info = persona_data.get("bio_info", {})
        especializacao = bio_info.get("especializacao", "").lower()
        
        # Ajustes específicos
        if "youtube" in especializacao or "marketing" in especializacao:
            base_config["temperature"] = 0.8  # Mais criativo
        
        if "multilíngue" in especializacao or len(bio_info.get("idiomas", "").split(",")) > 2:
            tools.append("translation_services")
        
        # Configuração final
        ai_config = {
            "ai_model": base_config["ai_model"],
            "max_tokens": base_config["max_tokens"],
            "temperature": base_config["temperature"],
            "response_format": base_config["response_format"],
            "tools_available": sorted(tools),
            "priority_level": base_config["priority_level"],
            "decision_authority": base_config["decision_authority"],
            "access_scope": base_config["access_scope"]
        }
        
        # Adicionar expertise_area para especialistas
        if role_type == "especialista":
            ai_config["expertise_area"] = bio_info.get("especializacao", "General Expertise")
        elif role_type == "executivo":
            ai_config["specialization_focus"] = bio_info.get("especializacao", "General Executive")
        
        return ai_config
    
    def generate_communication_config(self, persona_data: Dict, role_type: str) -> Dict:
        """Gerar configuração de comunicação"""
        
        base_configs = {
            "assistente": {
                "can_send_ci": True,
                "can_receive_ci": True,
                "default_priority": "normal",
                "auto_response": False,
                "escalation_rules": ["beyond_authority", "technical_issues"],
                "can_send_to": ["executivo_assigned", "especialistas", "suporte"],
                "receives_from": ["executivo_assigned", "clientes"]
            },
            "executivo": {
                "can_send_ci": True,
                "can_receive_ci": True,
                "default_priority": "normal",
                "auto_response": False,
                "escalation_rules": ["complex_cases", "client_complaints"],
                "can_send_to": ["gestor", "assistentes", "especialistas", "suporte"],
                "receives_from": ["gestor", "assistentes", "clientes"]
            },
            "especialista": {
                "can_send_ci": True,
                "can_receive_ci": True,
                "default_priority": "normal",
                "auto_response": False,
                "escalation_rules": ["resource_constraints", "policy_conflicts"],
                "can_send_to": ["gestor", "executivos", "assistentes"],
                "receives_from": ["all_internal"]
            },
            "gestor": {
                "can_send_ci": True,
                "can_receive_ci": True,
                "default_priority": "high",
                "auto_response": False,
                "escalation_rules": [],
                "can_send_to": ["all_internal"],
                "receives_from": ["all_internal", "stakeholders"]
            },
            "suporte": {
                "can_send_ci": True,
                "can_receive_ci": True,
                "default_priority": "normal",
                "auto_response": False,
                "escalation_rules": ["unresolved_issues", "vip_clients"],
                "can_send_to": ["all_internal"],
                "receives_from": ["clientes", "externos"]
            }
        }
        
        return base_configs.get(role_type, base_configs["assistente"])
    
    def generate_rag_config(self, persona_data: Dict, role_type: str) -> Dict:
        """Gerar configuração de acesso ao RAG"""
        
        configs = {
            "assistente": {
                "level": "operational",
                "categories": ["procedures", "executive_specialization"],
                "priority": "medium"
            },
            "executivo": {
                "level": "strategic",
                "categories": ["strategic", "own_department", "market_data"],
                "priority": "high"
            },
            "especialista": {
                "level": "technical", 
                "categories": ["technical", "own_area", "procedures"],
                "priority": "high"
            },
            "gestor": {
                "level": "full",
                "categories": ["all"],
                "priority": "maximum"
            },
            "suporte": {
                "level": "basic",
                "categories": ["procedures", "faqs", "general"],
                "priority": "low"
            }
        }
        
        return configs.get(role_type, configs["assistente"])
    
    def create_tech_specs_structure(self, persona_path: Path) -> bool:
        """Criar estrutura de tech specs para uma persona"""
        
        # Verificar dependências
        if not (persona_path / "competencias").exists():
            print(f"❌ Competências não encontradas em {persona_path}")
            return False
        
        # Carregar dados
        persona_data = self.load_persona_data(persona_path)
        role_type = self.determine_role_type(persona_path)
        
        # Gerar configurações
        ai_config = self.generate_ai_config(persona_data, role_type)
        comm_config = self.generate_communication_config(persona_data, role_type)
        rag_config = self.generate_rag_config(persona_data, role_type)
        
        # Criar pasta tech_specs
        tech_path = persona_path / "tech_specs"
        tech_path.mkdir(exist_ok=True)
        
        # Salvar configuração de IA
        ai_file = tech_path / "ai_config.json"
        with open(ai_file, 'w', encoding='utf-8') as f:
            json.dump({
                "metadata": {
                    "persona_name": persona_data["persona_name"],
                    "role_type": role_type,
                    "generated_at": datetime.now().isoformat(),
                    "script_version": "2.0.0"
                },
                "ai_configuration": ai_config
            }, f, indent=2, ensure_ascii=False)
        
        # Salvar configuração de ferramentas
        tools_config = {
            "communication_settings": comm_config,
            "rag_access_level": rag_config,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "based_on_competencias": True
            }
        }
        
        tools_file = tech_path / "tools_config.json"
        with open(tools_file, 'w', encoding='utf-8') as f:
            json.dump(tools_config, f, indent=2, ensure_ascii=False)
        
        # Criar documentação MD
        md_content = self.generate_tech_specs_md(persona_data, role_type, ai_config, comm_config, rag_config)
        md_file = tech_path / "tech_specs_completas.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Tech Specs geradas para {persona_data['persona_name']}")
        print(f"   🤖 {ai_file}")
        print(f"   🔧 {tools_file}")
        print(f"   📋 {md_file}")
        
        return True
    
    def generate_tech_specs_md(self, persona_data: Dict, role_type: str, ai_config: Dict, comm_config: Dict, rag_config: Dict) -> str:
        """Gerar documentação MD das tech specs"""
        
        persona_name = persona_data["persona_name"]
        
        md_content = f"""# ⚙️ TECH SPECS - {persona_name.upper().replace('_', ' ')}

> *Gerado automaticamente pelo Script 2 - Generate Tech Specs*

## 📋 **INFORMAÇÕES BÁSICAS**

- **Persona:** {persona_name}
- **Role Type:** {role_type.title()}
- **Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Baseado em:** Biografia + Competências

## 🤖 **CONFIGURAÇÕES DE IA**

### **Modelo e Parâmetros:**
- **AI Model:** {ai_config['ai_model']}
- **Max Tokens:** {ai_config['max_tokens']}
- **Temperature:** {ai_config['temperature']}
- **Response Format:** {ai_config['response_format']}

### **Autoridade e Acesso:**
- **Priority Level:** {ai_config['priority_level']}
- **Decision Authority:** {ai_config['decision_authority']}
- **Access Scope:** {ai_config['access_scope']}

### **Ferramentas Disponíveis:**
"""
        
        for i, tool in enumerate(ai_config['tools_available'], 1):
            md_content += f"{i}. `{tool}`\n"
        
        md_content += f"""
## 📧 **CONFIGURAÇÕES DE COMUNICAÇÃO**

### **Permissões:**
- **Pode Enviar CI:** {'Sim' if comm_config['can_send_ci'] else 'Não'}
- **Pode Receber CI:** {'Sim' if comm_config['can_receive_ci'] else 'Não'}
- **Prioridade Padrão:** {comm_config['default_priority']}
- **Auto Response:** {'Ativo' if comm_config['auto_response'] else 'Desativo'}

### **Regras de Escalação:**
"""
        
        for rule in comm_config['escalation_rules']:
            md_content += f"- {rule}\n"
        
        md_content += f"""
### **Comunicação Permitida:**
**Pode Enviar Para:**
"""
        
        for dest in comm_config['can_send_to']:
            md_content += f"- {dest}\n"
        
        md_content += f"""
**Recebe De:**
"""
        
        for source in comm_config['receives_from']:
            md_content += f"- {source}\n"
        
        md_content += f"""
## 📚 **ACESSO AO RAG**

- **Nível:** {rag_config['level']}
- **Prioridade:** {rag_config['priority']}

### **Categorias de Acesso:**
"""
        
        for cat in rag_config['categories']:
            md_content += f"- {cat}\n"
        
        md_content += f"""
## 📊 **RESUMO TÉCNICO**

- **Total de Ferramentas:** {len(ai_config['tools_available'])}
- **Nível de Acesso:** {ai_config['access_scope']}
- **Autoridade de Decisão:** {ai_config['decision_authority']}
- **Complexidade:** {'Alta' if ai_config['max_tokens'] > 2000 else 'Média' if ai_config['max_tokens'] > 1500 else 'Básica'}

## 🔄 **PRÓXIMOS PASSOS**

1. **Script 3:** Gerar RAG personalizado baseado nestas specs
2. **Script 4:** Desenvolver workflows específicos
3. **Implementação:** Deploy das configurações

---

*Arquivo gerado pelo Virtual Company Generator Master v2.0.0*  
📅 **Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
🔄 **Script:** 2 - Generate Tech Specs v1.0.0
"""
        
        return md_content
    
    def process_all_personas(self) -> Dict:
        """Processar todas as personas"""
        
        print("\n" + "="*60)
        print("⚙️ SCRIPT 2 - GERADOR DE TECH SPECS")
        print("="*60)
        print(f"📍 Base: {self.base_path}")
        print(f"👥 Personas: {self.personas_path}")
        
        results = {
            "processed": [],
            "failed": [],
            "total": 0
        }
        
        # Buscar todas as pastas de personas
        for role_folder in self.personas_path.iterdir():
            if role_folder.is_dir():
                print(f"\n📁 Processando {role_folder.name}...")
                
                for persona_folder in role_folder.iterdir():
                    if persona_folder.is_dir():
                        results["total"] += 1
                        
                        if self.create_tech_specs_structure(persona_folder):
                            results["processed"].append(str(persona_folder))
                        else:
                            results["failed"].append(str(persona_folder))
        
        # Relatório final
        print(f"\n{'='*60}")
        print("📊 RELATÓRIO FINAL")
        print(f"{'='*60}")
        print(f"✅ Processadas: {len(results['processed'])}")
        print(f"❌ Falharam: {len(results['failed'])}")
        print(f"📊 Total: {results['total']}")
        
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
    generator = TechSpecsGenerator(base_path)
    results = generator.process_all_personas()
    
    # Exit code baseado no resultado
    if results["failed"]:
        sys.exit(1)
    else:
        print(f"\n🎉 SCRIPT 2 CONCLUÍDO COM SUCESSO!")
        sys.exit(0)


if __name__ == "__main__":
    main()