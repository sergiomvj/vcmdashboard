#!/usr/bin/env python3
"""
CRIADOR DE TEMPLATE LIMPO PARA NOVAS EMPRESAS VIRTUAIS
Cria estrutura organizada baseada no sistema reorganizado do Carntrack
"""

import os
import shutil
from pathlib import Path
import json

def create_clean_template():
    """Cria template limpo para novas empresas virtuais"""
    
    print("🚀 CRIANDO TEMPLATE LIMPO PARA NOVAS EMPRESAS VIRTUAIS")
    print("=" * 60)
    
    # Definir pasta de destino (fora do projeto atual)
    template_dir = Path(r"C:\Users\Sergio Castro\Documents\Projetos\1NewTools\VIRTUAL_COMPANY_TEMPLATE_CLEAN")
    
    # Remover se já existir
    if template_dir.exists():
        shutil.rmtree(template_dir)
        print(f"🗑️ Removendo template existente")
    
    # Criar estrutura base
    create_base_structure(template_dir)
    
    # Criar templates de exemplo
    create_example_templates(template_dir)
    
    # Criar documentação
    create_template_documentation(template_dir)
    
    # Criar scripts de geração
    create_generation_scripts(template_dir)
    
    print(f"\n✅ TEMPLATE LIMPO CRIADO COM SUCESSO!")
    print(f"📁 Localização: {template_dir}")
    print_template_structure()

def create_base_structure(template_dir):
    """Cria estrutura de pastas base"""
    
    print("\n📂 Criando estrutura de pastas...")
    
    # Estrutura principal
    folders = [
        "01_DOCUMENTACAO_GERAL",
        "02_SCRIPTS_AUTOMACAO", 
        "03_WORKFLOWS_LEGADO",
        "04_PERSONAS_SCRIPTS_1_2_3",
        "04_PERSONAS_SCRIPTS_1_2_3/assistentes_exemplo",
        "04_PERSONAS_SCRIPTS_1_2_3/executivos_exemplo", 
        "04_PERSONAS_SCRIPTS_1_2_3/especialistas_exemplo",
        "04_PERSONAS_SCRIPTS_1_2_3/suporte_exemplo",
        "05_TEMPLATES_SISTEMA",
        "05_TEMPLATES_SISTEMA/biografia_templates",
        "05_TEMPLATES_SISTEMA/competencias_templates",
        "05_TEMPLATES_SISTEMA/tech_specs_templates", 
        "05_TEMPLATES_SISTEMA/rag_templates",
        "05_TEMPLATES_SISTEMA/tasktodo_templates",
        "05_TEMPLATES_SISTEMA/workflow_templates",
        "05_TEMPLATES_SISTEMA/email_templates",
        "05_TEMPLATES_SISTEMA/documento_templates",
        "06_RAG_KNOWLEDGE_BASE",
        "07_EMAIL_TEMPLATES",
        "08_DATABASE_SCHEMAS", 
        "09_MONITORING_LOGS"
    ]
    
    # Criar todas as pastas
    for folder in folders:
        folder_path = template_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"   📁 {folder}")
    
    print("   ✅ Estrutura de pastas criada")

