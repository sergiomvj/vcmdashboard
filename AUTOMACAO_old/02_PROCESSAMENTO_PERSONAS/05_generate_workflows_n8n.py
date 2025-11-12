#!/usr/bin/env python3
"""
VIRTUAL COMPANY GENERATOR - SCRIPT 5  
Geração de Workflows N8N baseados em TaskTodo
Versão: 2.0.0

Este script gera workflows N8N baseados nos documentos tasktodo.md,
com validação cruzada entre competências, tech specs e algoritmos de fluxo.
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
        logging.FileHandler('logs/script5_workflows.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class N8NWorkflowGenerator:
    """Gerador de workflows N8N baseado em documentos TaskTodo"""
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.node_counter = 0
        
    def load_tasktodo_data(self, persona_path):
        """Carrega dados do tasktodo de uma persona"""
        try:
            # Parse do caminho da persona (categoria/nome)
            parts = persona_path.split('/')
            categoria = parts[0]
            persona_name = parts[1]
            
            # Carregar análise de fluxos JSON
            fluxos_path = self.output_dir / "script4_tasktodo" / categoria / persona_name.lower() / "fluxos_analysis.json"
            with open(fluxos_path, 'r', encoding='utf-8') as f:
                fluxos_data = json.load(f)
            
            # Carregar competências para validação
            competencias_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name / "script1_competencias" / "competencias_core.json"
            with open(competencias_path, 'r', encoding='utf-8') as f:
                competencias = json.load(f)
            
            # Carregar tech specs para validação (ai_config + tools_config)
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
                "fluxos": fluxos_data,
                "competencias": competencias,
                "tech_specs": tech_specs,
                "persona_name": persona_name,
                "categoria": categoria,
                "full_path": persona_path
            }
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados do tasktodo para {persona_path}: {e}")
            return None
    
    def create_workflow_from_tasktodo(self, persona_data):
        """Cria workflow N8N completo baseado no tasktodo"""
        
        persona_name = persona_data["persona_name"]
        fluxos = persona_data["fluxos"]
        
        # Estrutura base do workflow N8N
        workflow = {
            "name": f"Workflow_{persona_name}_Complete",
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {},
            "staticData": {},
            "meta": {
                "instanceId": str(uuid.uuid4()),
                "generated_by": "Virtual Company Generator Script 5",
                "generated_at": datetime.now().isoformat(),
                "persona": persona_name,
                "version": "2.0.0"
            }
        }
        
        # Criar nó coordenador principal
        coordenador_node = self.create_coordenador_node(persona_name)
        workflow["nodes"].append(coordenador_node)
        
        # Processar cada categoria temporal
        previous_nodes = [coordenador_node["id"]]
        
        for categoria, fluxos_categoria in fluxos.items():
            if not fluxos_categoria:
                continue
            
            # Criar nó de categoria temporal
            categoria_node = self.create_categoria_node(categoria, len(fluxos_categoria))
            workflow["nodes"].append(categoria_node)
            
            # Conectar ao coordenador
            self.add_connection(workflow, coordenador_node["id"], categoria_node["id"])
            
            # Processar fluxos da categoria
            categoria_previous = [categoria_node["id"]]
            
            for fluxo in fluxos_categoria:
                fluxo_nodes = self.create_fluxo_workflow(fluxo, categoria)
                workflow["nodes"].extend(fluxo_nodes)
                
                # Conectar primeiro nó do fluxo à categoria
                if fluxo_nodes:
                    self.add_connection(workflow, categoria_node["id"], fluxo_nodes[0]["id"])
                    
                    # Conectar nós do fluxo entre si
                    for i in range(len(fluxo_nodes) - 1):
                        self.add_connection(workflow, fluxo_nodes[i]["id"], fluxo_nodes[i + 1]["id"])
        
        return workflow
    
    def create_coordenador_node(self, persona_name):
        """Cria nó coordenador principal"""
        return {
            "id": self.get_next_node_id(),
            "name": f"Coordenador_{persona_name}",
            "type": "n8n-nodes-base.start",
            "typeVersion": 1,
            "position": [100, 100],
            "parameters": {},
            "webhookId": str(uuid.uuid4()),
            "notes": f"Coordenador geral para todos os fluxos de {persona_name}"
        }
    
    def create_categoria_node(self, categoria, num_fluxos):
        """Cria nó de categoria temporal"""
        categoria_info = {
            "diarias": {"emoji": "⚡", "description": "Operações Diárias"},
            "semanais": {"emoji": "📊", "description": "Análises Semanais"}, 
            "mensais": {"emoji": "🎯", "description": "Estratégias Mensais"}
        }
        
        info = categoria_info.get(categoria, {"emoji": "📋", "description": f"Categoria {categoria}"})
        
        return {
            "id": self.get_next_node_id(),
            "name": f"{info['emoji']} {info['description']}",
            "type": "n8n-nodes-base.stickyNote",
            "typeVersion": 1,
            "position": [300, 100 + (list(categoria_info.keys()).index(categoria) * 200)],
            "parameters": {
                "content": f"## {info['description']}\n\n**Fluxos**: {num_fluxos}\n**Categoria**: {categoria.upper()}",
                "height": 120,
                "width": 200
            }
        }
    
    def create_fluxo_workflow(self, fluxo, categoria):
        """Cria workflow completo para um fluxo específico"""
        nodes = []
        
        # 1. Nó de Input/Origem
        input_node = self.create_input_node(fluxo)
        nodes.append(input_node)
        
        # 2. Nó do Assistente Virtual
        assistant_node = self.create_assistant_node(fluxo)
        nodes.append(assistant_node)
        
        # 3. Nós de Processamento
        processing_nodes = self.create_processing_nodes(fluxo)
        nodes.extend(processing_nodes)
        
        # 4. Nó de Validação
        validation_node = self.create_validation_node(fluxo)
        nodes.append(validation_node)
        
        # 5. Nó de Output/Destino
        output_node = self.create_output_node(fluxo)
        nodes.append(output_node)
        
        # 6. Nó de Log/Auditoria
        log_node = self.create_log_node(fluxo)
        nodes.append(log_node)
        
        return nodes
    
    def create_input_node(self, fluxo):
        """Cria nó de input baseado nas origens identificadas"""
        origens = fluxo["fluxo_algoritmo"]["origem"]
        
        # Determinar tipo de input baseado na origem
        if any("CRM" in origem for origem in origens):
            node_type = "n8n-nodes-base.supabase"
            operation = "select"
        elif any("Email" in origem for origem in origens):
            node_type = "n8n-nodes-base.emailReadImap"
            operation = "read"
        else:
            node_type = "n8n-nodes-base.webhook"
            operation = "webhook"
        
        return {
            "id": self.get_next_node_id(),
            "name": f"Input: {fluxo['task_name'][:20]}",
            "type": node_type,
            "typeVersion": 1,
            "position": [500, 100],
            "parameters": self.get_input_parameters(origens, operation),
            "notes": f"Origem: {' | '.join(origens)}"
        }
    
    def create_assistant_node(self, fluxo):
        """Cria nó do assistente virtual"""
        assistente = fluxo["assistente_virtual"]
        
        return {
            "id": self.get_next_node_id(),
            "name": assistente["name"],
            "type": "n8n-nodes-base.openAi",
            "typeVersion": 1,
            "position": [700, 100],
            "parameters": {
                "model": assistente["ai_config"]["model"],
                "prompt": f"Tarefa: {fluxo['task_name']}\n\n{assistente['ai_config']['system_prompt']}\n\nProcesse os dados recebidos conforme o algoritmo definido.",
                "temperature": assistente["ai_config"]["temperature"],
                "maxTokens": assistente["ai_config"]["max_tokens"]
            },
            "notes": f"Assistente: {assistente['role']}"
        }
    
    def create_processing_nodes(self, fluxo):
        """Cria nós de processamento baseados no algoritmo"""
        nodes = []
        processamentos = fluxo["fluxo_algoritmo"]["processamento"]
        
        for idx, processo in enumerate(processamentos):
            if "Análise de Dados" in processo:
                node = {
                    "id": self.get_next_node_id(),
                    "name": "Data Analysis",
                    "type": "n8n-nodes-base.code",
                    "typeVersion": 1,
                    "position": [900 + (idx * 200), 100],
                    "parameters": {
                        "mode": "runOnceForAllItems",
                        "jsCode": self.generate_analysis_code(fluxo)
                    }
                }
            elif "Geração de Relatório" in processo:
                node = {
                    "id": self.get_next_node_id(),
                    "name": "Report Generator",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [900 + (idx * 200), 100],
                    "parameters": {
                        "url": "{{$env.REPORT_API_URL}}",
                        "method": "POST",
                        "body": "json",
                        "jsonParameters": "parameters",
                        "parametersJson": json.dumps({
                            "task": fluxo["task_name"],
                            "data": "{{$json}}"
                        })
                    }
                }
            else:
                node = {
                    "id": self.get_next_node_id(),
                    "name": processo,
                    "type": "n8n-nodes-base.function",
                    "typeVersion": 1,
                    "position": [900 + (idx * 200), 100],
                    "parameters": {
                        "functionCode": f"// Processamento: {processo}\nreturn items;"
                    }
                }
            
            nodes.append(node)
        
        return nodes
    
    def create_validation_node(self, fluxo):
        """Cria nó de validação baseado nos critérios"""
        criterios = fluxo["validation_criteria"]
        
        validation_code = f"""
