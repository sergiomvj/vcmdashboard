#!/usr/bin/env python3
"""
🎯 SCRIPT 1 - GERADOR DE COMPETÊNCIAS
=====================================

Analisa biografias das personas e gera competências técnicas e comportamentais.

Input: bio/*.md
Output: competencias/ (JSON + MD)

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

class CompetenciasGenerator:
    def __init__(self, base_path: str = None):
        """Inicializar gerador de competências"""
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent
        
        self.personas_path = self.base_path / "04_PERSONAS_COMPLETAS"
        self.output_path = self.base_path / "competencias_output"
        self.output_path.mkdir(exist_ok=True)
        
        # Templates de competências por área
        self.competencias_templates = {
            "assistente": {
                "tecnicas": [
                    "Gestão de agenda e calendário",
                    "Comunicação escrita profissional",
                    "Atendimento ao cliente",
                    "Organização de documentos",
                    "Suporte administrativo",
                    "Coordenação de reuniões"
                ],
                "comportamentais": [
                    "Proatividade",
                    "Atenção aos detalhes",
                    "Comunicação clara",
                    "Trabalho em equipe",
                    "Adaptabilidade",
                    "Empatia"
                ]
            },
            "executivo": {
                "tecnicas": [
                    "Gestão estratégica",
                    "Análise de dados",
                    "Tomada de decisão",
                    "Planejamento operacional",
                    "Gestão de projetos",
                    "Liderança de equipe"
                ],
                "comportamentais": [
                    "Liderança",
                    "Visão estratégica",
                    "Negociação",
                    "Comunicação executiva",
                    "Resiliência",
                    "Inovação"
                ]
            },
            "especialista": {
                "tecnicas": [
                    "Conhecimento técnico especializado",
                    "Análise e diagnóstico",
                    "Desenvolvimento de soluções",
                    "Consultoria técnica",
                    "Pesquisa e desenvolvimento",
                    "Implementação de processos"
                ],
                "comportamentais": [
                    "Expertise técnica",
                    "Pensamento analítico",
                    "Precisão",
                    "Aprendizado contínuo",
                    "Colaboração",
                    "Orientação a resultados"
                ]
            },
            "gestor": {
                "tecnicas": [
                    "Gestão empresarial",
                    "Planejamento estratégico",
                    "Gestão financeira",
                    "Liderança organizacional",
                    "Gestão de stakeholders",
                    "Governança corporativa"
                ],
                "comportamentais": [
                    "Liderança visionária",
                    "Tomada de decisão estratégica",
                    "Inspiração de equipes",
                    "Comunicação institucional",
                    "Gestão de mudanças",
                    "Responsabilidade corporativa"
                ]
            },
            "suporte": {
                "tecnicas": [
                    "Atendimento ao cliente",
                    "Resolução de problemas",
                    "Gestão de tickets",
                    "Comunicação multicanal",
                    "Escalação de problemas",
                    "Documentação de casos"
                ],
                "comportamentais": [
                    "Paciência",
                    "Empatia",
                    "Comunicação clara",
                    "Resolução de conflitos",
                    "Persistência",
                    "Orientação ao cliente"
                ]
            }
        }
        
    def extract_bio_info(self, bio_content: str) -> Dict:
        """Extrair informações relevantes da biografia"""
        info = {
            "nome": "",
            "nacionalidade": "",
            "idade": "",
            "formacao": "",
            "experiencia": "",
            "especializacao": "",
            "idiomas": [],
            "habilidades_mencionadas": [],
            "bio_completa": bio_content  # Adicionar texto completo para análise
        }
        
        # Extrair nome
        nome_match = re.search(r'\*\*(?:👤\s*)?Nome:\*\*\s*(.+)', bio_content)
        if nome_match:
            info["nome"] = nome_match.group(1).strip()
        
        # Extrair nacionalidade
        nacionalidade_match = re.search(r'\*\*Nacionalidade:\*\*\s*(.+)', bio_content)
        if nacionalidade_match:
            info["nacionalidade"] = nacionalidade_match.group(1).strip()
        
        # Extrair idade
        idade_match = re.search(r'\*\*Idade[^:]*:\*\*\s*(.+)', bio_content)
        if idade_match:
            info["idade"] = idade_match.group(1).strip()
        
        # Extrair formação
        formacao_matches = re.findall(r'formação|graduação|mestrado|doutorado|curso|certificação', bio_content, re.IGNORECASE)
        if formacao_matches:
            info["formacao"] = "Identificada na biografia"
        
        # Extrair idiomas
        idiomas_match = re.search(r'\*\*Idiomas:\*\*\s*(.+)', bio_content)
        if idiomas_match:
            idiomas_text = idiomas_match.group(1)
            info["idiomas"] = [lang.strip() for lang in re.split(r'[,e]', idiomas_text) if lang.strip()]
        
        # Extrair especialização
        espec_match = re.search(r'\*\*Especialização:\*\*\s*(.+)', bio_content)
        if espec_match:
            info["especializacao"] = espec_match.group(1).strip()
        
        return info
    
    def generate_competencias_from_bio(self, bio_info: Dict, role_type: str) -> Dict:
        """Gerar competências baseadas na biografia e tipo de role"""
        
        # Competências base do template
        competencias_base = self.competencias_templates.get(role_type, self.competencias_templates["assistente"])
        
        competencias = {
            "competencias_tecnicas": competencias_base["tecnicas"].copy(),
            "competencias_comportamentais": competencias_base["comportamentais"].copy(),
            "competencias_personalizadas": [],
            "tarefas_diarias": [],
            "tarefas_semanais": [],
            "tarefas_mensais": []
        }
        
        # Extrair texto completo da bio para análise mais profunda
        bio_text = bio_info.get("bio_completa", "").lower()
        especializacao = bio_info.get("especializacao", "").lower()
        
        # COMPETÊNCIAS ESPECÍFICAS DE NUTRIÇÃO
        if any(word in especializacao for word in ["nutrição", "nutricional", "alimentar", "carnívora"]):
            competencias["competencias_personalizadas"].extend([
                "Análise de dados nutricionais avançados",
                "Planejamento de dietas carnívoras personalizadas", 
                "Revisão de relatórios nutricionais especializados",
                "Conhecimento em filosofia alimentar carnívora",
                "Interpretação de exames e métricas de saúde",
                "Desenvolvimento de dashboards nutricionais"
            ])
            
            # TAREFAS DIÁRIAS - NUTRIÇÃO
            competencias["tarefas_diarias"].extend([
                "Acompanhar logs alimentares dos clientes",
                "Responder dúvidas sobre dieta carnívora",
                "Atualizar dashboards de progresso nutricional",
                "Revisar e validar entradas de alimentos",
                "Monitorar alertas de saúde dos clientes",
                "Comunicar-se com clientes multilíngues",
                "Organizar dados de consultas do dia"
            ])
            
            # TAREFAS SEMANAIS - NUTRIÇÃO  
            competencias["tarefas_semanais"].extend([
                "Gerar relatórios de progresso semanal",
                "Analisar tendências nutricionais dos clientes",
                "Revisar e ajustar planos alimentares",
                "Preparar materiais para consultas da semana",
                "Coordenar com equipe de especialistas",
                "Atualizar base de conhecimento nutricional",
                "Realizar follow-ups detalhados de casos"
            ])
            
            # TAREFAS MENSAIS - NUTRIÇÃO
            competencias["tarefas_mensais"].extend([
                "Compilar relatórios mensais de performance",
                "Avaliar eficácia dos protocolos nutricionais",
                "Planejar campanhas educativas sobre carnívora",
                "Revisar e atualizar diretrizes alimentares",
                "Analisar métricas de satisfação dos clientes",
                "Desenvolver novos dashboards e visualizações",
                "Participar de treinamentos especializados"
            ])
            
        # COMPETÊNCIAS MULTILÍNGUES ESPECÍFICAS
        idiomas = bio_info.get("idiomas", [])
        if isinstance(idiomas, str):
            idiomas = [lang.strip() for lang in idiomas.split(',')]
        
        if len(idiomas) > 2:
            competencias["competencias_personalizadas"].extend([
                "Atendimento multilíngue especializado",
                "Comunicação intercultural avançada",
                "Tradução técnica de termos nutricionais",
                "Adaptação cultural de planos alimentares"
            ])
            
            # TAREFAS DIÁRIAS - MULTILÍNGUE
            competencias["tarefas_diarias"].extend([
                "Atender clientes em múltiplos idiomas",
                "Traduzir materiais técnicos conforme demanda",
                "Adaptar comunicação por contexto cultural"
            ])
            
            # TAREFAS SEMANAIS - MULTILÍNGUE
            competencias["tarefas_semanais"].extend([
                "Revisar traduções de materiais educativos",
                "Preparar conteúdo culturalmente adaptado",
                "Coordenar com equipes internacionais"
            ])
        
        # COMPETÊNCIAS DE MARKETING DIGITAL
        if any(word in especializacao for word in ["marketing", "social", "digital", "redes"]):
            competencias["competencias_personalizadas"].extend([
                "Estratégia de marketing digital para saúde",
                "Criação de conteúdo educativo nutricional",
                "Gestão de campanhas de conscientização alimentar",
                "Análise de métricas de engajamento",
                "SEO para conteúdo de saúde e nutrição",
                "Automação de marketing para clientes de dieta"
            ])
            
            # TAREFAS DIÁRIAS - MARKETING
            competencias["tarefas_diarias"].extend([
                "Publicar conteúdo nas redes sociais",
                "Monitorar comentários e engajamento",
                "Responder mensagens de seguidores",
                "Acompanhar métricas de performance diária",
                "Criar posts educativos sobre carnívora"
            ])
            
            # TAREFAS SEMANAIS - MARKETING
            competencias["tarefas_semanais"].extend([
                "Planejar calendário de conteúdo semanal",
                "Analisar performance das campanhas",
                "Criar materiais visuais e vídeos",
                "Otimizar posts para SEO",
                "Coordenar com influenciadores"
            ])
            
            # TAREFAS MENSAIS - MARKETING
            competencias["tarefas_mensais"].extend([
                "Desenvolver estratégias de campanha mensal",
                "Analisar ROI das campanhas",
                "Planejar orçamento de marketing",
                "Avaliar novos canais e plataformas",
                "Criar relatórios executivos de marketing"
            ])
            
        # COMPETÊNCIAS DE YOUTUBE/VIDEO
        if any(word in especializacao for word in ["youtube", "vídeo", "conteúdo", "criação"]):
            competencias["competencias_personalizadas"].extend([
                "Produção de conteúdo educativo em vídeo",
                "Otimização de SEO para YouTube",
                "Storytelling para transformação de saúde",
                "Edição de vídeos educacionais",
                "Análise de performance de canal",
                "Criação de thumbnails atrativas"
            ])
            
            # TAREFAS DIÁRIAS - YOUTUBE
            competencias["tarefas_diarias"].extend([
                "Responder comentários nos vídeos",
                "Monitorar analytics do canal",
                "Filmar conteúdo educativo diário",
                "Interagir com comunidade do YouTube"
            ])
            
            # TAREFAS SEMANAIS - YOUTUBE
            competencias["tarefas_semanais"].extend([
                "Editar e publicar vídeos semanais",
                "Otimizar títulos e descrições para SEO",
                "Criar thumbnails atrativas",
                "Planejar roteiro dos próximos vídeos"
            ])
            
            # TAREFAS MENSAIS - YOUTUBE
            competencias["tarefas_mensais"].extend([
                "Analisar performance geral do canal",
                "Planejar séries temáticas mensais",
                "Colaborar com outros criadores",
                "Atualizar estratégia de conteúdo"
            ])
        
        # COMPETÊNCIAS EXECUTIVAS
        if role_type == "executivo":
            competencias["competencias_personalizadas"].extend([
                "Gestão estratégica de empresa de saúde",
                "Tomada de decisão baseada em dados nutricionais",
                "Liderança de equipes multidisciplinares",
                "Desenvolvimento de protocolos empresariais",
                "Análise de ROI em programas de saúde",
                "Negociação com fornecedores de alimentos"
            ])
            
            # TAREFAS DIÁRIAS - EXECUTIVO
            competencias["tarefas_diarias"].extend([
                "Revisar métricas de performance da empresa",
                "Coordenar reuniões de equipe",
                "Tomar decisões operacionais urgentes",
                "Acompanhar indicadores financeiros",
                "Comunicar-se com stakeholders chave"
            ])
            
            # TAREFAS SEMANAIS - EXECUTIVO
            competencias["tarefas_semanais"].extend([
                "Conduzir reuniões de planejamento semanal",
                "Revisar e aprovar estratégias departamentais",
                "Analisar relatórios de performance",
                "Coordenar com outros executivos",
                "Avaliar progresso de projetos estratégicos"
            ])
            
            # TAREFAS MENSAIS - EXECUTIVO
            competencias["tarefas_mensais"].extend([
                "Desenvolver estratégias de longo prazo",
                "Revisar orçamentos e investimentos",
                "Avaliar performance geral da empresa",
                "Planejar expansão e novos produtos",
                "Apresentar resultados ao board"
            ])
            
        # COMPETÊNCIAS DE SUPORTE TÉCNICO
        if role_type == "suporte":
            competencias["competencias_personalizadas"].extend([
                "Resolução de problemas técnicos em apps de nutrição",
                "Suporte especializado para dieta carnívora",
                "Troubleshooting de dispositivos de monitoramento",
                "Educação de clientes sobre ferramentas digitais",
                "Escalação técnica qualificada",
                "Documentação de casos complexos"
            ])
            
            # TAREFAS DIÁRIAS - SUPORTE
            competencias["tarefas_diarias"].extend([
                "Responder tickets de suporte",
                "Resolver problemas técnicos urgentes",
                "Educar clientes sobre uso do app",
                "Documentar bugs e issues encontrados",
                "Fazer follow-up de casos abertos"
            ])
            
            # TAREFAS SEMANAIS - SUPORTE
            competencias["tarefas_semanais"].extend([
                "Analisar tendências de problemas técnicos",
                "Atualizar base de conhecimento",
                "Treinar novos membros da equipe",
                "Colaborar com desenvolvimento para fixes",
                "Criar tutoriais e materiais de ajuda"
            ])
            
            # TAREFAS MENSAIS - SUPORTE
            competencias["tarefas_mensais"].extend([
                "Avaliar métricas de satisfação do suporte",
                "Propor melhorias nos processos",
                "Participar de treinamentos avançados",
                "Colaborar em desenvolvimento de novas features",
                "Analisar ROI das soluções implementadas"
            ])
        
        # COMPETÊNCIAS BASEADAS EM RESPONSABILIDADES ESPECÍFICAS
        if "organizar e revisar relatórios" in bio_text:
            competencias["competencias_personalizadas"].extend([
                "Organização sistemática de relatórios nutricionais",
                "Revisão técnica de planos alimentares",
                "Controle de qualidade em documentação médica"
            ])
            
            competencias["tarefas_diarias"].extend([
                "Revisar relatórios de clientes do dia",
                "Organizar documentação nutricional",
                "Validar dados de entrada nos sistemas"
            ])
            
            competencias["tarefas_semanais"].extend([
                "Compilar relatórios semanais consolidados",
                "Revisar qualidade dos dados históricos",
                "Coordenar com equipe sobre inconsistências"
            ])
            
        if "contato com clientes" in bio_text:
            competencias["competencias_personalizadas"].extend([
                "Gestão de relacionamento com clientes de saúde",
                "Follow-up personalizado de progresso",
                "Comunicação empática sobre mudanças alimentares"
            ])
            
            competencias["tarefas_diarias"].extend([
                "Responder mensagens de clientes",
                "Fazer check-ins de progresso",
                "Agendar consultas e follow-ups"
            ])
            
        if "coerência entre dados" in bio_text:
            competencias["competencias_personalizadas"].extend([
                "Validação cruzada de dados nutricionais",
                "Garantia de consistência em protocolos",
                "Auditoria de informações científicas"
            ])
            
            competencias["tarefas_diarias"].extend([
                "Validar consistência de dados de entrada",
                "Identificar discrepâncias nos protocolos",
                "Auditar informações científicas atualizadas"
            ])
            
        if any(word in bio_text for word in ["dashboard", "ferramentas digitais", "análise"]):
            competencias["competencias_personalizadas"].extend([
                "Desenvolvimento de dashboards interativos",
                "Domínio avançado de ferramentas de análise",
                "Visualização de dados nutricionais complexos"
            ])
            
            competencias["tarefas_semanais"].extend([
                "Atualizar dashboards de performance",
                "Desenvolver novas visualizações de dados",
                "Analisar métricas e tendências"
            ])
            
        if any(word in bio_text for word in ["fotografia", "design", "visual"]):
            competencias["competencias_personalizadas"].extend([
                "Fotografia profissional de alimentos",
                "Design visual para materiais educativos",
                "Criação de conteúdo visual atrativo"
            ])
            
            competencias["tarefas_semanais"].extend([
                "Criar conteúdo visual para campanhas",
                "Fotografar alimentos para materiais educativos",
                "Desenvolver designs para redes sociais"
            ])
        
        # Remover duplicatas mantendo ordem
        for key in ["competencias_personalizadas", "tarefas_diarias", "tarefas_semanais", "tarefas_mensais"]:
            competencias[key] = list(dict.fromkeys(competencias[key]))
        
        # Limitar a um número razoável
        if len(competencias["competencias_personalizadas"]) > 12:
            competencias["competencias_personalizadas"] = competencias["competencias_personalizadas"][:12]
        if len(competencias["tarefas_diarias"]) > 10:
            competencias["tarefas_diarias"] = competencias["tarefas_diarias"][:10]
        if len(competencias["tarefas_semanais"]) > 8:
            competencias["tarefas_semanais"] = competencias["tarefas_semanais"][:8]
        if len(competencias["tarefas_mensais"]) > 6:
            competencias["tarefas_mensais"] = competencias["tarefas_mensais"][:6]
            
        return competencias
    
    def create_competencias_structure(self, persona_path: Path) -> bool:
        """Criar estrutura de competências para uma persona"""
        
        # Verificar se existe biografia
        bio_files = list(persona_path.glob("*_bio.md"))
        if not bio_files:
            print(f"❌ Biografia não encontrada em {persona_path}")
            return False
        
        bio_file = bio_files[0]
        
        # Ler biografia
        with open(bio_file, 'r', encoding='utf-8') as f:
            bio_content = f.read()
        
        # Extrair informações
        bio_info = self.extract_bio_info(bio_content)
        
        # Determinar tipo de role
        persona_name = persona_path.name
        role_type = "assistente"  # default
        
        if "executivo" in str(persona_path):
            role_type = "executivo"
        elif "especialista" in str(persona_path):
            role_type = "especialista"
        elif "gestor" in str(persona_path):
            role_type = "gestor"
        elif "suporte" in str(persona_path):
            role_type = "suporte"
        
        # Gerar competências
        competencias = self.generate_competencias_from_bio(bio_info, role_type)
        
        # Criar pasta de competências
        comp_path = persona_path / "competencias"
        comp_path.mkdir(exist_ok=True)
        
        # Salvar JSON de competências
        comp_json = {
            "persona_info": {
                "nome": bio_info.get("nome", persona_name),
                "role_type": role_type,
                "especializacao": bio_info.get("especializacao", ""),
                "gerado_em": datetime.now().isoformat()
            },
            "competencias": competencias,
            "metadata": {
                "script_version": "1.0.0",
                "bio_source": bio_file.name,
                "total_competencias": len(competencias["competencias_tecnicas"]) + 
                                    len(competencias["competencias_comportamentais"]) + 
                                    len(competencias["competencias_personalizadas"])
            }
        }
        
        json_file = comp_path / "competencias_core.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(comp_json, f, indent=2, ensure_ascii=False)
        
        # Criar arquivo MD detalhado
        md_content = self.generate_competencias_md(comp_json, bio_info)
        md_file = comp_path / "competencias_detalhadas.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✅ Competências geradas para {persona_name}")
        print(f"   📄 {json_file}")
        print(f"   📋 {md_file}")
        
        return True
    
    def generate_competencias_md(self, comp_data: Dict, bio_info: Dict) -> str:
        """Gerar arquivo MD detalhado das competências"""
        
        persona_info = comp_data["persona_info"]
        competencias = comp_data["competencias"]
        
        md_content = f"""# 🎯 COMPETÊNCIAS - {persona_info['nome'].upper()}

