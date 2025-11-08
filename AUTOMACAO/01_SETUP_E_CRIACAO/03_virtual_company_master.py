#!/usr/bin/env python3
"""
VIRTUAL COMPANY GENERATOR - MASTER COMPLETO
Sistema integrado para geração de empresas virtuais com template limpo
"""

import os
import shutil
from pathlib import Path
import subprocess
import sys

def main_menu():
    """Menu principal do sistema"""
    
    print("🚀 VIRTUAL COMPANY GENERATOR MASTER v2.0.0")
    print("=" * 60)
    print("Sistema Completo de Geração de Empresas Virtuais")
    print("")
    
    while True:
        print("📋 OPÇÕES DISPONÍVEIS:")
        print("1. 🏗️  Criar Nova Empresa Virtual (Template Limpo)")
        print("2. ⚡ Executar Scripts em Empresa Existente")
        print("3. 🔍 Validar Estrutura de Empresa")
        print("4. 📊 Status de Empresa Virtual")
        print("5. 🎨 Gerenciar Templates")
        print("6. ❌ Sair")
        print("")
        
        choice = input("Escolha uma opção (1-6): ").strip()
        
        if choice == "1":
            create_new_company()
        elif choice == "2":
            run_scripts_on_company()
        elif choice == "3":
            validate_company_structure()
        elif choice == "4":
            show_company_status()
        elif choice == "5":
            manage_templates()
        elif choice == "6":
            print("👋 Saindo do Virtual Company Generator...")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")
        print("\n" + "=" * 60)