def create_example_templates(template_dir):
    """Cria templates de exemplo"""
    
    print("\n📋 Criando templates de exemplo...")
    
    # Template de biografia
    bio_template = """# BIOGRAFIA - [NOME DA PERSONA]

## 📋 INFORMAÇÕES BÁSICAS
**Nome**: [Nome Completo]
**Cargo/Função**: [Título Profissional]  
**Departamento**: [Departamento/Área]
**Empresa**: [Nome da Empresa]
**Localização**: [Cidade, País]
**Experiência**: [X anos na área]

## 👤 PERFIL PROFISSIONAL

### Background Acadêmico
- [Formação 1]
- [Formação 2]
- [Certificações relevantes]

### Experiência Profissional
- [Cargo anterior 1] - [Empresa] ([Período])
- [Cargo anterior 2] - [Empresa] ([Período])
- [Cargo atual] - [Empresa atual] ([Período atual])

### Competências Técnicas
- [Competência técnica 1]
- [Competência técnica 2] 
- [Competência técnica 3]
- [Competência técnica 4]

### Competências Comportamentais  
- [Soft skill 1]
- [Soft skill 2]
- [Soft skill 3]

## 🎯 RESPONSABILIDADES E OBJETIVOS

### Responsabilidades Principais
1. [Responsabilidade estratégica 1]
2. [Responsabilidade operacional 2] 
3. [Responsabilidade de gestão 3]

### Objetivos de Curto Prazo (3 meses)
- [Objetivo operacional 1]
- [Objetivo operacional 2]

### Objetivos de Médio Prazo (6-12 meses)
- [Objetivo tático 1]
- [Objetivo tático 2] 

### Objetivos de Longo Prazo (1+ anos)
- [Objetivo estratégico 1]
- [Objetivo estratégico 2]

## 📅 ROTINA DE TRABALHO

### Tarefas Diárias (Operacionais)
- [Tarefa diária 1 - ex: Verificar emails e responder solicitações urgentes]
- [Tarefa diária 2 - ex: Monitorar KPIs principais]
- [Tarefa diária 3 - ex: Atualizar status de projetos]
- [Tarefa diária 4]
- [Tarefa diária 5]

### Tarefas Semanais (Táticas)
- [Tarefa semanal 1 - ex: Reunião de equipe e planejamento semanal]
- [Tarefa semanal 2 - ex: Análise de relatórios e métricas]
- [Tarefa semanal 3 - ex: Revisão de processos e melhorias]
- [Tarefa semanal 4]

### Tarefas Mensais (Estratégicas)
- [Tarefa mensal 1 - ex: Planejamento estratégico e definição de metas]
- [Tarefa mensal 2 - ex: Avaliação de performance e resultados]
- [Tarefa mensal 3 - ex: Reuniões com stakeholders]

## 🔧 FERRAMENTAS E TECNOLOGIAS
### Software Utilizado
- [Software 1 - ex: Microsoft Office 365]
- [Software 2 - ex: CRM Salesforce]
- [Software 3 - ex: Slack para comunicação]

### Plataformas e Sistemas
- [Plataforma 1]
- [Sistema 2]
- [Ferramenta 3]

## 📊 MÉTRICAS E KPIS
### KPIs Principais
- [KPI 1 - ex: Taxa de satisfação do cliente]
- [KPI 2 - ex: Produtividade da equipe]
- [KPI 3 - ex: ROI de projetos]

### Métricas Secundárias
- [Métrica 1]
- [Métrica 2]

## 🤝 RELACIONAMENTOS PROFISSIONAIS
### Reporta para
- [Nome/Cargo do superior direto]

### Gerencia
- [Subordinado 1]
- [Subordinado 2]

### Colabora com
- [Departamento/Equipe 1]
- [Parceiro interno 2]
- [Stakeholder externo 3]

## 🎭 DESAFIOS E OPORTUNIDADES
### Principais Desafios
1. [Desafio operacional 1]
2. [Desafio estratégico 2]
3. [Desafio de crescimento 3]

### Oportunidades de Melhoria
1. [Oportunidade de automação 1]
2. [Oportunidade de otimização 2] 
3. [Oportunidade de inovação 3]

## 💡 PROCESSOS AUTOMATIZÁVEIS
### Alta Prioridade
- [Processo repetitivo 1]
- [Processo manual 2]

### Média Prioridade  
- [Processo 3]
- [Processo 4]

### Baixa Prioridade
- [Processo 5]

---
*Template criado pelo Virtual Company Generator v2.0.0*
*Para usar: substitua todos os campos [entre colchetes] com informações específicas da persona*
"""

    # Salvar template de biografia
    bio_path = template_dir / "05_TEMPLATES_SISTEMA/biografia_templates/biografia_template.md"
    with open(bio_path, 'w', encoding='utf-8') as f:
        f.write(bio_template)
    
    # Template de persona exemplo
    persona_example_path = template_dir / "04_PERSONAS_SCRIPTS_1_2_3/assistentes_exemplo/Persona_Exemplo"
    persona_example_path.mkdir(parents=True, exist_ok=True)
    
    # Criar estrutura de exemplo para persona
    persona_folders = [
        "script1_competencias",
        "script2_tech_specs", 
        "script3_rag",
        "script4_tasktodo",
        "script5_workflows_n8n"
    ]
    
    for folder in persona_folders:
        (persona_example_path / folder).mkdir(exist_ok=True)
        
        # Criar README em cada pasta
        readme_content = f"""# {folder.upper()}

## Descrição
Esta pasta contém os outputs do {folder.replace('_', ' ').title()}.

## Arquivos esperados
- [Listar arquivos que serão gerados pelo script correspondente]

## Como usar
1. Execute o script correspondente
2. Os arquivos serão gerados automaticamente nesta pasta
3. Verifique os outputs para validar os resultados

---
*Gerado pelo Virtual Company Generator v2.0.0*
"""
        
        readme_path = persona_example_path / folder / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    # Biografia de exemplo
    bio_example = bio_template.replace("[NOME DA PERSONA]", "PERSONA EXEMPLO") \
                             .replace("[Nome Completo]", "Persona de Exemplo") \
                             .replace("[Título Profissional]", "Cargo Exemplo") \
                             .replace("[Departamento/Área]", "Departamento Exemplo")
    
    bio_example_path = persona_example_path / "Persona_Exemplo_bio.md"
    with open(bio_example_path, 'w', encoding='utf-8') as f:
        f.write(bio_example)
    
    print("   ✅ Templates de exemplo criados")