> *Gerado automaticamente pelo Script 1 - Generate Competências*

## 📋 **INFORMAÇÕES BÁSICAS**

- **Nome:** {persona_info['nome']}
- **Role Type:** {persona_info['role_type'].title()}
- **Especialização:** {persona_info['especializacao']}
- **Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔧 **COMPETÊNCIAS TÉCNICAS**

"""
        
        for i, comp in enumerate(competencias["competencias_tecnicas"], 1):
            md_content += f"{i}. **{comp}**\n"
        
        md_content += f"""
## 🧠 **COMPETÊNCIAS COMPORTAMENTAIS**

"""
        
        for i, comp in enumerate(competencias["competencias_comportamentais"], 1):
            md_content += f"{i}. **{comp}**\n"
        
        if competencias["competencias_personalizadas"]:
            md_content += f"""
## ⭐ **COMPETÊNCIAS PERSONALIZADAS**
> *Baseadas na biografia específica*

"""
            for i, comp in enumerate(competencias["competencias_personalizadas"], 1):
                md_content += f"{i}. **{comp}**\n"
        
        # SEÇÕES TEMPORAIS DE TAREFAS
        if competencias.get("tarefas_diarias"):
            md_content += f"""
## 📅 **TAREFAS DIÁRIAS**
> *Atividades operacionais e de rotina*

