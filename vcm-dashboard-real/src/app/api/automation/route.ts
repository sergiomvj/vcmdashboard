import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, scriptNumber, force_regenerate, ...otherParams } = body;
    
    // Determinar qual script executar baseado na ação
    let scriptPath = '';
    let args: string[] = [];
    
    switch (action) {
      case 'generate-biografias':
        scriptPath = path.join(process.cwd(), '../AUTOMACAO/01_SETUP_E_CRIACAO/05_auto_biografia_generator.py');
        break;
        
      case 'run-script':
        if (!scriptNumber || scriptNumber < 1 || scriptNumber > 5) {
          return NextResponse.json({ error: 'Número do script deve ser entre 1 e 5' }, { status: 400 });
        }
        const scriptFiles = [
          '01_generate_competencias.py',
          '02_generate_tech_specs.py', 
          '03_generate_rag.py',
          '04_generate_fluxos_analise.py',
          '05_generate_workflows_n8n.py'
        ];
        scriptPath = path.join(process.cwd(), `../AUTOMACAO/02_PROCESSAMENTO_PERSONAS/${scriptFiles[scriptNumber - 1]}`);
        if (force_regenerate) {
          args.push('--force-regenerate');
        }
        break;
        
      case 'run-cascade':
        // Para cascata, executamos o script que roda todos em sequência
        scriptPath = path.join(process.cwd(), '../AUTOMACAO/03_ORGANIZACAO_E_MANUTENCAO/04_test_scripts_4_5.py');
        break;
        
      default:
        return NextResponse.json({ error: 'Ação não reconhecida' }, { status: 400 });
    }

    return new Promise((resolve) => {
      const pythonProcess = spawn('python', [scriptPath, ...args], {
        cwd: path.dirname(scriptPath),
        env: process.env,
      });

      let output = '';
      let error = '';

      pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        error += data.toString();
      });

      pythonProcess.on('close', (code) => {
        const response = {
          success: code === 0,
          code,
          output: output || 'Processo executado com sucesso',
          error: error || null,
          action,
          scriptNumber: scriptNumber || null,
        };

        resolve(NextResponse.json(response));
      });

      pythonProcess.on('error', (err) => {
        resolve(NextResponse.json({
          success: false,
          error: `Erro ao executar script: ${err.message}`,
          action,
          scriptNumber: scriptNumber || null,
        }, { status: 500 }));
      });
    });

  } catch (error) {
    console.error('Erro na API de automação:', error);
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    );
  }
}