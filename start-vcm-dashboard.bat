@echo off
echo 🚀 Iniciando VCM Dashboard Completo...
echo =======================================

echo 📝 Verificando dependências...

REM Verificar Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado. Instale Node.js primeiro.
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado. Instale Python primeiro.
    pause
    exit /b 1
)

echo ✅ Dependências OK

REM Obter diretório do script
set "SCRIPT_DIR=%~dp0"
set "FRONTEND_DIR=%SCRIPT_DIR%vcm-dashboard-real"

echo 🔗 Iniciando servidor backend (FastAPI)...
start "VCM Backend" cmd /c "cd /d "%SCRIPT_DIR%" && python api_bridge_real.py"

REM Aguardar backend inicializar
timeout /t 3 /nobreak >nul

echo 🌐 Iniciando servidor frontend (Next.js)...
start "VCM Frontend" cmd /c "cd /d "%FRONTEND_DIR%" && npm run dev"

REM Aguardar frontend inicializar
timeout /t 5 /nobreak >nul

echo.
echo =======================================
echo 🎉 VCM Dashboard iniciado com sucesso!
echo 🌐 Frontend: http://localhost:3001
echo 🔗 Backend API: http://localhost:8000
echo 📚 Documentação API: http://localhost:8000/docs
echo.
echo 💡 Para parar os serviços, feche as janelas abertas
echo    ou use Ctrl+C em cada terminal
echo =======================================

REM Aguardar frontend estar pronto e abrir navegador
timeout /t 10 /nobreak >nul
start http://localhost:3001

echo 🌐 Abrindo dashboard no navegador...
pause