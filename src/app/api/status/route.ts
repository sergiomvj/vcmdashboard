import { NextResponse } from 'next/server';

/**
 * 📊 API Route para status de execução dos scripts
 */
export async function GET() {
  try {
    // Status simulado para desenvolvimento
    const executionStatus = {
      biografia: { 
        running: false, 
        last_run: new Date(Date.now() - 3600000).toISOString(), 
        last_result: { success: true, message: 'Biografias geradas com sucesso' }
      },
      script_1: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      script_2: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      script_3: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      script_4: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      script_5: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      cascade: { 
        running: false, 
        last_run: null, 
        last_result: null 
      },
      api_mode: 'next-routes',
      message: 'Sistema funcionando com API routes integradas',
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(executionStatus);

  } catch (error) {
    console.error('❌ Erro ao buscar status:', error);
    return NextResponse.json(
      { 
        success: false, 
        message: 'Erro ao buscar status de execução', 
        error: String(error) 
      },
      { status: 500 }
    );
  }
}