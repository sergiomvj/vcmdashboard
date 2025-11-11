import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

/**
 * 🔗 API Route para executar automação VCM
 * Executa scripts Python diretamente do Next.js
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { empresa_id, script_type, force_update } = body;

    // Validação básica
    if (!empresa_id || !script_type) {
      return NextResponse.json(
        { success: false, message: 'empresa_id e script_type são obrigatórios' },
        { status: 400 }
      );
    }

    // Caminhos dos scripts
    const scriptPaths = {
      biografia: '../AUTOMACAO/01_SETUP_E_CRIACAO/05_auto_biografia_generator.py',
      competencias: '../AUTOMACAO/02_PROCESSAMENTO_PERSONAS/01_generate_competencias.py',
      tech_specs: '../AUTOMACAO/02_PROCESSAMENTO_PERSONAS/02_generate_tech_specs.py',
      rag: '../AUTOMACAO/02_PROCESSAMENTO_PERSONAS/03_generate_rag.py',
      workflows: '../AUTOMACAO/02_PROCESSAMENTO_PERSONAS/05_generate_workflows_n8n.py',
    };

    const scriptPath = scriptPaths[script_type as keyof typeof scriptPaths];
    if (!scriptPath) {
      return NextResponse.json(
        { success: false, message: 'Script type inválido' },
        { status: 400 }
      );
    }

    // Executar script Python
    const taskId = `task-${Date.now()}`;
    const command = `python "${path.resolve(scriptPath)}" --empresa-id="${empresa_id}"`;
    
    console.log(`🚀 Executando: ${command}`);

    // Execução assíncrona (não bloqueia a resposta)
    execAsync(command).then((result) => {
      console.log(`✅ Script ${script_type} concluído:`, result.stdout);
    }).catch((error) => {
      console.error(`❌ Erro no script ${script_type}:`, error);
    });

    return NextResponse.json({
      success: true,
      message: `Executando ${script_type} para ${empresa_id}`,
      task_id: taskId,
      status: 'running'
    });

  } catch (error) {
    console.error('❌ Erro na API de automação:', error);
    return NextResponse.json(
      { success: false, message: 'Erro interno do servidor', error: String(error) },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'VCM Automation API',
    available_scripts: [
      'biografia',
      'competencias', 
      'tech_specs',
      'rag',
      'workflows'
    ]
  });
}