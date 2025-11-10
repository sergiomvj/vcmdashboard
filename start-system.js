// =====================================================
// 🚀 VCM - VIRTUAL COMPANY MANAGER - SYSTEM STARTER
// =====================================================
// Script Node.js para iniciar o sistema completo
// Versão: 1.0.0
// Data: November 2025
// =====================================================

const { spawn, exec } = require('child_process');
const path = require('path');
const fs = require('fs');

// Cores para console
const colors = {
    reset: '\x1b[0m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    white: '\x1b[37m'
};

function log(message, color = 'white') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function checkFile(filePath, name) {
    if (!fs.existsSync(filePath)) {
        log(`❌ ${name} não encontrado: ${filePath}`, 'red');
        return false;
    }
    log(`✅ ${name} encontrado`, 'green');
    return true;
}

function checkPort(port, callback) {
    const net = require('net');
    const server = net.createServer();
    
    server.listen(port, () => {
        server.once('close', () => {
            callback(false); // Port is free
        });
        server.close();
    });
    
    server.on('error', () => {
        callback(true); // Port is in use
    });
}

async function startSystem() {
    log('', 'white');
    log('========================================', 'cyan');
    log('🚀 VCM - VIRTUAL COMPANY MANAGER', 'yellow');
    log('========================================', 'cyan');
    log('', 'white');
    log('Inicializando sistema completo...', 'white');
    log('', 'white');

    // 1. Verificações iniciais
    log('🔍 Verificando arquivos necessários...', 'cyan');
    const checks = [
        checkFile('api_bridge_real.py', 'API Backend'),
        checkFile('vcm-dashboard-real', 'Dashboard Frontend'),
        checkFile('.env', 'Arquivo de configuração')
    ];

    if (!checks.every(check => check)) {
        log('❌ Verificações falharam! Certifique-se de estar na pasta raiz do projeto.', 'red');
        process.exit(1);
    }

    // 2. Verificar portas
    log('', 'white');
    log('🔍 Verificando portas...', 'cyan');
    
    return new Promise((resolve, reject) => {
        checkPort(8000, (inUse) => {
            if (inUse) {
                log('⚠️ Porta 8000 já está em uso!', 'yellow');
            } else {
                log('✅ Porta 8000 disponível', 'green');
            }

            checkPort(3001, (inUse) => {
                if (inUse) {
                    log('⚠️ Porta 3001 já está em uso!', 'yellow');
                } else {
                    log('✅ Porta 3001 disponível', 'green');
                }

                log('', 'white');
                startServices();
                resolve();
            });
        });
    });
}

function startServices() {
    log('🚀 Iniciando serviços...', 'cyan');
    log('', 'white');

    // 3. Iniciar API Backend
    log('📡 Iniciando API Backend (porta 8000)...', 'cyan');
    const apiProcess = spawn('python', ['api_bridge_real.py'], {
        stdio: ['pipe', 'pipe', 'pipe'],
        detached: false
    });

    apiProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output) {
            log(`[API] ${output}`, 'blue');
        }
    });

    apiProcess.stderr.on('data', (data) => {
        const output = data.toString().trim();
        if (output && !output.includes('INFO:')) {
            log(`[API ERROR] ${output}`, 'red');
        }
    });

    apiProcess.on('close', (code) => {
        log(`[API] Processo encerrado com código ${code}`, 'yellow');
    });

    // Aguardar API inicializar
    setTimeout(() => {
        log('✅ API Backend iniciada', 'green');
        
        // 4. Iniciar Frontend
        log('🌐 Iniciando Dashboard Frontend (porta 3001)...', 'cyan');
        
        const frontendProcess = spawn('npm', ['run', 'dev'], {
            cwd: path.join(__dirname, 'vcm-dashboard-real'),
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true,
            detached: false
        });

        frontendProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                log(`[FRONTEND] ${output}`, 'magenta');
            }
        });

        frontendProcess.stderr.on('data', (data) => {
            const output = data.toString().trim();
            if (output && !output.includes('warn')) {
                log(`[FRONTEND] ${output}`, 'yellow');
            }
        });

        frontendProcess.on('close', (code) => {
            log(`[FRONTEND] Processo encerrado com código ${code}`, 'yellow');
        });

        setTimeout(() => {
            log('✅ Dashboard Frontend iniciado', 'green');
            showSuccessMessage();
        }, 3000);

    }, 3000);

    // 5. Gerenciar encerramento
    process.on('SIGINT', () => {
        log('', 'white');
        log('🛑 Encerrando sistema...', 'yellow');
        
        try {
            apiProcess.kill('SIGINT');
            frontendProcess.kill('SIGINT');
        } catch (error) {
            // Ignore errors when killing processes
        }
        
        log('✅ Sistema encerrado', 'green');
        process.exit(0);
    });
}

function showSuccessMessage() {
    log('', 'white');
    log('========================================', 'cyan');
    log('🎉 VCM INICIADO COM SUCESSO!', 'green');
    log('========================================', 'cyan');
    log('', 'white');
    log('🌐 Dashboard: http://localhost:3001', 'white');
    log('🚀 API Docs:  http://localhost:8000/docs', 'white');
    log('🏥 Health:    http://localhost:8000/health', 'white');
    log('', 'white');
    log('💡 Aguarde alguns segundos para os serviços', 'yellow');
    log('   carregarem completamente...', 'yellow');
    log('', 'white');
    log('⚠️  Para parar: Pressione Ctrl+C', 'yellow');
    log('', 'white');

    // Aguardar e abrir navegador
    setTimeout(() => {
        log('🌐 Abrindo dashboard no navegador...', 'cyan');
        
        const open = require('child_process').exec;
        const url = 'http://localhost:3001';
        
        // Detectar SO e abrir navegador
        let command;
        switch (process.platform) {
            case 'darwin': // macOS
                command = `open ${url}`;
                break;
            case 'win32': // Windows
                command = `start ${url}`;
                break;
            default: // Linux
                command = `xdg-open ${url}`;
        }
        
        open(command, (error) => {
            if (error) {
                log(`⚠️ Não foi possível abrir o navegador automaticamente`, 'yellow');
                log(`🌐 Acesse manualmente: ${url}`, 'white');
            } else {
                log('✅ Dashboard aberto no navegador', 'green');
            }
        });
        
        log('', 'white');
        log('✅ Sistema completamente operacional!', 'green');
    }, 5000);
}

// Iniciar sistema
startSystem().catch((error) => {
    log(`❌ Erro ao iniciar sistema: ${error.message}`, 'red');
    process.exit(1);
});