def create_template_documentation(template_dir):
    """Cria documentação do template"""
    
    print("\n📚 Criando documentação...")
    
    # README principal
    main_readme = """# 🏗️ VIRTUAL COMPANY TEMPLATE - ESTRUTURA LIMPA

## 📋 VISÃO GERAL
Este é um template limpo para criação de novas empresas virtuais usando o Virtual Company Generator v2.0.0.

**🎯 Baseado na estrutura reorganizada e otimizada do sistema Carntrack**

## 🚀 COMO USAR ESTE TEMPLATE

### 1. Preparação
1. Copie esta pasta para um novo local
2. Renomeie para o nome da sua empresa virtual
3. Atualize o `README_EMPRESA.md` com informações da nova empresa

### 2. Criação de Personas  
1. Vá para `04_PERSONAS_SCRIPTS_1_2_3/`
2. Crie pastas para suas categorias (assistentes, executivos, etc.)
3. Para cada persona:
   - Use o template em `05_TEMPLATES_SISTEMA/biografia_templates/`
   - Crie pasta com nome da persona
   - Adicione biografia usando o template

### 3. Execução dos Scripts
1. **Script 1**: Gera competências baseadas na biografia
2. **Script 2**: Cria especificações técnicas baseadas nas competências  
3. **Script 3**: Gera base de conhecimento RAG
4. **Script 4**: Analisa fluxos e cria TaskTodo algorítmico
5. **Script 5**: Gera workflows N8N baseados no TaskTodo

### 4. Estrutura Final
Após executar todos os scripts, cada persona terá:
```
📂 Persona_Nome/
├── 📄 Persona_Nome_bio.md
├── 📂 script1_competencias/
├── 📂 script2_tech_specs/
├── 📂 script3_rag/
├── 📂 script4_tasktodo/
└── 📂 script5_workflows_n8n/
```

## 📂 ESTRUTURA DO TEMPLATE

### **01_DOCUMENTACAO_GERAL/**
- Documentação geral do sistema
- Manuais de uso
- Especificações técnicas

### **02_SCRIPTS_AUTOMACAO/**
- Scripts de automação
- Ferramentas auxiliares
- Utilitários

### **03_WORKFLOWS_LEGADO/**
- Workflows de referência
- Versões anteriores
- Backup de configurações

### **04_PERSONAS_SCRIPTS_1_2_3/**
🎯 **PASTA PRINCIPAL DAS PERSONAS**
- Estrutura organizada por categoria e persona
- Cada pasta de persona contém outputs dos 5 scripts
- Exemplo de estrutura fornecido

### **05_TEMPLATES_SISTEMA/**
🎨 **TEMPLATES REUTILIZÁVEIS**
- Templates para biografias
- Templates para cada script
- Exemplos e guias

### **06-09: Pastas de Sistema**
- RAG Knowledge Base
- Email Templates  
- Database Schemas
- Monitoring e Logs

## 🎯 VANTAGENS DESTA ESTRUTURA

✅ **Organizada**: Pastas numeradas seguem sequência lógica
✅ **Completa**: Tudo por persona em uma pasta  
✅ **Escalável**: Fácil adicionar novas personas e categorias
✅ **Reutilizável**: Templates para acelerar criação
✅ **Documentada**: Guias claros para cada etapa

## 📋 CHECKLIST PARA NOVA EMPRESA

- [ ] Copiar template para nova localização
- [ ] Renomear pasta com nome da empresa
- [ ] Atualizar README_EMPRESA.md
- [ ] Definir categorias de personas necessárias
- [ ] Criar biografias usando templates
- [ ] Executar scripts 1-5 sequencialmente
- [ ] Validar outputs de cada script
- [ ] Documentar particularidades da empresa

## 🔧 SCRIPTS INCLUÍDOS

Os scripts do Virtual Company Generator estão configurados para:
- Detectar automaticamente a estrutura
- Salvar outputs nas pastas corretas
- Validar consistência entre etapas
- Gerar documentação completa

## 📞 SUPORTE

Para dúvidas sobre uso deste template:
1. Consulte a documentação em cada pasta
2. Verifique os exemplos fornecidos
3. Siga a sequência de scripts 1-5

---
*Template gerado pelo Virtual Company Generator v2.0.0*
*Data de criação: Novembro 2025*
"""

    readme_path = template_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(main_readme)
    
    # Template de README para nova empresa
    empresa_readme = """# 🏢 [NOME DA EMPRESA] - EMPRESA VIRTUAL IA

> *Gerado pelo Virtual Company Generator Master v2.0.0*

## 🎉 **ESTRUTURA REORGANIZADA**

**IMPORTANTE**: Esta empresa usa a estrutura reorganizada e otimizada:

✅ **Pastas numeradas** na sequência dos scripts (01, 02, 03...)
✅ **Tudo por persona** em uma única pasta organizada  
✅ **Scripts identificados** (script1_competencias, script2_tech_specs, etc.)
✅ **Templates organizados** por categoria

---

## 📋 **VISÃO GERAL**

**Empresa:** [Nome da Empresa]
**Indústria:** [Indústria/Setor]
**Domínio:** [dominio.com]
**Criada em:** [Data]

### 🎯 **Descrição:**
[Descrição detalhada da empresa virtual, seus objetivos e propósito]

### 👥 **Público-Alvo:**
[Descrição do público-alvo principal]

### 🏆 **Objetivos de Negócio:**
[Objetivos principais da empresa virtual]

## 📊 **ESTATÍSTICAS ATUAIS**

- **Total de Personas:** [número]
- **Assistentes:** [número]
- **Executivos:** [número] 
- **Especialistas:** [número]
- **Suporte:** [número]

## 🚀 **ESTRUTURA DE PERSONAS**

### 👥 **Assistentes** (Nível Operacional)
- [Lista das personas assistentes]

### 🎯 **Executivos** (Nível Estratégico)  
- [Lista das personas executivas]

### 🔬 **Especialistas** (Nível Técnico)
- [Lista das personas especialistas]

### 🛠️ **Suporte** (Nível de Apoio)
- [Lista das personas de suporte]

## 📈 **STATUS DO PROJETO**

### ✅ Concluído
- [x] Estrutura base criada
- [x] Templates configurados

### 🔄 Em Andamento  
- [ ] [Tarefa em andamento 1]
- [ ] [Tarefa em andamento 2]

### 📋 Planejado
- [ ] [Tarefa planejada 1]
- [ ] [Tarefa planejada 2]

## 🔧 **SCRIPTS UTILIZADOS**

### Script 1 - Competências ✅
**Status:** [Concluído/Em Andamento/Pendente]
**Personas processadas:** [número]/[total]

### Script 2 - Tech Specs ✅  
**Status:** [Concluído/Em Andamento/Pendente]
**Personas processadas:** [número]/[total]

### Script 3 - RAG Knowledge Base ✅
**Status:** [Concluído/Em Andamento/Pendente]  
**Personas processadas:** [número]/[total]

### Script 4 - TaskTodo Analysis ✅
**Status:** [Concluído/Em Andamento/Pendente]
**Personas processadas:** [número]/[total]

### Script 5 - Workflows N8N ✅
**Status:** [Concluído/Em Andamento/Pendente]
**Personas processadas:** [número]/[total]

## 📁 **ESTRUTURA DE ARQUIVOS**

```
📂 [nome_empresa]/
├── 📂 01_DOCUMENTACAO_GERAL/
├── 📂 02_SCRIPTS_AUTOMACAO/
├── 📂 03_WORKFLOWS_LEGADO/
├── 📂 04_PERSONAS_SCRIPTS_1_2_3/
│   ├── 📂 assistentes/
│   ├── 📂 executivos/
│   ├── 📂 especialistas/
│   └── 📂 suporte/
├── 📂 05_TEMPLATES_SISTEMA/
├── 📂 06_RAG_KNOWLEDGE_BASE/
├── 📂 07_EMAIL_TEMPLATES/
├── 📂 08_DATABASE_SCHEMAS/
└── 📂 09_MONITORING_LOGS/
```

## 📞 **CONTATO E SUPORTE**

**Criado por:** [Seu nome]
**Data de criação:** [Data]
**Última atualização:** [Data]

---
*Sistema gerado pelo Virtual Company Generator v2.0.0*
"""

    empresa_readme_path = template_dir / "README_EMPRESA.md"
    with open(empresa_readme_path, 'w', encoding='utf-8') as f:
        f.write(empresa_readme)
    
    print("   ✅ Documentação criada")