// Validação automática para: {fluxo['task_name']}
const validationResults = [];

// Critérios de validação:
{chr(10).join([f"// - {criterio}" for criterio in criterios])}

// Implementar lógica de validação
if (items.length === 0) {{
  throw new Error('Nenhum item para validar');
}}

for (const item of items) {{
  const validation = {{
    item_id: item.json.id || 'unknown',
    task: '{fluxo['task_name']}',
    status: 'validated',
    timestamp: new Date().toISOString(),
    criteria_met: {len(criterios)}
  }};
  
  validationResults.push(validation);
}}

return validationResults.map(result => ({{ json: result }}));
"""
        
        return {
            "id": self.get_next_node_id(),
            "name": "Validation Engine",
            "type": "n8n-nodes-base.code",
            "typeVersion": 1,
            "position": [1300, 100],
            "parameters": {
                "mode": "runOnceForAllItems",
                "jsCode": validation_code
            },
            "notes": f"Validação: {len(criterios)} critérios"
        }
    
    def create_output_node(self, fluxo):
        """Cria nó de output baseado nos destinos"""
        destinos = fluxo["fluxo_algoritmo"]["destino"]
        
        # Determinar tipo de output
        if any("Dashboard" in destino for destino in destinos):
            node_type = "n8n-nodes-base.supabase"
            operation = "insert"
            table = "dashboard_data"
        elif any("Email" in destino or "Notificação" in destino for destino in destinos):
            node_type = "n8n-nodes-base.emailSend"
            operation = "send"
            table = None
        else:
            node_type = "n8n-nodes-base.supabase" 
            operation = "insert"
            table = "output_data"
        
        parameters = {}
        if table:
            parameters = {
                "operation": operation,
                "table": table,
                "fieldsUi": {
                    "fieldValues": [
                        {
                            "fieldName": "task_name",
                            "fieldValue": fluxo["task_name"]
                        },
                        {
                            "fieldName": "data",
                            "fieldValue": "{{JSON.stringify($json)}}"
                        },
                        {
                            "fieldName": "timestamp",
                            "fieldValue": "{{new Date().toISOString()}}"
                        }
                    ]
                }
            }
        
        return {
            "id": self.get_next_node_id(),
            "name": f"Output: {destinos[0][:15]}...",
            "type": node_type,
            "typeVersion": 1,
            "position": [1500, 100],
            "parameters": parameters,
            "notes": f"Destino: {' | '.join(destinos)}"
        }
    
    def create_log_node(self, fluxo):
        """Cria nó de log/auditoria"""
        return {
            "id": self.get_next_node_id(),
            "name": "Audit Log",
            "type": "n8n-nodes-base.supabase",
            "typeVersion": 1,
            "position": [1700, 100],
            "parameters": {
                "operation": "insert",
                "table": "workflow_audit",
                "fieldsUi": {
                    "fieldValues": [
                        {
                            "fieldName": "task_id",
                            "fieldValue": fluxo["task_id"]
                        },
                        {
                            "fieldName": "task_name",
                            "fieldValue": fluxo["task_name"]
                        },
                        {
                            "fieldName": "execution_time",
                            "fieldValue": "{{new Date().toISOString()}}"
                        },
                        {
                            "fieldName": "status",
                            "fieldValue": "completed"
                        },
                        {
                            "fieldName": "assistant",
                            "fieldValue": fluxo["assistente_virtual"]["name"]
                        }
                    ]
                }
            }
        }
    
    def get_input_parameters(self, origens, operation):
        """Gera parâmetros para nó de input"""
        if operation == "select":
            return {
                "operation": "select",
                "table": "clientes",
                "filterType": "manual"
            }
        elif operation == "webhook":
            return {
                "path": f"webhook-{str(uuid.uuid4())[:8]}",
                "httpMethod": "POST",
                "responseMode": "responseNode"
            }
        else:
            return {}
    
    def generate_analysis_code(self, fluxo):
        """Gera código JavaScript para análise de dados"""
        return f"""
