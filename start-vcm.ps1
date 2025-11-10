# =====================================================
# 🚀 VCM - VIRTUAL COMPANY MANAGER - INICIALIZADOR
# =====================================================
# Script PowerShell para iniciar todos os serviços do VCM
# Versão: 1.0.0
# Data: November 2025
# =====================================================

# Configurar título e cores
$Host.UI.RawUI.WindowTitle = "VCM - Virtual Company Manager"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 VCM - VIRTUAL COMPANY MANAGER" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Inicializando todos os serviços..." -ForegroundColor White
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path "vcm-dashboard-real")) {
    Write-Host "❌ Erro: Execute este script na pasta raiz do projeto!" -ForegroundColor Red
    Write-Host "📁 Esperado: vcm-dashboard-real deve existir aqui" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se o .env existe
if (-not (Test-Path ".env")) {
    Write-Host "❌ Erro: Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "💡 Copie o .env.example para .env e configure suas chaves" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "✅ Verificações iniciais OK" -ForegroundColor Green
Write-Host ""

# 1. Instalar dependências Python
Write-Host "📦 Verificando dependências Python..." -ForegroundColor Cyan
try {
    pip install fastapi uvicorn python-multipart supabase python-dotenv requests --quiet
    Write-Host "✅ Dependências Python OK" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Aviso: Problema com dependências Python: $($_.Exception.Message)" -ForegroundColor Yellow
}
Write-Host ""

# 2. Instalar dependências Node.js
Write-Host "📦 Verificando dependências Node.js..." -ForegroundColor Cyan
Set-Location "vcm-dashboard-real"
if (-not (Test-Path "node_modules")) {
    Write-Host "📥 Instalando dependências do frontend..." -ForegroundColor Yellow
    npm install
}
Set-Location ".."
Write-Host "✅ Dependências Node.js OK" -ForegroundColor Green
Write-Host ""

# 3. Função para verificar se uma porta está em uso
function Test-Port {
    param([int]$Port)
    $connection = New-Object System.Net.Sockets.TcpClient
    try {
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $true
    } catch {
        return $false
    }
}

# 4. Verificar se as portas estão livres
if (Test-Port 8000) {
    Write-Host "⚠️ Porta 8000 já está em uso!" -ForegroundColor Yellow
} else {
    Write-Host "✅ Porta 8000 disponível" -ForegroundColor Green
}

if (Test-Port 3001) {
    Write-Host "⚠️ Porta 3001 já está em uso!" -ForegroundColor Yellow
} else {
    Write-Host "✅ Porta 3001 disponível" -ForegroundColor Green
}
Write-Host ""

# 5. Iniciar API Backend
Write-Host "🚀 Iniciando API Backend (porta 8000)..." -ForegroundColor Cyan
$apiProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python api_bridge_real.py" -PassThru
Write-Host "✅ API Backend iniciada (PID: $($apiProcess.Id))" -ForegroundColor Green

# Aguardar um pouco
Start-Sleep 3

# 6. Iniciar Frontend
Write-Host "🌐 Iniciando Dashboard Frontend (porta 3001)..." -ForegroundColor Cyan
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\vcm-dashboard-real'; npm run dev" -PassThru
Write-Host "✅ Dashboard Frontend iniciado (PID: $($frontendProcess.Id))" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 VCM INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Dashboard: http://localhost:3001" -ForegroundColor White
Write-Host "🚀 API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "🏥 Health:    http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "💡 Aguarde alguns segundos para os serviços" -ForegroundColor Yellow
Write-Host "   carregarem completamente..." -ForegroundColor Yellow
Write-Host ""

# 7. Aguardar e verificar se os serviços estão rodando
Write-Host "🕐 Verificando serviços..." -ForegroundColor Cyan
for ($i = 1; $i -le 10; $i++) {
    Write-Host "." -NoNewline -ForegroundColor Yellow
    Start-Sleep 1
}
Write-Host ""

# Verificar se os serviços estão respondendo
try {
    $apiResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ API respondendo: $($apiResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ API ainda carregando..." -ForegroundColor Yellow
}

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3001" -TimeoutSec 5 -UseBasicParsing
    Write-Host "✅ Dashboard respondendo: $($frontendResponse.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Dashboard ainda carregando..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Abrindo dashboard no navegador..." -ForegroundColor Cyan
Start-Process "http://localhost:3001"

Write-Host ""
Write-Host "✅ Sistema completamente inicializado!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 COMANDOS ÚTEIS:" -ForegroundColor Cyan
Write-Host "   - Para parar API: Feche a janela 'python api_bridge_real.py'" -ForegroundColor White
Write-Host "   - Para parar Dashboard: Feche a janela 'npm run dev'" -ForegroundColor White
Write-Host "   - Para reiniciar: Execute este script novamente" -ForegroundColor White
Write-Host ""
Write-Host "📱 Pressione Enter para fechar este terminal..." -ForegroundColor Yellow
Read-Host