"""
            for i, tarefa in enumerate(competencias["tarefas_diarias"], 1):
                md_content += f"{i}. **{tarefa}**\n"
        
        if competencias.get("tarefas_semanais"):
            md_content += f"""
## 📊 **TAREFAS SEMANAIS**
> *Análises, relatórios e coordenação*

"""
            for i, tarefa in enumerate(competencias["tarefas_semanais"], 1):
                md_content += f"{i}. **{tarefa}**\n"
        
        if competencias.get("tarefas_mensais"):
            md_content += f"""
## 📈 **TAREFAS MENSAIS**
> *Estratégias, avaliações e planejamento*

"""
            for i, tarefa in enumerate(competencias["tarefas_mensais"], 1):
                md_content += f"{i}. **{tarefa}**\n"
        
        # Calcular totais incluindo tarefas temporais
        total_tarefas = (len(competencias.get("tarefas_diarias", [])) + 
                        len(competencias.get("tarefas_semanais", [])) + 
                        len(competencias.get("tarefas_mensais", [])))
        
        md_content += f"""
## 📊 **RESUMO**

- **Total de Competências:** {comp_data['metadata']['total_competencias']}
- **Técnicas:** {len(competencias['competencias_tecnicas'])}
- **Comportamentais:** {len(competencias['competencias_comportamentais'])}
- **Personalizadas:** {len(competencias['competencias_personalizadas'])}
- **Tarefas Diárias:** {len(competencias.get("tarefas_diarias", []))}
- **Tarefas Semanais:** {len(competencias.get("tarefas_semanais", []))}
- **Tarefas Mensais:** {len(competencias.get("tarefas_mensais", []))}
- **Total de Tarefas:** {total_tarefas}

