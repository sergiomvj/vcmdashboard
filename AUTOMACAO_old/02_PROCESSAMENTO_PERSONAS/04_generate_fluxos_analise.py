#!/usr/bin/env python3
"""
VIRTUAL COMPANY GENERATOR - SCRIPT 4
Análise de Fluxos e Task Mapping
Versão: 2.0.0

Este script analisa as competências e tech specs para identificar fluxos de trabalho,
mapeando cada tarefa algoritmicamente e criando documentos tasktodo.md para cada persona.
"""

import json
import os
import logging
from pathlib import Path
from datetime import datetime
import uuid

# Configuração de logging
import os
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/script4_fluxos.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FluxoAnalyzer:
    """Analisador de fluxos de trabalho para personas"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.personas_data = {}
        self.assistentes_config = {
            "coordenador": {
                "role": "Assistente Coordenador Geral",
                "description": "Coordena todos os fluxos de trabalho da persona",
                "ai_model": "gpt-4-turbo-preview",
                "temperature": 0.3,
                "max_tokens": 2000
            }
        }
        
    def load_persona_data(self, persona_path):
        """Carrega competências e tech specs de uma persona"""
        try:
            # Parse do caminho da persona (categoria/nome)
            parts = persona_path.split('/')
            categoria = parts[0]
            persona_name = parts[1]
            
            # Carregar competências
            competencias_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name / "script1_competencias" / "competencias_core.json"
            with open(competencias_path, 'r', encoding='utf-8') as f:
                competencias = json.load(f)
            
            # Carregar tech specs (ai_config + tools_config)
            ai_config_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name / "script2_tech_specs" / "ai_config.json"
            tools_config_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name / "script2_tech_specs" / "tools_config.json"
            
            tech_specs = {}
            if ai_config_path.exists():
                with open(ai_config_path, 'r', encoding='utf-8') as f:
                    tech_specs['ai_config'] = json.load(f)
            
            if tools_config_path.exists():
                with open(tools_config_path, 'r', encoding='utf-8') as f:
                    tech_specs['tools'] = json.load(f)
                
            return {
                "competencias": competencias,
                "tech_specs": tech_specs,
                "persona_name": persona_name,
                "categoria": categoria,
                "full_path": persona_path
            }
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados da persona {persona_path}: {e}")
            return None
    
    def analyze_task_flow(self, task, competencias, tech_specs, categoria_temporal):
        """Analisa um fluxo específico de uma tarefa"""
        
        # Identificar origem da informação
        origem = self._identify_data_source(task, competencias)
        
        # Identificar processamento necessário
        processamento = self._identify_processing(task, tech_specs)
        
        # Identificar destino/saída
        destino = self._identify_output_destination(task, competencias)
        
        # Criar assistente virtual específico para este fluxo
        assistente = self._create_flow_assistant(task, categoria_temporal)
        
        return {
            "task_id": str(uuid.uuid4()),
            "task_name": task,
            "categoria_temporal": categoria_temporal,
            "fluxo_algoritmo": {
                "origem": origem,
                "processamento": processamento,
                "destino": destino
            },
            "assistente_virtual": assistente,
            "dependencies": self._identify_dependencies(task, competencias),
            "tools_required": self._identify_tools(task, tech_specs),
            "validation_criteria": self._create_validation_criteria(task)
        }
    
    def _identify_data_source(self, task, competencias):
        """Identifica de onde vem a informação para a tarefa"""
        sources = []
        
        if any(keyword in task.lower() for keyword in ['clientes', 'atendimento', 'vendas']):
            sources.append("CRM/Sistema de Clientes")
        if any(keyword in task.lower() for keyword in ['dados', 'análise', 'relatório']):
            sources.append("Base de Dados/Analytics")
        if any(keyword in task.lower() for keyword in ['email', 'comunicação']):
            sources.append("Sistema de Email/Comunicação")
        if any(keyword in task.lower() for keyword in ['financeiro', 'pagamento']):
            sources.append("Sistema Financeiro")
        if any(keyword in task.lower() for keyword in ['produto', 'estoque']):
            sources.append("Sistema de Produtos/Estoque")
        
        # Se não identificou fonte específica, usar competências
        if not sources:
            sources.append("Input Manual/Competência Especializada")
            
        return sources
    
    def _identify_processing(self, task, tech_specs):
        """Identifica o que precisa ser feito com a informação"""
        processing = []
        
        if any(keyword in task.lower() for keyword in ['análise', 'analisar']):
            processing.append("Análise de Dados")
        if any(keyword in task.lower() for keyword in ['relatório', 'report']):
            processing.append("Geração de Relatório")
        if any(keyword in task.lower() for keyword in ['criar', 'gerar']):
            processing.append("Criação de Conteúdo")
        if any(keyword in task.lower() for keyword in ['atualizar', 'modificar']):
            processing.append("Atualização de Dados")
        if any(keyword in task.lower() for keyword in ['validar', 'verificar']):
            processing.append("Validação/Verificação")
        if any(keyword in task.lower() for keyword in ['enviar', 'comunicar']):
            processing.append("Comunicação/Envio")
        
        # Adicionar processamento baseado nas tech specs
        if 'ai_config' in tech_specs:
            processing.append("Processamento com IA")
        if 'tools' in tech_specs:
            processing.append("Uso de Ferramentas Especializadas")
            
        return processing
    
    def _identify_output_destination(self, task, competencias):
        """Identifica para onde a informação deve ir"""
        destinations = []
        
        if any(keyword in task.lower() for keyword in ['cliente', 'atendimento']):
            destinations.append("Sistema CRM/Cliente")
        if any(keyword in task.lower() for keyword in ['relatório', 'dashboard']):
            destinations.append("Dashboard/Relatórios")
        if any(keyword in task.lower() for keyword in ['email', 'notificação']):
            destinations.append("Sistema de Notificação")
        if any(keyword in task.lower() for keyword in ['arquivo', 'documento']):
            destinations.append("Sistema de Arquivos")
        if any(keyword in task.lower() for keyword in ['equipe', 'colaborador']):
            destinations.append("Comunicação Interna")
        
        # Default destination
        if not destinations:
            destinations.append("Output Estruturado/Base de Dados")
            
        return destinations
    
    def _create_flow_assistant(self, task, categoria_temporal):
        """Cria configuração do assistente virtual para o fluxo"""
        
        assistant_name = f"Assistant_{task.replace(' ', '_')[:20]}"
        
        # Configuração baseada na categoria temporal
        if categoria_temporal == "diaria":
            role_suffix = "Operacional Diário"
            temperature = 0.2
        elif categoria_temporal == "semanal":  
            role_suffix = "Tático Semanal"
            temperature = 0.3
        else:  # mensal
            role_suffix = "Estratégico Mensal"
            temperature = 0.4
            
        return {
            "name": assistant_name,
            "role": f"Assistente {role_suffix}",
            "task_focus": task,
            "ai_config": {
                "model": "gpt-4-turbo-preview",
                "temperature": temperature,
                "max_tokens": 1500,
                "system_prompt": f"Você é um assistente especializado em {task}. Foque em eficiência e precisão."
            }
        }
    
    def _identify_dependencies(self, task, competencias):
        """Identifica dependências da tarefa"""
        dependencies = []
        
        # Analisar dependências baseadas nas competências
        if 'tarefas_diarias' in competencias:
            for tarefa_diaria in competencias['tarefas_diarias']:
                if task != tarefa_diaria and any(word in task.lower() for word in tarefa_diaria.lower().split()):
                    dependencies.append(tarefa_diaria)
                    
        return dependencies
    
    def _identify_tools(self, task, tech_specs):
        """Identifica ferramentas necessárias"""
        tools = []
        
        if 'tools' in tech_specs:
            tools.extend(tech_specs['tools'])
        
        # Adicionar ferramentas baseadas na tarefa
        if any(keyword in task.lower() for keyword in ['email', 'comunicação']):
            tools.append("Email API")
        if any(keyword in task.lower() for keyword in ['dados', 'análise']):
            tools.append("Analytics Engine")
        if any(keyword in task.lower() for keyword in ['relatório']):
            tools.append("Report Generator")
            
        return list(set(tools))  # Remove duplicatas
    
    def _create_validation_criteria(self, task):
        """Cria critérios de validação para a tarefa"""
        criteria = []
        
        criteria.append("Dados de entrada validados")
        criteria.append("Processamento executado sem erros")
        criteria.append("Output gerado no formato correto")
        
        if any(keyword in task.lower() for keyword in ['cliente', 'atendimento']):
            criteria.append("Satisfação do cliente verificada")
        if any(keyword in task.lower() for keyword in ['dados', 'análise']):
            criteria.append("Precisão dos dados verificada")
        if any(keyword in task.lower() for keyword in ['relatório']):
            criteria.append("Completude do relatório verificada")
            
        return criteria
    
    def generate_tasktodo_document(self, persona_data):
        """Gera documento tasktodo.md para uma persona"""
        
        persona_name = persona_data["persona_name"]
        competencias = persona_data["competencias"]
        tech_specs = persona_data["tech_specs"]
        
        # Analisar todas as tarefas por categoria temporal
        fluxos_analysis = {
            "diarias": [],
            "semanais": [], 
            "mensais": []
        }
        
        # Processar tarefas diárias
        if 'tarefas_diarias' in competencias:
            for task in competencias['tarefas_diarias']:
                analysis = self.analyze_task_flow(task, competencias, tech_specs, "diaria")
                fluxos_analysis["diarias"].append(analysis)
        
        # Processar tarefas semanais
        if 'tarefas_semanais' in competencias:
            for task in competencias['tarefas_semanais']:
                analysis = self.analyze_task_flow(task, competencias, tech_specs, "semanal")
                fluxos_analysis["semanais"].append(analysis)
        
        # Processar tarefas mensais
        if 'tarefas_mensais' in competencias:
            for task in competencias['tarefas_mensais']:
                analysis = self.analyze_task_flow(task, competencias, tech_specs, "mensal")
                fluxos_analysis["mensais"].append(analysis)
        
        # Gerar documento markdown
        tasktodo_content = self._generate_markdown_content(persona_name, fluxos_analysis)
        
        # Criar diretório script4_tasktodo dentro da pasta da persona
        categoria = persona_data.get("categoria", "unknown")
        persona_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_data["persona_name"]
        tasktodo_dir = persona_path / "script4_tasktodo"
        tasktodo_dir.mkdir(parents=True, exist_ok=True)
        
        # Salvar documento
        tasktodo_path = tasktodo_dir / "tasktodo.md"
        with open(tasktodo_path, 'w', encoding='utf-8') as f:
            f.write(tasktodo_content)
            
        # Salvar análise JSON para processamento posterior
        analysis_path = tasktodo_dir / "fluxos_analysis.json"
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(fluxos_analysis, f, indent=2, ensure_ascii=False)
            
        logging.info(f"TaskTodo gerado para {persona_name}: {tasktodo_path}")
        return tasktodo_path
    
    def _generate_markdown_content(self, persona_name, fluxos_analysis):
        """Gera conteúdo markdown do documento tasktodo"""
        
        content = f"""# TASKTODO - {persona_name.upper()}
*Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📋 RESUMO EXECUTIVO
Este documento mapeia algoritmicamente todos os fluxos de trabalho necessários para {persona_name}, 
organizados por categoria temporal (diário/semanal/mensal) com assistentes virtuais dedicados.

## 🔄 ASSISTENTE COORDENADOR GERAL
**Nome**: Coordenador_{persona_name}
**Função**: Orquestrar todos os fluxos de trabalho
**Responsabilidades**:
- Coordenar execução de tarefas entre assistentes
- Monitorar dependências e cronogramas
- Resolver conflitos de prioridade
- Reportar status geral

---

"""

        # Processar cada categoria temporal
        for categoria, fluxos in fluxos_analysis.items():
            if not fluxos:
                continue
                
            categoria_upper = categoria.upper()
            content += f"## 📅 FLUXOS {categoria_upper}\n\n"
            
            for idx, fluxo in enumerate(fluxos, 1):
                content += f"### {idx}. {fluxo['task_name']}\n"
                content += f"**Task ID**: `{fluxo['task_id']}`\n\n"
                
                # Algoritmo do fluxo
                content += "#### 🔍 ALGORITMO DE EXECUÇÃO\n"
                content += "```algorithm\n"
                content += "INÍCIO\n"
                content += f"  INPUT: {' | '.join(fluxo['fluxo_algoritmo']['origem'])}\n"
                content += f"  PROCESSO:\n"
                for processo in fluxo['fluxo_algoritmo']['processamento']:
                    content += f"    - {processo}\n"
                content += f"  OUTPUT: {' | '.join(fluxo['fluxo_algoritmo']['destino'])}\n"
                content += "  VALIDAÇÃO:\n"
                for criterio in fluxo['validation_criteria']:
                    content += f"    - {criterio}\n"
                content += "FIM\n"
                content += "```\n\n"
                
                # Assistente Virtual
                assistente = fluxo['assistente_virtual']
                content += "#### 🤖 ASSISTENTE VIRTUAL\n"
                content += f"- **Nome**: {assistente['name']}\n"
                content += f"- **Role**: {assistente['role']}\n"
                content += f"- **AI Model**: {assistente['ai_config']['model']}\n"
                content += f"- **Temperature**: {assistente['ai_config']['temperature']}\n\n"
                
                # Dependências
                if fluxo['dependencies']:
                    content += "#### 🔗 DEPENDÊNCIAS\n"
                    for dep in fluxo['dependencies']:
                        content += f"- {dep}\n"
                    content += "\n"
                
                # Ferramentas
                if fluxo['tools_required']:
                    content += "#### 🛠️ FERRAMENTAS NECESSÁRIAS\n"
                    for tool in fluxo['tools_required']:
                        content += f"- {tool}\n"
                    content += "\n"
                
                content += "---\n\n"
        
        # Resumo final
        total_fluxos = sum(len(fluxos) for fluxos in fluxos_analysis.values())
        content += f"## 📊 ESTATÍSTICAS\n"
        content += f"- **Total de Fluxos**: {total_fluxos}\n"
        content += f"- **Fluxos Diários**: {len(fluxos_analysis.get('diarias', []))}\n"
        content += f"- **Fluxos Semanais**: {len(fluxos_analysis.get('semanais', []))}\n"
        content += f"- **Fluxos Mensais**: {len(fluxos_analysis.get('mensais', []))}\n"
        content += f"- **Assistentes Virtuais**: {total_fluxos + 1} (incluindo coordenador)\n\n"
        
        content += "## ✅ CHECKLIST DE VALIDAÇÃO\n"
        content += "- [ ] Todas as competências foram mapeadas\n"
        content += "- [ ] Tech specs foram consideradas\n"
        content += "- [ ] Fluxos estão algoritmicamente definidos\n"
        content += "- [ ] Assistentes virtuais configurados\n"
        content += "- [ ] Dependências identificadas\n"
        content += "- [ ] Critérios de validação estabelecidos\n"
        
        return content

def main():
    """Função principal do Script 4"""
    
    print("VIRTUAL COMPANY GENERATOR - SCRIPT 4")
    print("Análise de Fluxos e Task Mapping")
    print("=" * 50)
    
    # Solicitar diretório de output
    output_dir = input("\nDigite o caminho do diretório de output da empresa: ")
    
    if not os.path.exists(output_dir):
        print(f"ERRO: Diretório não encontrado: {output_dir}")
        return
    
    # Inicializar analisador
    analyzer = FluxoAnalyzer(output_dir)
    
    # Descobrir personas disponíveis
    personas_dir = Path(output_dir) / "04_PERSONAS_COMPLETAS"
    if not personas_dir.exists():
        print("ERRO: Diretório de personas não encontrado!")
        return
    
    # Buscar arquivos de competências para identificar personas (estrutura hierárquica)
    personas = []
    for categoria_dir in personas_dir.iterdir():
        if categoria_dir.is_dir():
            for persona_dir in categoria_dir.iterdir():
                if persona_dir.is_dir():
                    competencias_file = persona_dir / "script1_competencias" / "competencias_core.json"
                    if competencias_file.exists():
                        personas.append(f"{categoria_dir.name}/{persona_dir.name}")
    
    print(f"\nPersonas encontradas: {len(personas)}")
    for persona in personas:
        print(f"   - {persona}")
    
    print("\nIniciando análise de fluxos...")
    
    # Processar cada persona
    for persona in personas:
        print(f"\nProcessando {persona}...")
        
        # Carregar dados da persona
        persona_data = analyzer.load_persona_data(persona)
        
        if persona_data:
            # Gerar documento tasktodo
            tasktodo_path = analyzer.generate_tasktodo_document(persona_data)
            print(f"   SUCESSO: TaskTodo gerado: {tasktodo_path}")
        else:
            print(f"   ERRO: Erro ao processar {persona}")
    
    print("\nSCRIPT 4 CONCLUÍDO COM SUCESSO!")
    print("Documentos TaskTodo gerados na pasta: tasktodo/")
    print("Execute o Script 5 para gerar os workflows N8N")

if __name__ == "__main__":
    main()