def create_generation_scripts(template_dir):
    """Cria scripts auxiliares para geração"""
    
    print("\n🔧 Criando scripts auxiliares...")
    
    # Script para inicializar nova empresa
    init_script = """#!/usr/bin/env python3
\"\"\"
INICIALIZADOR DE NOVA EMPRESA VIRTUAL
Script para configurar rapidamente uma nova empresa virtual
\"\"\"

import os
from pathlib import Path
from datetime import datetime

def initialize_new_company():
    \"\"\"Inicializa configuração de nova empresa\"\"\"
    
    print("🚀 INICIALIZANDO NOVA EMPRESA VIRTUAL")
    print("=" * 50)
    
    # Coletar informações básicas
    company_info = {}
    company_info['nome'] = input("📋 Nome da empresa: ")
    company_info['industria'] = input("🏭 Indústria/Setor: ") 
    company_info['dominio'] = input("🌐 Domínio (ex: empresa.com): ")
    company_info['descricao'] = input("📝 Descrição breve: ")
    company_info['publico_alvo'] = input("👥 Público-alvo: ")
    
    # Atualizar README_EMPRESA.md
    update_company_readme(company_info)
    
    # Criar categorias de personas
    setup_persona_categories()
    
    print("\\n✅ EMPRESA INICIALIZADA COM SUCESSO!")
    print("🔄 Próximos passos:")
    print("1. Criar biografias das personas usando os templates")
    print("2. Executar scripts 1-5 sequencialmente")
    print("3. Validar outputs de cada script")

def update_company_readme(info):
    \"\"\"Atualiza README com informações da empresa\"\"\"
    
    readme_path = Path("README_EMPRESA.md")
    
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir placeholders
        content = content.replace('[NOME DA EMPRESA]', info['nome'])
        content = content.replace('[Nome da Empresa]', info['nome'])
        content = content.replace('[Indústria/Setor]', info['industria'])
        content = content.replace('[dominio.com]', info['dominio'])
        content = content.replace('[Data]', datetime.now().strftime('%Y-%m-%d'))
        content = content.replace('[Descrição detalhada da empresa virtual, seus objetivos e propósito]', info['descricao'])
        content = content.replace('[Descrição do público-alvo principal]', info['publico_alvo'])
        
        # Salvar atualizado
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 README_EMPRESA.md atualizado para {info['nome']}")

def setup_persona_categories():
    \"\"\"Configura categorias de personas\"\"\"
    
    categories = ['assistentes', 'executivos', 'especialistas', 'suporte']
    personas_dir = Path("04_PERSONAS_SCRIPTS_1_2_3")
    
    for category in categories:
        category_dir = personas_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Criar README na categoria
        readme_content = f\"\"\"# {category.upper()}

## Descrição
Pasta para personas da categoria {category}.

## Como adicionar nova persona
1. Criar pasta com nome da persona
2. Copiar template de biografia de `05_TEMPLATES_SISTEMA/biografia_templates/`
3. Preencher biografia com informações específicas
4. Executar scripts 1-5 sequencialmente

## Estrutura esperada para cada persona
```
📂 Nome_da_Persona/
├── 📄 Nome_da_Persona_bio.md
├── 📂 script1_competencias/
├── 📂 script2_tech_specs/
├── 📂 script3_rag/
├── 📂 script4_tasktodo/
└── 📂 script5_workflows_n8n/
```

---
*Gerado automaticamente pelo inicializador*
\"\"\"
        
        readme_path = category_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    print("📁 Categorias de personas configuradas")

if __name__ == "__main__":
    initialize_new_company()
"""

    script_path = template_dir / "initialize_company.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(init_script)
    
    # Script de validação
    validation_script = """#!/usr/bin/env python3
\"\"\"
VALIDADOR DE ESTRUTURA
Verifica se a estrutura da empresa virtual está correta
\"\"\"

import os
from pathlib import Path

def validate_structure():
    \"\"\"Valida estrutura da empresa virtual\"\"\"
    
    print("🔍 VALIDANDO ESTRUTURA DA EMPRESA VIRTUAL")
    print("=" * 50)
    
    issues = []
    warnings = []
    
    # Verificar pastas principais
    required_folders = [
        "01_DOCUMENTACAO_GERAL",
        "02_SCRIPTS_AUTOMACAO", 
        "03_WORKFLOWS_LEGADO",
        "04_PERSONAS_SCRIPTS_1_2_3",
        "05_TEMPLATES_SISTEMA",
        "06_RAG_KNOWLEDGE_BASE",
        "07_EMAIL_TEMPLATES", 
        "08_DATABASE_SCHEMAS",
        "09_MONITORING_LOGS"
    ]
    
    for folder in required_folders:
        if not Path(folder).exists():
            issues.append(f"Pasta obrigatória ausente: {folder}")
        else:
            print(f"✅ {folder}")
    
    # Verificar personas
    personas_dir = Path("04_PERSONAS_SCRIPTS_1_2_3")
    if personas_dir.exists():
        categories = [d for d in personas_dir.iterdir() if d.is_dir()]
        
        if not categories:
            warnings.append("Nenhuma categoria de persona encontrada")
        else:
            print(f"\\n👥 Categorias de personas encontradas: {len(categories)}")
            
            total_personas = 0
            for category in categories:
                personas = [d for d in category.iterdir() if d.is_dir() and not d.name.endswith('_exemplo')]
                total_personas += len(personas)
                print(f"   📂 {category.name}: {len(personas)} personas")
                
                # Verificar estrutura de cada persona
                for persona in personas:
                    validate_persona_structure(persona, warnings)
            
            print(f"\\n📊 Total de personas: {total_personas}")
    
    # Verificar arquivos principais
    required_files = ["README.md", "README_EMPRESA.md"]
    for file in required_files:
        if not Path(file).exists():
            issues.append(f"Arquivo obrigatório ausente: {file}")
        else:
            print(f"✅ {file}")
    
    # Relatório final
    print("\\n" + "=" * 50)
    print("📋 RELATÓRIO DE VALIDAÇÃO")
    print("=" * 50)
    
    if not issues and not warnings:
        print("🎉 ESTRUTURA PERFEITA! Tudo está correto.")
    else:
        if issues:
            print("❌ PROBLEMAS ENCONTRADOS:")
            for issue in issues:
                print(f"   ❌ {issue}")
        
        if warnings:
            print("\\n⚠️ AVISOS:")
            for warning in warnings:
                print(f"   ⚠️ {warning}")
    
    return len(issues) == 0

def validate_persona_structure(persona_path, warnings):
    \"\"\"Valida estrutura de uma persona específica\"\"\"
    
    expected_folders = [
        "script1_competencias",
        "script2_tech_specs", 
        "script3_rag",
        "script4_tasktodo",
        "script5_workflows_n8n"
    ]
    
    missing_folders = []
    for folder in expected_folders:
        if not (persona_path / folder).exists():
            missing_folders.append(folder)
    
    if missing_folders:
        warnings.append(f"Persona {persona_path.name}: pastas ausentes: {', '.join(missing_folders)}")
    
    # Verificar biografia
    bio_files = list(persona_path.glob("*_bio.md"))
    if not bio_files:
        warnings.append(f"Persona {persona_path.name}: biografia não encontrada")

if __name__ == "__main__":
    validate_structure()
"""

    validation_path = template_dir / "validate_structure.py"
    with open(validation_path, 'w', encoding='utf-8') as f:
        f.write(validation_script)
    
    print("   ✅ Scripts auxiliares criados")

