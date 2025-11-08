#!/usr/bin/env python3
"""
REORGANIZAÇÃO COMPLETA DA ESTRUTURA DE PASTAS
Organiza tudo por sequência de scripts e mantém documentos por persona
"""

import os
import shutil
from pathlib import Path
import json

def reorganize_structure():
    """Reorganiza toda a estrutura de pastas"""
    
    base_dir = Path(r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\Carntrack\carntrack_carnivore_diet_system")
    
    print("🔄 REORGANIZANDO ESTRUTURA COMPLETA...")
    print("=" * 50)
    
    # 1. Renomear pastas principais na sequência dos scripts
    rename_mappings = {
        "01_DOCUMENTACAO": "01_DOCUMENTACAO_GERAL",
        "02_SCRIPTS": "02_SCRIPTS_AUTOMACAO", 
        "03_N8N_WORKFLOWS": "03_WORKFLOWS_LEGADO",
        "04_PERSONAS_COMPLETAS": "04_PERSONAS_SCRIPTS_1_2_3",
        "05_WORKFLOWS_N8N": "TEMP_WORKFLOWS_N8N",  # Temporário
        "06_TEMPLATES": "05_TEMPLATES_SISTEMA",
        "07_RAG_KNOWLEDGE_BASE": "06_RAG_KNOWLEDGE_BASE", 
        "08_EMAIL_TEMPLATES": "07_EMAIL_TEMPLATES",
        "09_DATABASE_SCHEMAS": "08_DATABASE_SCHEMAS",
        "10_MONITORING": "09_MONITORING_LOGS"
    }
    
    # Renomear pastas principais
    for old_name, new_name in rename_mappings.items():
        old_path = base_dir / old_name
        new_path = base_dir / new_name
        
        if old_path.exists() and not new_path.exists():
            print(f"📁 Renomeando: {old_name} → {new_name}")
            old_path.rename(new_path)
    
    # 2. Criar nova estrutura para personas organizadas por scripts
    personas_dir = base_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    
    if personas_dir.exists():
        # Para cada categoria de persona
        for categoria_dir in personas_dir.iterdir():
            if categoria_dir.is_dir():
                # Para cada persona individual
                for persona_dir in categoria_dir.iterdir():
                    if persona_dir.is_dir():
                        reorganize_persona_folder(persona_dir, categoria_dir.name)
    
    # 3. Mover workflows para dentro de cada persona
    move_workflows_to_personas(base_dir)
    
    # 4. Mover tasktodo para dentro de cada persona
    move_tasktodo_to_personas(base_dir)
    
    # 5. Organizar Templates
    organize_templates_folder(base_dir)
    
    # 6. Limpar pasta temporária
    temp_workflows = base_dir / "TEMP_WORKFLOWS_N8N"
    if temp_workflows.exists():
        shutil.rmtree(temp_workflows)
        print("🗑️ Removendo pasta temporária de workflows")
    
    print("\n✅ REORGANIZAÇÃO COMPLETA FINALIZADA!")
    print_final_structure(base_dir)

def reorganize_persona_folder(persona_dir, categoria):
    """Reorganiza pasta de uma persona individual"""
    
    persona_name = persona_dir.name
    print(f"📋 Reorganizando {categoria}/{persona_name}...")
    
    # Criar estrutura sequencial dentro da persona
    script_folders = {
        "script1_competencias": "competencias",
        "script2_tech_specs": "tech_specs", 
        "script3_rag": "rag",
        "script4_tasktodo": None,  # Será criada depois
        "script5_workflows_n8n": None  # Será criada depois
    }
    
    # Renomear pastas existentes para seguir sequência
    for new_folder, old_folder in script_folders.items():
        if old_folder and (persona_dir / old_folder).exists():
            old_path = persona_dir / old_folder
            new_path = persona_dir / new_folder
            
            if not new_path.exists():
                old_path.rename(new_path)
                print(f"   📁 {old_folder} → {new_folder}")

def move_workflows_to_personas(base_dir):
    """Move workflows para dentro de cada pasta de persona"""
    
    workflows_dir = base_dir / "TEMP_WORKFLOWS_N8N" 
    personas_dir = base_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    
    if not workflows_dir.exists():
        return
    
    print("\n🔄 Movendo workflows para pastas das personas...")
    
    # Mapear arquivos de workflow para personas
    for workflow_file in workflows_dir.glob("workflow_*.json"):
        persona_name = workflow_file.stem.replace("workflow_", "")
        
        # Encontrar pasta da persona correspondente
        persona_path = find_persona_path(personas_dir, persona_name)
        
        if persona_path:
            # Criar pasta script5_workflows_n8n se não existir
            script5_dir = persona_path / "script5_workflows_n8n"
            script5_dir.mkdir(exist_ok=True)
            
            # Mover todos os arquivos relacionados (workflow, validation, README)
            files_to_move = [
                workflows_dir / f"workflow_{persona_name}.json",
                workflows_dir / f"validation_{persona_name}.json", 
                workflows_dir / f"README_{persona_name}.md"
            ]
            
            for file_path in files_to_move:
                if file_path.exists():
                    dest_path = script5_dir / file_path.name
                    shutil.move(str(file_path), str(dest_path))
                    print(f"   📄 {file_path.name} → {persona_path.name}/script5_workflows_n8n/")

def move_tasktodo_to_personas(base_dir):
    """Move tasktodo para dentro de cada pasta de persona"""
    
    tasktodo_dir = base_dir / "tasktodo"  # Pode estar na raiz ou em 05_TASKTODO
    if not tasktodo_dir.exists():
        tasktodo_dir = base_dir / "05_TASKTODO"
    
    personas_dir = base_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    
    if not tasktodo_dir.exists():
        return
        
    print("\n🔄 Movendo tasktodo para pastas das personas...")
    
    # Para cada categoria no tasktodo
    for categoria_dir in tasktodo_dir.iterdir():
        if categoria_dir.is_dir():
            # Para cada persona no tasktodo
            for persona_tasktodo_dir in categoria_dir.iterdir():
                if persona_tasktodo_dir.is_dir():
                    persona_name = persona_tasktodo_dir.name
                    
                    # Encontrar pasta da persona correspondente
                    persona_path = find_persona_path(personas_dir, persona_name)
                    
                    if persona_path:
                        # Criar pasta script4_tasktodo se não existir
                        script4_dir = persona_path / "script4_tasktodo"
                        script4_dir.mkdir(exist_ok=True)
                        
                        # Mover arquivos tasktodo
                        for file_path in persona_tasktodo_dir.iterdir():
                            if file_path.is_file():
                                dest_path = script4_dir / file_path.name
                                shutil.move(str(file_path), str(dest_path))
                                print(f"   📄 {file_path.name} → {persona_path.name}/script4_tasktodo/")
    
    # Remover pasta tasktodo vazia
    if tasktodo_dir.exists():
        shutil.rmtree(tasktodo_dir)
        print("🗑️ Removendo pasta tasktodo da raiz")

def find_persona_path(personas_dir, persona_name):
    """Encontra o caminho de uma persona pelo nome"""
    
    for categoria_dir in personas_dir.iterdir():
        if categoria_dir.is_dir():
            for persona_dir in categoria_dir.iterdir():
                if persona_dir.is_dir():
                    # Comparar nomes (ignorando case e caracteres especiais)
                    if normalize_name(persona_dir.name) == normalize_name(persona_name):
                        return persona_dir
    return None

def normalize_name(name):
    """Normaliza nome para comparação"""
    return name.lower().replace("_", " ").replace("-", " ").strip()

def organize_templates_folder(base_dir):
    """Organiza pasta de templates"""
    
    templates_dir = base_dir / "05_TEMPLATES_SISTEMA"
    
    if templates_dir.exists():
        print("\n📋 Organizando pasta TEMPLATES...")
        
        # Criar subpastas organizadas
        template_structure = {
            "biografia_templates": "Templates para biografias de personas",
            "competencias_templates": "Templates do Script 1 - Competências", 
            "tech_specs_templates": "Templates do Script 2 - Tech Specs",
            "rag_templates": "Templates do Script 3 - RAG",
            "tasktodo_templates": "Templates do Script 4 - TaskTodo",
            "workflow_templates": "Templates do Script 5 - Workflows N8N",
            "email_templates": "Templates de email",
            "documento_templates": "Templates de documentos"
        }
        
        for folder_name, description in template_structure.items():
            folder_path = templates_dir / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # Criar README em cada pasta de template
            readme_path = folder_path / "README.md"
            if not readme_path.exists():
                readme_content = f"""# {folder_name.replace('_', ' ').title()}

## Descrição
{description}

## Como usar
1. Copie os templates necessários
2. Personalize conforme sua necessidade
3. Use nos scripts correspondentes

## Templates disponíveis
- (Adicionar templates conforme necessário)
"""
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(readme_content)
        
        print("   ✅ Estrutura de templates organizadas")

def print_final_structure(base_dir):
    """Imprime estrutura final organizada"""
    
    print("\n" + "=" * 60)
    print("📁 ESTRUTURA FINAL ORGANIZADA")
    print("=" * 60)
    
    structure = """
📂 carntrack_carnivore_diet_system/
├── 📂 01_DOCUMENTACAO_GERAL/
├── 📂 02_SCRIPTS_AUTOMACAO/
├── 📂 03_WORKFLOWS_LEGADO/
├── 📂 04_PERSONAS_SCRIPTS_1_2_3/
│   ├── 📂 assistentes/
│   │   ├── 📂 Daniela_Alvarez/
│   │   │   ├── 📄 Daniela_Alvarez_bio.md
│   │   │   ├── 📂 script1_competencias/
│   │   │   ├── 📂 script2_tech_specs/
│   │   │   ├── 📂 script3_rag/
│   │   │   ├── 📂 script4_tasktodo/
│   │   │   └── 📂 script5_workflows_n8n/
│   │   └── 📂 [outras assistentes...]
│   ├── 📂 executivos/
│   ├── 📂 especialistas/
│   └── 📂 suporte/
├── 📂 05_TEMPLATES_SISTEMA/
│   ├── 📂 biografia_templates/
│   ├── 📂 competencias_templates/
│   ├── 📂 tech_specs_templates/
│   ├── 📂 rag_templates/
│   ├── 📂 tasktodo_templates/
│   ├── 📂 workflow_templates/
│   ├── 📂 email_templates/
│   └── 📂 documento_templates/
├── 📂 06_RAG_KNOWLEDGE_BASE/
├── 📂 07_EMAIL_TEMPLATES/
├── 📂 08_DATABASE_SCHEMAS/
└── 📂 09_MONITORING_LOGS/
    """
    
    print(structure)
    print("\n🎯 VANTAGENS DA NOVA ESTRUTURA:")
    print("✅ Pastas numeradas na sequência dos scripts")
    print("✅ Tudo de cada persona em uma única pasta")
    print("✅ Scripts organizados sequencialmente dentro de cada persona")
    print("✅ Templates bem organizados por categoria")
    print("✅ Fácil navegação e localização")

if __name__ == "__main__":
    reorganize_structure()