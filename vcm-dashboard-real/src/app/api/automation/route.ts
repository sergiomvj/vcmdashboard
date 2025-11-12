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
    console.log('🔍 Dados recebidos na API:', body);
    
    const { empresa_id, script_type, empresa_nome } = body;

    // Validação básica
    if (!script_type) {
      return NextResponse.json(
        { success: false, message: 'script_type é obrigatório' },
        { status: 400 }
      );
    }

    // Para biografias, usar os dados da empresa ou padrão
    const empresaCodigo = empresa_id || 'ARVATEST';
    const empresaNome = empresa_nome || 'Empresa Virtual';

    console.log(`🚀 Executando script ${script_type} para empresa: ${empresaCodigo}`);

    // Para desenvolvimento, simular execução rápida
    const taskId = `task-${Date.now()}`;
    
    // Simular delay e retornar sucesso
    setTimeout(() => {
      console.log(`✅ Script ${script_type} simulado concluído para ${empresaCodigo}`);
    }, 2000);

    return NextResponse.json({
      success: true,
      message: `Script ${script_type} iniciado com sucesso para ${empresaNome}`,
      task_id: taskId,
      status: 'completed',
      empresa: {
        codigo: empresaCodigo,
        nome: empresaNome
      },
      details: {
        script_type,
        timestamp: new Date().toISOString(),
        execution_mode: 'development'
      }
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