def print_template_structure():
    """Imprime estrutura do template criado"""
    
    print("\n" + "=" * 60)
    print("📂 ESTRUTURA DO TEMPLATE CRIADO")
    print("=" * 60)
    
    structure = """
📂 VIRTUAL_COMPANY_TEMPLATE_CLEAN/
├── 📄 README.md
├── 📄 README_EMPRESA.md (template)
├── 📄 initialize_company.py
├── 📄 validate_structure.py
├── 📂 01_DOCUMENTACAO_GERAL/
├── 📂 02_SCRIPTS_AUTOMACAO/
├── 📂 03_WORKFLOWS_LEGADO/
├── 📂 04_PERSONAS_SCRIPTS_1_2_3/
│   ├── 📂 assistentes_exemplo/
│   │   └── 📂 Persona_Exemplo/
│   │       ├── 📄 Persona_Exemplo_bio.md
│   │       ├── 📂 script1_competencias/
│   │       ├── 📂 script2_tech_specs/
│   │       ├── 📂 script3_rag/
│   │       ├── 📂 script4_tasktodo/
│   │       └── 📂 script5_workflows_n8n/
│   ├── 📂 executivos_exemplo/
│   ├── 📂 especialistas_exemplo/
│   └── 📂 suporte_exemplo/
├── 📂 05_TEMPLATES_SISTEMA/
│   ├── 📂 biografia_templates/
│   │   └── 📄 biografia_template.md
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
    
    print("\n🎯 COMO USAR O TEMPLATE:")
    print("1. 📁 Copie a pasta para nova localização")
    print("2. 🏢 Execute `python initialize_company.py`")  
    print("3. 👥 Crie biografias usando os templates")
    print("4. ⚡ Execute scripts 1-5 sequencialmente")
    print("5. ✅ Use `python validate_structure.py` para verificar")

if __name__ == "__main__":
    create_clean_template()