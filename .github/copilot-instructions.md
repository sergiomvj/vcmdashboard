# Virtual Company Manager (VCM) - AI Coding Agent Instructions

## 🎯 Project Overview
This is a **Virtual Company Manager** system that automatically generates complete virtual companies with AI-powered personas, workflows, and Supabase integration. The project consists of a Python automation backend for company generation and a planned React dashboard frontend.

## 🏗️ Architecture & Key Concepts

### Dual Database Strategy
- **VCM Central**: Master Supabase database (`fzyokrvdyeczhfqlwxzb.supabase.co`) for managing multiple virtual companies
- **Individual RAG Databases**: Each virtual company gets its own Supabase database (e.g., LifewayUSA: `neaoblaycbdunfxgunjo.supabase.co`)
- **Synchronization**: Bidirectional sync between local data → RAG DB → VCM Central

### Five-Script Cascade Processing
The system follows a **strict sequential workflow** (Scripts 1-5):
1. **Biography Generation** → Personas with complete backgrounds
2. **Competencies Analysis** → Technical & behavioral skills extraction  
3. **Tech Specifications** → System requirements and tools
4. **RAG Database Population** → Structured knowledge base creation
5. **N8N Workflow Generation** → Automated business process workflows

### Persona System
- **20 standardized personas** across 3 categories: `executivos`, `especialistas`, `assistentes`
- **CEO is special**: Always generated first with `is_ceo: true` flag
- **Configuration-driven**: All persona data stored in `personas_config.json`
- **Multi-language support**: Personas can speak multiple languages for international companies

## 📁 Critical Directory Structure

```
AUTOMACAO/
├── 01_SETUP_E_CRIACAO/           # Company generation & setup
├── 02_PROCESSAMENTO_PERSONAS/    # 5-script cascade processing
├── 03_ORGANIZACAO_E_MANUTENCAO/  # System maintenance & testing
└── 04_EXECUTAVEIS_BAT/           # Batch execution scripts (empty)

Docs/                             # Architecture documentation
.env                              # Multi-database configuration
```

## 🔧 Development Workflows

### Running the Cascade (Critical Sequence)
```bash
# NEVER run scripts out of order - dependencies are strict
cd AUTOMACAO/02_PROCESSAMENTO_PERSONAS/
python 01_generate_competencias.py
python 02_generate_tech_specs.py  
python 03_generate_rag.py
python 04_generate_fluxos_analise.py
python 05_generate_workflows_n8n.py
```

### Environment Configuration
- **Always check `.env`** before database operations
- **VCM_SUPABASE_*** = Central management database
- **LIFEWAY_SUPABASE_*** = Example virtual company database
- **Multiple API keys**: OpenAI, Anthropic, Google AI for different generation tasks

### Testing & Validation
- Use `AUTOMACAO/03_ORGANIZACAO_E_MANUTENCAO/04_test_scripts_4_5.py` for validation
- Output validation is in `test_biografias_output/` directories
- **Always verify JSON structure** in `personas_config.json` after generation

## ⚡ Project-Specific Patterns

### Python Class Architecture
- **Generator classes**: Self-contained with `__init__` setting up paths and logging
- **Path detection**: Uses `Path(__file__).parent.parent` for relative navigation
- **Logging strategy**: File-based logging to avoid Windows encoding issues
- **Error handling**: Comprehensive try/catch with detailed logging

### Data Flow Patterns
```python
# Standard pattern for all generators
self.base_path = Path(__file__).parent.parent
self.output_path = self.base_path / "output_directory"
self.output_path.mkdir(exist_ok=True)
```

### Supabase Integration
- **Service role keys** for administrative operations
- **Anon keys** for read operations  
- **Connection pooling** handled at application level
- **Sync operations** are batch-based with retry logic

## 🚨 Common Pitfalls

### Script Dependencies
- **Never skip cascade steps** - each script depends on previous outputs
- **Check personas_config.json exists** before running processing scripts
- **Validate output directories** before proceeding to next script

### Database Operations
- **Always use absolute paths** for file operations
- **Check environment variables** before database connections
- **Handle encoding properly** - use `encoding='utf-8'` for file operations
- **Batch operations** for large persona datasets

### Windows-Specific Issues
- **PowerShell paths**: Use forward slashes in Python, backslashes in Windows commands
- **File encoding**: Explicitly specify UTF-8 for all file operations
- **Path separators**: Use `Path()` objects, not string concatenation

## 📋 Key Integration Points

### Frontend (Planned React Dashboard)
- **Vite + TypeScript + React + shadcn-ui + Tailwind CSS**
- **Lovable.dev integration** for rapid prototyping
- **Real-time sync** with VCM Central database
- **Multi-company management** interface

### External Systems
- **N8N workflows**: Generated JSON files for business automation
- **Multiple AI providers**: OpenAI for generation, Anthropic for analysis
- **Supabase**: Both as data store and real-time sync platform

## 🎯 When Working on This Project

1. **Always start by checking** `.env` configuration and database connectivity
2. **Respect the cascade order** - never run processing scripts out of sequence  
3. **Validate JSON outputs** after each script execution
4. **Use logging extensively** - all operations should be logged to files
5. **Test with LifewayUSA data** - it's the reference implementation
6. **Consider multi-language support** in all persona-related features

This system is designed for **scalability and automation** - every virtual company should be generatable with minimal manual intervention.