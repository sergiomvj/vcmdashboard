import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function GET() {
  try {
    console.log('🔍 API STATUS - Endpoint chamado em:', new Date().toISOString());
    console.log('🔍 NODE_ENV:', process.env.NODE_ENV);
    console.log('🔍 NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL ? 'SET' : 'NOT_SET');
    
    // Buscar dados reais das empresas no Supabase
    const { data: empresas, error: empresasError } = await supabase
      .from('empresas')
      .select('*')
      .order('created_at', { ascending: false });

    if (empresasError) {
      console.error('❌ Erro ao buscar empresas:', empresasError);
    }

    // Buscar configurações do sistema
    const { data: configs, error: configsError } = await supabase
      .from('system_configurations')
      .select('*');

    if (configsError) {
      console.error('❌ Erro ao buscar configurações:', configsError);
    }

    const realExecutionStatus = {
      biografia: { 
        running: false, 
        last_run: empresas?.[0]?.updated_at || new Date().toISOString(), 
        last_result: (empresas && empresas.length > 0) ? 'success' : 'idle',
        companies_count: empresas?.length || 0
      },
      script_1: { 
        running: false, 
        last_run: null, 
        last_result: 'idle'
      },
      script_2: { running: false, last_run: null, last_result: 'idle' },
      script_3: { running: false, last_run: null, last_result: 'idle' },
      script_4: { running: false, last_run: null, last_result: 'idle' },
      script_5: { running: false, last_run: null, last_result: 'idle' },
      cascade: { running: false, last_run: null, last_result: 'idle' },
      _debug: {
        timestamp: new Date().toISOString(),
        status: 'API_WORKING_REAL',
        version: '4.0-supabase',
        node_env: process.env.NODE_ENV || 'unknown',
        supabase_connected: !empresasError,
        empresas_count: empresas?.length || 0,
        configs_count: configs?.length || 0,
        build_time: new Date().toISOString()
      },
      _empresas: empresas || []
    };

    console.log('✅ Retornando status REAL:', realExecutionStatus);
    
    return NextResponse.json(realExecutionStatus, {
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    });
  } catch (error) {
    console.error('Erro ao buscar status:', error);
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    );
  }
}