def create_new_company():
    """Cria nova empresa virtual usando template limpo"""
    
    print("\n🏗️ CRIAR NOVA EMPRESA VIRTUAL")
    print("=" * 50)
    
    # Template limpo
    template_source = Path(r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\VIRTUAL_COMPANY_TEMPLATE_CLEAN")
    
    if not template_source.exists():
        print("❌ Template limpo não encontrado!")
        print("Execute 'python create_clean_template.py' primeiro.")
        return
    
    # Coletar informações da nova empresa
    company_name = input("📋 Nome da empresa (sem espaços): ").strip().replace(" ", "_")
    if not company_name:
        print("❌ Nome da empresa é obrigatório!")
        return
    
    # Definir pasta de destino
    base_dir = Path(r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools")
    company_dir = base_dir / f"EMPRESA_{company_name.upper()}"
    
    if company_dir.exists():
        print(f"❌ Empresa {company_name} já existe em: {company_dir}")
        return
    
    try:
        # Copiar template
        print(f"📁 Copiando template para: {company_dir}")
        shutil.copytree(template_source, company_dir)
        
        # Executar inicializador
        print("🔧 Executando inicializador...")
        os.chdir(company_dir)
        
        # Executar initialize_company.py se existir
        init_script = company_dir / "initialize_company.py"
        if init_script.exists():
            subprocess.run([sys.executable, str(init_script)], check=True)
        
        print(f"\n✅ EMPRESA {company_name} CRIADA COM SUCESSO!")
        print(f"📁 Localização: {company_dir}")
        print(f"📖 Consulte o README.md para próximos passos")
        
        # Voltar ao diretório original
        os.chdir(Path(__file__).parent)
        
    except Exception as e:
        print(f"❌ Erro ao criar empresa: {e}")

def run_scripts_on_company():
    """Executa scripts em empresa existente"""
    
    print("\n⚡ EXECUTAR SCRIPTS EM EMPRESA")
    print("=" * 50)
    
    # Solicitar pasta da empresa
    company_path = input("📁 Caminho completo da empresa: ").strip()
    
    if not company_path:
        print("❌ Caminho da empresa é obrigatório!")
        return
    
    company_dir = Path(company_path)
    if not company_dir.exists():
        print(f"❌ Empresa não encontrada: {company_dir}")
        return
    
    # Verificar estrutura
    personas_dir = company_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    if not personas_dir.exists():
        print("❌ Estrutura de personas não encontrada!")
        return
    
    # Menu de scripts
    while True:
        print("\n📋 SCRIPTS DISPONÍVEIS:")
        print("1. Script 1 - Competências")
        print("2. Script 2 - Tech Specs") 
        print("3. Script 3 - RAG Knowledge Base")
        print("4. Script 4 - TaskTodo Analysis")
        print("5. Script 5 - Workflows N8N")
        print("6. 🚀 Executar TODOS os scripts (1-5)")
        print("7. ⬅️ Voltar ao menu principal")
        
        choice = input("\nEscolha um script (1-7): ").strip()
        
        if choice == "7":
            break
        elif choice in ["1", "2", "3", "4", "5"]:
            run_single_script(choice, company_path)
        elif choice == "6":
            run_all_scripts(company_path)
        else:
            print("❌ Opção inválida!")

def run_single_script(script_num, company_path):
    """Executa um script específico"""
    
    scripts_map = {
        "1": "generate_competencias.py",
        "2": "generate_tech_specs.py", 
        "3": "generate_rag.py",
        "4": "generate_fluxos_analise.py",
        "5": "generate_workflows_n8n.py"
    }
    
    script_names = {
        "1": "Competências",
        "2": "Tech Specs",
        "3": "RAG Knowledge Base", 
        "4": "TaskTodo Analysis",
        "5": "Workflows N8N"
    }
    
    script_file = scripts_map.get(script_num)
    script_name = script_names.get(script_num)
    
    if not script_file:
        print("❌ Script inválido!")
        return
    
    print(f"\n⚡ Executando Script {script_num} - {script_name}...")
    
    # Caminho do script
    core_dir = Path(__file__).parent / "core"
    script_path = core_dir / script_file
    
    if not script_path.exists():
        print(f"❌ Script não encontrado: {script_path}")
        return
    
    try:
        # Executar script com input do caminho da empresa
        result = subprocess.run(
            [sys.executable, str(script_path)], 
            input=company_path + "\n",
            text=True,
            capture_output=True,
            timeout=300
        )
        
        print("📤 OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ AVISOS/ERROS:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ Script {script_num} executado com sucesso!")
        else:
            print(f"❌ Script {script_num} falhou com código: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏱️ Script excedeu tempo limite de 5 minutos!")
    except Exception as e:
        print(f"❌ Erro ao executar script: {e}")

def run_all_scripts(company_path):
    """Executa todos os scripts sequencialmente"""
    
    print(f"\n🚀 EXECUTANDO TODOS OS SCRIPTS SEQUENCIALMENTE...")
    print("=" * 50)
    
    scripts = ["1", "2", "3", "4", "5"]
    
    for script_num in scripts:
        print(f"\n📋 Executando Script {script_num}...")
        run_single_script(script_num, company_path)
        
        # Pausa entre scripts
        input(f"Script {script_num} concluído. Pressione Enter para continuar...")
    
    print("\n🎉 TODOS OS SCRIPTS EXECUTADOS!")

def validate_company_structure():
    """Valida estrutura de empresa"""
    
    print("\n🔍 VALIDAR ESTRUTURA DE EMPRESA")
    print("=" * 50)
    
    company_path = input("📁 Caminho completo da empresa: ").strip()
    
    if not company_path:
        print("❌ Caminho da empresa é obrigatório!")
        return
    
    company_dir = Path(company_path)
    if not company_dir.exists():
        print(f"❌ Empresa não encontrada: {company_dir}")
        return
    
    # Executar validador se existir
    validator_script = company_dir / "validate_structure.py"
    
    if validator_script.exists():
        try:
            os.chdir(company_dir)
            subprocess.run([sys.executable, str(validator_script)], check=True)
            os.chdir(Path(__file__).parent)
        except Exception as e:
            print(f"❌ Erro ao executar validador: {e}")
    else:
        print("❌ Script de validação não encontrado na empresa!")

def show_company_status():
    """Mostra status de empresa"""
    
    print("\n📊 STATUS DE EMPRESA VIRTUAL")
    print("=" * 50)
    
    company_path = input("📁 Caminho completo da empresa: ").strip()
    
    if not company_path:
        print("❌ Caminho da empresa é obrigatório!")
        return
    
    company_dir = Path(company_path)
    if not company_dir.exists():
        print(f"❌ Empresa não encontrada: {company_dir}")
        return
    
    # Análise básica
    personas_dir = company_dir / "04_PERSONAS_SCRIPTS_1_2_3"
    
    if not personas_dir.exists():
        print("❌ Estrutura de personas não encontrada!")
        return
    
    # Contar personas por categoria
    categories = {}
    total_personas = 0
    
    for category_dir in personas_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.endswith('_exemplo'):
            personas = [d for d in category_dir.iterdir() if d.is_dir()]
            categories[category_dir.name] = len(personas)
            total_personas += len(personas)
    
    # Verificar scripts executados
    scripts_status = check_scripts_status(personas_dir)
    
    # Relatório
    print(f"\n📋 EMPRESA: {company_dir.name}")
    print(f"📁 Localização: {company_dir}")
    print(f"\n👥 PERSONAS POR CATEGORIA:")
    
    for category, count in categories.items():
        print(f"   📂 {category}: {count} personas")
    
    print(f"\n📊 Total de personas: {total_personas}")
    
    print(f"\n⚡ STATUS DOS SCRIPTS:")
    for script_num, status in scripts_status.items():
        status_icon = "✅" if status["completed"] > 0 else "❌"
        print(f"   {status_icon} Script {script_num}: {status['completed']}/{status['total']} personas")

def check_scripts_status(personas_dir):
    """Verifica status de execução dos scripts"""
    
    scripts_status = {
        "1": {"completed": 0, "total": 0},
        "2": {"completed": 0, "total": 0}, 
        "3": {"completed": 0, "total": 0},
        "4": {"completed": 0, "total": 0},
        "5": {"completed": 0, "total": 0}
    }
    
    script_folders = {
        "1": "script1_competencias",
        "2": "script2_tech_specs",
        "3": "script3_rag", 
        "4": "script4_tasktodo",
        "5": "script5_workflows_n8n"
    }
    
    # Contar personas e verificar scripts
    for category_dir in personas_dir.iterdir():
        if category_dir.is_dir() and not category_dir.name.endswith('_exemplo'):
            for persona_dir in category_dir.iterdir():
                if persona_dir.is_dir():
                    # Atualizar total
                    for script_num in scripts_status:
                        scripts_status[script_num]["total"] += 1
                    
                    # Verificar se scripts foram executados
                    for script_num, folder_name in script_folders.items():
                        script_dir = persona_dir / folder_name
                        if script_dir.exists() and any(script_dir.iterdir()):
                            scripts_status[script_num]["completed"] += 1
    
    return scripts_status

def manage_templates():
    """Gerencia templates do sistema"""
    
    print("\n🎨 GERENCIAR TEMPLATES")
    print("=" * 50)
    
    print("🚧 Funcionalidade em desenvolvimento...")
    print("📋 Templates disponíveis em: 05_TEMPLATES_SISTEMA/")
    print("📖 Consulte a documentação para uso manual dos templates")

if __name__ == "__main__":
    main_menu()