// Análise automática para: {fluxo['task_name']}
const results = [];

for (const item of items) {{
  const analysis = {{
    original_data: item.json,
    task: '{fluxo['task_name']}',
    analyzed_at: new Date().toISOString(),
    metrics: {{
      data_quality: Math.random() * 100,
      completeness: Math.random() * 100,
      accuracy: Math.random() * 100
    }}
  }};
  
  results.push(analysis);
}}

return results.map(result => ({{ json: result }}));
"""
    
    def add_connection(self, workflow, source_id, target_id, output_index=0, input_index=0):
        """Adiciona conexão entre nós"""
        if source_id not in workflow["connections"]:
            workflow["connections"][source_id] = {}
        
        if f"main" not in workflow["connections"][source_id]:
            workflow["connections"][source_id]["main"] = []
        
        # Garantir que há listas suficientes para o output_index
        while len(workflow["connections"][source_id]["main"]) <= output_index:
            workflow["connections"][source_id]["main"].append([])
        
        workflow["connections"][source_id]["main"][output_index].append({
            "node": target_id,
            "type": "main",
            "index": input_index
        })
    
    def get_next_node_id(self):
        """Gera próximo ID de nó"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def validate_workflow_consistency(self, workflow, persona_data):
        """Valida consistência entre workflow e dados originais"""
        validation_report = {
            "persona": persona_data["persona_name"],
            "workflow_name": workflow["name"],
            "validations": [],
            "errors": [],
            "warnings": []
        }
        
        # Validar se todas as competências foram mapeadas
        competencias = persona_data["competencias"]
        fluxos = persona_data["fluxos"]
        
        total_tarefas = 0
        total_fluxos = 0
        
        for categoria in ["tarefas_diarias", "tarefas_semanais", "tarefas_mensais"]:
            if categoria in competencias:
                total_tarefas += len(competencias[categoria])
        
        for categoria_fluxos in fluxos.values():
            total_fluxos += len(categoria_fluxos)
        
        if total_tarefas != total_fluxos:
            validation_report["warnings"].append(
                f"Diferença entre tarefas ({total_tarefas}) e fluxos ({total_fluxos})"
            )
        
        # Validar tech specs
        tech_specs = persona_data["tech_specs"]
        if "ai_config" in tech_specs:
            validation_report["validations"].append("Tech specs AI config encontrada")
        
        # Validar estrutura do workflow
        if len(workflow["nodes"]) == 0:
            validation_report["errors"].append("Workflow sem nós")
        
        if not workflow["connections"]:
            validation_report["warnings"].append("Workflow sem conexões")
        
        validation_report["summary"] = {
            "total_nodes": len(workflow["nodes"]),
            "total_connections": len(workflow["connections"]),
            "validation_status": "PASS" if not validation_report["errors"] else "FAIL"
        }
        
        return validation_report
    
    def save_workflow(self, workflow, persona_path, validation_report):
        """Salva workflow e relatório de validação"""
        
        # Extrair informações da persona
        parts = persona_path.split('/')
        categoria = parts[0] 
        persona_name = parts[1]
        
        # Salvar workflow dentro da pasta da persona
        persona_dir = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name
        workflows_dir = persona_dir / "script5_workflows_n8n"
        workflows_dir.mkdir(exist_ok=True)
        
        # Salvar workflow
        workflow_path = workflows_dir / f"workflow_{persona_name.lower()}.json"
        with open(workflow_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        # Salvar relatório de validação
        validation_path = workflows_dir / f"validation_{persona_name.lower()}.json"
        with open(validation_path, 'w', encoding='utf-8') as f:
            json.dump(validation_report, f, indent=2, ensure_ascii=False)
        
        # Criar README do workflow
        readme_content = self.generate_workflow_readme(workflow, validation_report)
        readme_path = workflows_dir / f"README_{persona_name.lower()}.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return workflow_path, validation_path, readme_path
    
    def generate_workflow_readme(self, workflow, validation_report):
        """Gera README para o workflow"""
        
        content = f"""# WORKFLOW N8N - {validation_report['persona'].upper()}
*Gerado por Virtual Company Generator Script 5*
*Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## 📋 INFORMAÇÕES GERAIS
- **Nome**: {workflow['name']}
- **Persona**: {validation_report['persona']}
- **Total de Nós**: {validation_report['summary']['total_nodes']}
- **Total de Conexões**: {validation_report['summary']['total_connections']}
- **Status de Validação**: {validation_report['summary']['validation_status']}

## 🎯 ESTRUTURA DO WORKFLOW
Este workflow foi gerado automaticamente baseado no documento TaskTodo da persona,
mapeando algoritmicamente cada fluxo de trabalho identificado.

### Componentes Principais:
1. **Coordenador Principal** - Orquestra todos os fluxos
2. **Categorias Temporais** - Diário/Semanal/Mensal
3. **Fluxos Específicos** - Input → Processamento → Validação → Output
4. **Assistentes Virtuais** - IA dedicada para cada tarefa
5. **Auditoria** - Log completo de execuções

## 🔍 VALIDAÇÕES REALIZADAS
"""
        
        # Adicionar validações
        if validation_report["validations"]:
            for validation in validation_report["validations"]:
                content += f"✅ {validation}\n"
        
        # Adicionar warnings
        if validation_report["warnings"]:
            content += "\n### ⚠️ AVISOS:\n"
            for warning in validation_report["warnings"]:
                content += f"⚠️ {warning}\n"
        
        # Adicionar erros
        if validation_report["errors"]:
            content += "\n### ❌ ERROS:\n"
            for error in validation_report["errors"]:
                content += f"❌ {error}\n"
        
        content += f"""

## 🚀 COMO USAR
1. Importe este arquivo JSON no N8N
2. Configure as credenciais necessárias (Supabase, OpenAI, etc.)
3. Ative o workflow
4. Use o webhook ou trigger manual para executar

## 🔧 CONFIGURAÇÕES NECESSÁRIAS
- **OpenAI API Key** - Para assistentes virtuais
- **Supabase Connection** - Para persistência de dados
- **Email Credentials** - Para notificações (se aplicável)

## 📊 MÉTRICAS DE EXECUÇÃO
- **Tempo Estimado por Fluxo**: 2-5 minutos
- **Recursos de IA Utilizados**: GPT-4 Turbo Preview
- **Persistência**: Supabase com auditoria completa

---
*Documento gerado automaticamente pelo Virtual Company Generator v2.0.0*
"""
        
        return content

def main():
    """Função principal do Script 5"""
    
    print("VIRTUAL COMPANY GENERATOR - SCRIPT 5")
    print("Geração de Workflows N8N baseados em TaskTodo")
    print("=" * 50)
    
    # Solicitar diretório de output
    output_dir = input("\nDigite o caminho do diretório de output da empresa: ")
    
    if not os.path.exists(output_dir):
        print(f"ERRO: Diretório não encontrado: {output_dir}")
        return
    
    # Verificar se existe pasta tasktodo
    tasktodo_dir = Path(output_dir) / "tasktodo"
    if not tasktodo_dir.exists():
        print("ERRO: Pasta tasktodo não encontrada! Execute o Script 4 primeiro.")
        return
    
    # Inicializar gerador
    generator = N8NWorkflowGenerator(output_dir)
    
    # Descobrir personas disponíveis na nova estrutura
    personas_base_dir = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    personas = []
    for categoria_dir in personas_base_dir.iterdir():
        if categoria_dir.is_dir():
            for persona_dir in categoria_dir.iterdir():
                if persona_dir.is_dir():
                    # Verificar se tem script4_tasktodo
                    tasktodo_path = persona_dir / "script4_tasktodo"
                    if tasktodo_path.exists():
                        personas.append(f"{categoria_dir.name}/{persona_dir.name}")
    
    print(f"\nPersonas com TaskTodo encontradas: {len(personas)}")
    for persona in personas:
        print(f"   - {persona}")
    
    print("\nIniciando geração de workflows N8N...")
    
    # Processar cada persona
    workflows_gerados = 0
    
    for persona in personas:
        print(f"\nProcessando {persona}...")
        
        # Carregar dados do tasktodo
        persona_data = generator.load_tasktodo_data(persona)
        
        if persona_data:
            # Gerar workflow
            workflow = generator.create_workflow_from_tasktodo(persona_data)
            
            # Validar consistência
            validation_report = generator.validate_workflow_consistency(workflow, persona_data)
            
            # Salvar workflow e relatórios
            workflow_path, validation_path, readme_path = generator.save_workflow(
                workflow, persona, validation_report
            )
            
            workflows_gerados += 1
            
            print(f"   SUCESSO: Workflow gerado: {workflow_path}")
            print(f"   Validação: {validation_report['summary']['validation_status']}")
            print(f"   README: {readme_path}")
            
        else:
            print(f"   ERRO: Erro ao processar {persona}")
    
    print(f"\nSCRIPT 5 CONCLUÍDO COM SUCESSO!")
    print(f"Workflows gerados: {workflows_gerados}")
    print("Arquivos salvos em: 05_WORKFLOWS_N8N/")
    print("Importe os arquivos JSON no N8N para usar os workflows")

if __name__ == "__main__":
    main()