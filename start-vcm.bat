@echo off
REM =====================================================
REM 🚀 VCM - VIRTUAL COMPANY MANAGER - INICIALIZADOR
REM =====================================================
REM Script para iniciar todos os serviços do VCM
REM Versão: 1.0.0
REM Data: November 2025
REM =====================================================

title VCM - Virtual Company Manager

echo.
echo ========================================
echo 🚀 VCM - VIRTUAL COMPANY MANAGER
echo ========================================
echo.
echo Inicializando todos os serviços...
echo.

REM Verificar se estamos no diretório correto
if not exist "vcm-dashboard-real" (
    echo ❌ Erro: Execute este script na pasta raiz do projeto!
    echo 📁 Esperado: vcm-dashboard-real deve existir aqui
    pause
    exit /b 1
)

REM Verificar se o .env existe
if not exist ".env" (
    echo ❌ Erro: Arquivo .env não encontrado!
    echo 💡 Copie o .env.example para .env e configure suas chaves
    pause
    exit /b 1
)

echo ✅ Verificações iniciais OK
echo.

REM 1. Instalar dependências Python se necessário
echo 📦 Verificando dependências Python...
pip install fastapi uvicorn python-multipart supabase python-dotenv requests --quiet
echo ✅ Dependências Python OK
echo.

REM 2. Instalar dependências Node.js se necessário
echo 📦 Verificando dependências Node.js...
cd vcm-dashboard-real
if not exist "node_modules" (
    echo 📥 Instalando dependências do frontend...
    npm install
)
cd ..
echo ✅ Dependências Node.js OK
echo.

REM 3. Iniciar API Backend em nova janela
echo 🚀 Iniciando API Backend (porta 8000)...
start "VCM API Backend" cmd /k "python api_bridge_real.py"
timeout /t 3 /nobreak >nul
echo ✅ API Backend iniciada

REM 4. Iniciar Frontend em nova janela
echo 🌐 Iniciando Dashboard Frontend (porta 3001)...
start "VCM Dashboard" cmd /k "cd vcm-dashboard-real && npm run dev"
timeout /t 3 /nobreak >nul
echo ✅ Dashboard Frontend iniciado

echo.
echo ========================================
echo 🎉 VCM INICIADO COM SUCESSO!
echo ========================================
echo.
echo 🌐 Dashboard: http://localhost:3001
echo 🚀 API Docs:  http://localhost:8000/docs
echo 🏥 Health:    http://localhost:8000/health
echo.
echo 💡 Aguarde alguns segundos para os serviços
echo    carregarem completamente...
echo.
echo ⚠️  Para parar: Feche as janelas dos serviços
echo    ou pressione Ctrl+C em cada uma
echo.

REM Aguardar 10 segundos e abrir dashboard
echo 🕐 Aguardando serviços carregarem (10s)...
timeout /t 10 /nobreak >nul

echo 🌐 Abrindo dashboard no navegador...
start http://localhost:3001

echo.
echo ✅ Sistema completamente inicializado!
echo 📱 Pressione qualquer tecla para fechar este terminal
pause >nul