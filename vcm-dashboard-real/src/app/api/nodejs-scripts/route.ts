import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { scriptId, empresaCodigo } = await request.json();

    if (!scriptId || !empresaCodigo) {
      return NextResponse.json(
        { error: 'scriptId e empresaCodigo são obrigatórios' },
        { status: 400 }
      );
    }

    // Mapeamento de scripts
    const scriptPaths = {
      'competencias': 'AUTOMACAO/02_PROCESSAMENTO_PERSONAS/01_generate_competencias.js',
      'tech-specs': 'AUTOMACAO/02_PROCESSAMENTO_PERSONAS/02_generate_tech_specs.js',
      'rag-database': 'AUTOMACAO/02_PROCESSAMENTO_PERSONAS/03_generate_rag.js',
      'fluxos-analise': 'AUTOMACAO/02_PROCESSAMENTO_PERSONAS/04_generate_fluxos_analise.js',
      'workflows-n8n': 'AUTOMACAO/02_PROCESSAMENTO_PERSONAS/05_generate_workflows_n8n.js'
    };

    const scriptPath = scriptPaths[scriptId as keyof typeof scriptPaths];
    
    if (!scriptPath) {
      return NextResponse.json(
        { error: 'Script não encontrado' },
        { status: 404 }
      );
    }

    // Caminho completo do script
    const fullScriptPath = path.join(process.cwd(), scriptPath);
    
    // Comando para executar o script
    const command = `node "${fullScriptPath}" --empresa-codigo ${empresaCodigo}`;
    
    console.log(`Executando: ${command}`);

    // Executar o script com timeout
    const { stdout, stderr } = await execAsync(command, {
      timeout: 300000, // 5 minutos
      cwd: process.cwd()
    });

    return NextResponse.json({
      success: true,
      scriptId,
      empresaCodigo,
      output: stdout,
      error: stderr || null,
      timestamp: new Date().toISOString()
    });

  } catch (error: any) {
    console.error('Erro na execução do script:', error);
    
    return NextResponse.json({
      success: false,
      error: error.message || 'Erro interno do servidor',
      details: error.code === 'ETIMEDOUT' ? 'Timeout na execução' : undefined
    }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'API de execução de scripts Node.js',
    scripts: [
      'competencias',
      'tech-specs', 
      'rag-database',
      'fluxos-analise',
      'workflows-n8n'
    ]
  });
}