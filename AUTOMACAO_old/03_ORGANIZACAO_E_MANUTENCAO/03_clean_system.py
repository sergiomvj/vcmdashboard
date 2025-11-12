#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Limpeza Completa - VIRTUAL_COMPANY_GENERATOR
Remove todo o lixo de testes e deixa apenas os arquivos essenciais
"""

import os
import shutil
from pathlib import Path

def clean_virtual_company_generator():
    """Execute limpeza completa do sistema"""
    
    # Pasta base
    base_path = Path("C:/Users/Sergio Castro/Documents/Projetos/1NewTools/VIRTUAL_COMPANY_GENERATOR")
    
    if not base_path.exists():
        print(f"❌ Pasta não encontrada: {base_path}")
        return False
    
    print("🧹 INICIANDO LIMPEZA COMPLETA")
    print("=" * 50)
    
    # Arquivos essenciais (não deletar)
    essential_files = {
        "README.md",
        "core/create_project_template.py", 
        "core/project_company_generator.py"
    }
    
    # Converter para caminhos absolutos
    essential_paths = {base_path / file for file in essential_files}
    
    removed_count = 0
    
    # 1. Remover pastas desnecessárias completamente
    folders_to_remove = [
        "config",
        "logs", 
        "output",
        "templates",
        "core/__pycache__"
    ]
    
    for folder in folders_to_remove:
        folder_path = base_path / folder
        if folder_path.exists():
            try:
                shutil.rmtree(folder_path)
                print(f"🗑️  Pasta removida: {folder}/")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {folder}: {e}")
    
    # 2. Remover arquivos desnecessários na raiz
    root_files_to_remove = [
        "DEMONSTRACAO_EASY123.md",
        "DEMONSTRACAO_EASY123_CORRIGIDA.md", 
        "generate_company.bat",
        "GUIA_EASY123.md",
        "LOCALIZACAO_ARQUIVOS_EASY123.md",
        "ORGANIZACAO_POR_PROJETO.md",
        "SISTEMA_MASTER_PRONTO.md",
        "AUDITORIA_LIMPEZA.md"  # Remove a própria auditoria após usar
    ]
    
    for file in root_files_to_remove:
        file_path = base_path / file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️  Arquivo removido: {file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover {file}: {e}")
    
    # 3. Remover arquivos desnecessários em core/
    core_files_to_remove = [
        "migrate_existing.py",
        "setup_project_generator.py", 
        "virtual_company_generator.py"
    ]
    
    for file in core_files_to_remove:
        file_path = base_path / "core" / file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️  Arquivo removido: core/{file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Erro ao remover core/{file}: {e}")
    
    # 4. Criar README.md limpo se não existir
    readme_path = base_path / "README.md"
    if not readme_path.exists():
        readme_content = """# Virtual Company Generator

Sistema para criar empresas virtuais com 16 personas organizacionais dentro de projetos específicos.

## 🚀 Como Usar

### 1. Criar Template de Projeto
```bash
cd core/
python create_project_template.py "C:\\Caminho\\Para\\SeuProjeto"
```

### 2. Gerar Empresa no Projeto  
```bash
cd "C:\\Caminho\\Para\\SeuProjeto"
python create_virtual_company.py
```

### 3. Resultado
```
SeuProjeto/
└── SuaEmpresa_virtual_company/
    ├── config/
    ├── personas/ (16 personas)
    ├── workflows/
    ├── docs/
    └── logs/
```

## 📁 Estrutura

```
VIRTUAL_COMPANY_GENERATOR/
├── README.md                        (este arquivo)
└── core/
    ├── create_project_template.py   (cria template no projeto)
    └── project_company_generator.py (motor de geração)
```

## ✨ Características

- ✅ Empresa criada DENTRO do projeto
- ✅ 16 personas organizacionais
- ✅ Sistema autocontido
- ✅ Sem dependências externas
- ✅ Múltiplos setores suportados
"""
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("📝 README.md criado/atualizado")
    
    # 5. Verificar arquivos restantes
    print("\n" + "=" * 50)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("=" * 50)
    print(f"🗑️  Itens removidos: {removed_count}")
    
    print("\n📁 Estrutura final:")
    remaining_files = []
    for root, dirs, files in os.walk(base_path):
        # Filtrar __pycache__ da listagem
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            file_path = Path(root) / file
            relative_path = file_path.relative_to(base_path)
            remaining_files.append(str(relative_path))
    
    remaining_files.sort()
    
    for file in remaining_files:
        print(f"  ✅ {file}")
    
    print(f"\n📊 Total de arquivos restantes: {len(remaining_files)}")
    
    if len(remaining_files) <= 5:
        print("🎉 Sistema ultra-limpo! Apenas arquivos essenciais.")
    else:
        print("⚠️  Ainda existem mais arquivos que o esperado.")
    
    return True

def main():
    """Função principal com confirmação"""
    print("🚨 ATENÇÃO: Esta operação irá DELETAR permanentemente arquivos!")
    print("📋 Será mantido apenas:")
    print("   - README.md")
    print("   - core/create_project_template.py")
    print("   - core/project_company_generator.py")
    print()
    
    response = input("Tem certeza que quer continuar? (digite 'SIM' para confirmar): ")
    
    if response.upper() == 'SIM':
        clean_virtual_company_generator()
    else:
        print("❌ Operação cancelada.")

if __name__ == "__main__":
    main()