## 🎯 **ANÁLISE TEMPORAL**

### **🔄 Distribuição de Carga de Trabalho:**
- **Operacional (Diária):** {len(competencias.get("tarefas_diarias", []))} tarefas
- **Tática (Semanal):** {len(competencias.get("tarefas_semanais", []))} tarefas  
- **Estratégica (Mensal):** {len(competencias.get("tarefas_mensais", []))} tarefas

### **📈 Complexidade dos Fluxos N8N:**
- **Workflows Diários:** Automação e monitoramento
- **Workflows Semanais:** Análise e relatórios
- **Workflows Mensais:** Estratégia e planejamento

## 🔄 **PRÓXIMOS PASSOS**

1. **Script 2:** Gerar Tech Specs baseadas nestas competências
2. **Script 3:** Criar RAG personalizado
3. **Script 4:** Desenvolver workflows específicos

---

*Arquivo gerado pelo Virtual Company Generator Master v2.0.0*  
📅 **Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
🔄 **Script:** 1 - Generate Competências v1.0.0
"""
        
        return md_content
    
    def process_all_personas(self) -> Dict:
        """Processar todas as personas encontradas"""
        
        print("\n" + "="*60)
        print("🎯 SCRIPT 1 - GERADOR DE COMPETÊNCIAS")
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
                        
                        if self.create_competencias_structure(persona_folder):
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
    generator = CompetenciasGenerator(base_path)
    results = generator.process_all_personas()
    
    # Exit code baseado no resultado
    if results["failed"]:
        sys.exit(1)
    else:
        print(f"\n🎉 SCRIPT 1 CONCLUÍDO COM SUCESSO!")
        sys.exit(0)


if __name__ == "__main__":
    main()