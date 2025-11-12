#!/usr/bin/env python3
"""
ATUALIZAÇÃO DOS SCRIPTS PARA NOVA ESTRUTURA
Atualiza todos os scripts 4 e 5 para funcionarem com a estrutura reorganizada
"""

import os
from pathlib import Path

def update_scripts_for_new_structure():
    """Atualiza scripts para funcionar com nova estrutura"""
    
    print("🔄 ATUALIZANDO SCRIPTS PARA NOVA ESTRUTURA...")
    print("=" * 50)
    
    # Caminhos dos scripts
    script_dir = Path(r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\VIRTUAL_COMPANY_GENERATOR\core")
    
    # Atualizar Script 4
    update_script_4(script_dir)
    
    # Atualizar Script 5
    update_script_5(script_dir)
    
    print("\n✅ SCRIPTS ATUALIZADOS COM SUCESSO!")
    print("🔄 Agora os scripts funcionam com a nova estrutura organizada")

def update_script_4(script_dir):
    """Atualiza Script 4 para nova estrutura"""
    
    script4_path = script_dir / "generate_fluxos_analise.py"
    
    print("📝 Atualizando Script 4...")
    
    # Ler conteúdo atual
    with open(script4_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituições para nova estrutura
    replacements = {
        '/ "04_PERSONAS_COMPLETAS" /': '/ "04_PERSONAS_SCRIPTS_1_2_3" /',
        '/ "competencias" /': '/ "script1_competencias" /',
        '/ "tech_specs" /': '/ "script2_tech_specs" /',
        'competencias_core.json': 'competencias_core.json',  # Mantém
        'ai_config.json': 'ai_config.json',  # Mantém  
        'tools_config.json': 'tools_config.json'  # Mantém
    }
    
    # Aplicar substituições
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Atualizar local onde salva tasktodo - agora salva direto na pasta da persona
    old_tasktodo_save = '''# Criar diretório tasktodo se não existir
        # Usar categoria/persona para organizar
        categoria = persona_data.get("categoria", "unknown")
        tasktodo_dir = self.output_dir / "tasktodo" / categoria / persona_name.lower()
        tasktodo_dir.mkdir(parents=True, exist_ok=True)'''
    
    new_tasktodo_save = '''# Criar diretório script4_tasktodo dentro da pasta da persona
        categoria = persona_data.get("categoria", "unknown")
        persona_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_data["persona_name"]
        tasktodo_dir = persona_path / "script4_tasktodo"
        tasktodo_dir.mkdir(parents=True, exist_ok=True)'''
    
    content = content.replace(old_tasktodo_save, new_tasktodo_save)
    
    # Salvar arquivo atualizado
    with open(script4_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ Script 4 atualizado")

def update_script_5(script_dir):
    """Atualiza Script 5 para nova estrutura"""
    
    script5_path = script_dir / "generate_workflows_n8n.py"
    
    print("📝 Atualizando Script 5...")
    
    # Ler conteúdo atual
    with open(script5_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituições para nova estrutura
    replacements = {
        '/ "04_PERSONAS_COMPLETAS" /': '/ "04_PERSONAS_SCRIPTS_1_2_3" /',
        '/ "competencias" /': '/ "script1_competencias" /',
        '/ "tech_specs" /': '/ "script2_tech_specs" /',
        '/ "tasktodo" /': '/ "script4_tasktodo" /',
        'competencias_core.json': 'competencias_core.json',  # Mantém
        'ai_config.json': 'ai_config.json',  # Mantém
        'tools_config.json': 'tools_config.json'  # Mantém
    }
    
    # Aplicar substituições
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Atualizar carregamento de dados do tasktodo
    old_load_tasktodo = '''# Carregar análise de fluxos JSON
            fluxos_path = self.output_dir / "tasktodo" / categoria / persona_name.lower() / "fluxos_analysis.json"'''
    
    new_load_tasktodo = '''# Carregar análise de fluxos JSON da pasta da persona
            persona_path = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name
            fluxos_path = persona_path / "script4_tasktodo" / "fluxos_analysis.json"'''
    
    content = content.replace(old_load_tasktodo, new_load_tasktodo)
    
    # Atualizar descoberta de personas
    old_discovery = '''# Descobrir personas disponíveis (estrutura hierárquica)
    personas = []
    for categoria_dir in tasktodo_dir.iterdir():
        if categoria_dir.is_dir():
            for persona_dir in categoria_dir.iterdir():
                if persona_dir.is_dir():
                    personas.append(f"{categoria_dir.name}/{persona_dir.name}")'''
    
    new_discovery = '''# Descobrir personas disponíveis na nova estrutura
    personas_base_dir = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    personas = []
    for categoria_dir in personas_base_dir.iterdir():
        if categoria_dir.is_dir():
            for persona_dir in categoria_dir.iterdir():
                if persona_dir.is_dir():
                    # Verificar se tem script4_tasktodo
                    tasktodo_path = persona_dir / "script4_tasktodo"
                    if tasktodo_path.exists():
                        personas.append(f"{categoria_dir.name}/{persona_dir.name}")'''
    
    content = content.replace(old_discovery, new_discovery)
    
    # Atualizar local onde salva workflows - agora salva direto na pasta da persona
    old_workflow_save = '''# Criar diretório de workflows
        workflows_dir = self.output_dir / "05_WORKFLOWS_N8N"
        workflows_dir.mkdir(exist_ok=True)
        
        # Extrair nome limpo da persona (sem categoria)
        persona_name = persona_path.split('/')[-1]  # pega só o nome final
        
        # Salvar workflow
        workflow_path = workflows_dir / f"workflow_{persona_name.lower()}.json"'''
    
    new_workflow_save = '''# Extrair informações da persona
        parts = persona_path.split('/')
        categoria = parts[0] 
        persona_name = parts[1]
        
        # Salvar workflow dentro da pasta da persona
        persona_dir = self.output_dir / "04_PERSONAS_SCRIPTS_1_2_3" / categoria / persona_name
        workflows_dir = persona_dir / "script5_workflows_n8n"
        workflows_dir.mkdir(exist_ok=True)
        
        # Salvar workflow
        workflow_path = workflows_dir / f"workflow_{persona_name.lower()}.json"'''
    
    content = content.replace(old_workflow_save, new_workflow_save)
    
    # Salvar arquivo atualizado
    with open(script5_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ Script 5 atualizado")

if __name__ == "__main__":
    update_scripts_for_new_structure()