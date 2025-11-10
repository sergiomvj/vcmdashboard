# 🚀 Inicializador VCM Dashboard para Windows
# ==========================================

Write-Host "🚀 Iniciando VCM Dashboard completo..." -ForegroundColor Green
Write-Host "=" * 50

# Verificar dependências
Write-Host "🔍 Verificando dependências..." -ForegroundColor Yellow

# Verificar Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js não encontrado. Instale Node.js primeiro." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar Python
try {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado." -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Obter diretório do script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $scriptDir "vcm-dashboard-real"

Write-Host ""
Write-Host "🔗 Iniciando servidor backend (FastAPI)..." -ForegroundColor Blue

# Iniciar backend em nova janela PowerShell
$backendScript = @"
cd '$scriptDir'
python api_bridge_real.py
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "🌐 Iniciando servidor frontend (Next.js)..." -ForegroundColor Blue

# Verificar se diretório frontend existe
if (-not (Test-Path $frontendDir)) {
    Write-Host "❌ Diretório frontend não encontrado: $frontendDir" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Iniciar frontend em nova janela PowerShell
$frontendScript = @"
cd '$frontendDir'
npm run dev
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript -WindowStyle Normal

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "=" * 50
Write-Host "🎉 VCM Dashboard iniciado com sucesso!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3001" -ForegroundColor Cyan
Write-Host "🔗 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Documentação API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Para parar os serviços, feche as janelas PowerShell abertas" -ForegroundColor Yellow
Write-Host "   ou use Ctrl+C em cada terminal" -ForegroundColor Yellow
Write-Host "=" * 50

# Aguardar frontend estar pronto e abrir navegador
Write-Host "⏳ Aguardando frontend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "🌐 Abrindo dashboard no navegador..." -ForegroundColor Green
Start-Process "http://localhost:3001"

Write-Host ""
Write-Host "✅ Sistema inicializado com sucesso!" -ForegroundColor Green
Read-Host "Pressione Enter para fechar esta janela"