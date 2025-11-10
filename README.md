# 🚀 VCM - Virtual Company Manager

Sistema completo para geração e gestão de empresas virtuais com IA.

## 🎯 Início Rápido

### Opção 1: Script Automático (Recomendado)

**Windows:**
```bash
# Duplo clique no arquivo ou execute no terminal:
start-vcm.bat
```

**PowerShell:**
```powershell
.\start-vcm.ps1
```

**Linux/macOS:**
```bash
chmod +x start-vcm.sh
./start-vcm.sh
```

### Opção 2: NPM (Multi-plataforma)

```bash
# Instalar dependências
npm install

# Iniciar sistema completo
npm start
```

### Opção 3: Manual

```bash
# Terminal 1 - API Backend
python api_bridge_real.py

# Terminal 2 - Frontend Dashboard
cd vcm-dashboard-real
npm run dev
```

## 🌐 Acesso ao Sistema

- **Dashboard:** http://localhost:3001
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## ⚙️ Configuração

1. **Copie o arquivo de configuração:**
   ```bash
   cp .env.example .env
   ```

2. **Configure suas chaves no arquivo `.env`:**
   - VCM_SUPABASE_URL
   - VCM_SUPABASE_SERVICE_ROLE_KEY
   - OPENAI_API_KEY
   - Outras configurações necessárias

## 📋 Pré-requisitos

- **Python 3.8+**
- **Node.js 18+**
- **NPM ou Yarn**

## 🔧 Scripts Disponíveis

| Comando | Descrição |
|---------|-----------|
| `npm start` | Inicia o sistema completo |
| `npm run start:api` | Inicia apenas a API |
| `npm run start:frontend` | Inicia apenas o frontend |
| `npm run setup` | Instala todas as dependências |
| `npm run test:connectivity` | Testa conectividade da API |
| `npm run test:supabase` | Testa conexão com Supabase |
| `npm run build` | Build do frontend para produção |

## 🏗️ Arquitetura

```
vcm_vite_react/
├── 🚀 start-vcm.bat/.ps1/.sh    # Scripts de inicialização
├── 📡 api_bridge_real.py         # API Backend FastAPI
├── 🌐 vcm-dashboard-real/        # Frontend Next.js
├── 🤖 AUTOMACAO/                 # Scripts Python de IA
│   ├── 01_SETUP_E_CRIACAO/       # Geração de empresas
│   ├── 02_PROCESSAMENTO_PERSONAS/ # Processamento de personas
│   └── 03_ORGANIZACAO_E_MANUTENCAO/ # Manutenção
├── 📚 Docs/                      # Documentação
└── ⚙️ .env                       # Configurações
```

## 🎯 Funcionalidades

- ✅ **Geração de Empresas Virtuais** - Criação automática com IA
- ✅ **Gestão de Personas** - 20 personas padronizadas
- ✅ **Processamento em Cascata** - 5 scripts sequenciais
- ✅ **Interface Web** - Dashboard Next.js completo
- ✅ **API REST** - Backend FastAPI robusto
- ✅ **Integração Supabase** - Banco de dados em tempo real
- ✅ **Workflows N8N** - Automação de processos

## 🛠️ Desenvolvimento

### Estrutura de Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
npm run setup

# Modo desenvolvimento com hot reload
npm start

# Build para produção
npm run build
```

### Logs e Debug

- **API Logs:** Aparecem no terminal da API
- **Frontend Logs:** Console do navegador
- **Sistema Logs:** Arquivos .log gerados automaticamente

## 🚨 Solução de Problemas

### Porta já em uso
```bash
# Verificar processos nas portas
netstat -ano | findstr :8000
netstat -ano | findstr :3001

# Matar processo (substitua PID)
taskkill /PID <PID> /F
```

### Dependências
```bash
# Reinstalar dependências Python
pip install -r requirements.txt

# Reinstalar dependências Node.js
npm run setup
```

### Conectividade Supabase
```bash
# Testar conexão
npm run test:supabase
```

## 📞 Suporte

- **Issues:** GitHub Issues
- **Documentação:** `/Docs` folder
- **API Docs:** http://localhost:8000/docs

## 📄 Licença

MIT License - Veja arquivo LICENSE para detalhes.

---

**Virtual Company Manager v1.0.0**  
*Desenvolvido por Sergio Castro*