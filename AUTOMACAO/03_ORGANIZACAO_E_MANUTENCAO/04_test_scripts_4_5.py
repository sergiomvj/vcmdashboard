#!/usr/bin/env python3
"""
TESTE COMPLETO - SCRIPTS 4 e 5
Análise de Fluxos + Geração de Workflows N8N
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script4_test():
    """Testa o Script 4 - Análise de Fluxos"""
    print("🚀 TESTANDO SCRIPT 4 - ANÁLISE DE FLUXOS")
    print("=" * 50)
    
    # Diretório de teste
    output_dir = r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\Carntrack\carntrack_carnivore_diet_system"
    
    # Verificar se existe o diretório
    if not os.path.exists(output_dir):
        print(f"❌ Diretório não encontrado: {output_dir}")
        return False
    
    try:
        # Executar Script 4
        result = subprocess.run([
            sys.executable, 
            r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\VIRTUAL_COMPANY_GENERATOR\core\generate_fluxos_analise.py"
        ], 
        input=output_dir + "\n",
        text=True,
        capture_output=True,
        timeout=300
        )
        
        print("📤 OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORS:")
            print(result.stderr)
        
        # Verificar se pasta tasktodo foi criada
        tasktodo_dir = Path(output_dir) / "tasktodo"
        if tasktodo_dir.exists():
            personas = list(tasktodo_dir.iterdir())
            print(f"✅ Pasta tasktodo criada com {len(personas)} personas")
            
            # Verificar alguns arquivos
            for persona_dir in personas[:2]:  # Testar primeiras 2 personas
                tasktodo_file = persona_dir / "tasktodo.md"
                analysis_file = persona_dir / "fluxos_analysis.json"
                
                if tasktodo_file.exists() and analysis_file.exists():
                    print(f"✅ {persona_dir.name}: TaskTodo e Analysis criados")
                else:
                    print(f"❌ {persona_dir.name}: Arquivos faltando")
            
            return True
        else:
            print("❌ Pasta tasktodo não foi criada")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar Script 4: {e}")
        return False

def run_script5_test():
    """Testa o Script 5 - Workflows N8N"""
    print("\n🚀 TESTANDO SCRIPT 5 - WORKFLOWS N8N")
    print("=" * 50)
    
    # Diretório de teste
    output_dir = r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\Carntrack\carntrack_carnivore_diet_system"
    
    try:
        # Executar Script 5
        result = subprocess.run([
            sys.executable, 
            r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\VIRTUAL_COMPANY_GENERATOR\core\generate_workflows_n8n.py"
        ], 
        input=output_dir + "\n",
        text=True,
        capture_output=True,
        timeout=300
        )
        
        print("📤 OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ ERRORS:")
            print(result.stderr)
        
        # Verificar se workflows foram criados
        workflows_dir = Path(output_dir) / "05_WORKFLOWS_N8N"
        if workflows_dir.exists():
            workflows = list(workflows_dir.glob("workflow_*.json"))
            validations = list(workflows_dir.glob("validation_*.json"))
            readmes = list(workflows_dir.glob("README_*.md"))
            
            print(f"✅ Workflows criados: {len(workflows)}")
            print(f"✅ Validações criadas: {len(validations)}")
            print(f"✅ READMEs criados: {len(readmes)}")
            
            return len(workflows) > 0
        else:
            print("❌ Pasta de workflows não foi criada")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar Script 5: {e}")
        return False

def main():
    """Executa teste completo dos Scripts 4 e 5"""
    print("🎯 TESTE COMPLETO - SCRIPTS 4 e 5")
    print("📋 Análise de Fluxos + Workflows N8N")
    print("=" * 60)
    
    # Mudar para diretório do projeto
    os.chdir(Path(__file__).parent.parent)
    
    # Teste Script 4
    script4_success = run_script4_test()
    
    # Teste Script 5 (apenas se Script 4 passou)
    script5_success = False
    if script4_success:
        script5_success = run_script5_test()
    else:
        print("\n❌ Pulando Script 5 - Script 4 falhou")
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    print(f"Script 4 (Análise de Fluxos): {'✅ PASSOU' if script4_success else '❌ FALHOU'}")
    print(f"Script 5 (Workflows N8N): {'✅ PASSOU' if script5_success else '❌ FALHOU'}")
    
    if script4_success and script5_success:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("🔄 Sistema completo de Scripts 1-5 funcionando!")
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        print("🔍 Verifique os logs acima para detalhes")

if __name__ == "__main__":
    main()