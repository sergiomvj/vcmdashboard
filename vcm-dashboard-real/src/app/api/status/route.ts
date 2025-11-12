import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    console.log('🔍 API STATUS - Endpoint chamado em:', new Date().toISOString());
    console.log('🔍 NODE_ENV:', process.env.NODE_ENV);
    console.log('🔍 VCM_ENVIRONMENT:', process.env.VCM_ENVIRONMENT);
    console.log('🔍 NEXT_PUBLIC_SUPABASE_URL:', process.env.NEXT_PUBLIC_SUPABASE_URL ? 'SET' : 'NOT_SET');
    
    // Mock data com timestamp para verificar se está atualizando
    const mockExecutionStatus = {
      biografia: { running: false, last_run: new Date().toISOString(), last_result: 'success' },
      script_1: { running: false, last_run: new Date().toISOString(), last_result: 'idle' },
      script_2: { running: false, last_run: null, last_result: 'idle' },
      script_3: { running: false, last_run: null, last_result: 'idle' },
      script_4: { running: false, last_run: null, last_result: 'idle' },
      script_5: { running: false, last_run: null, last_result: 'idle' },
      cascade: { running: false, last_run: null, last_result: 'idle' },
      _debug: {
        timestamp: new Date().toISOString(),
        status: 'API_WORKING',
        version: '3.0',
        node_env: process.env.NODE_ENV || 'unknown',
        vcm_env: process.env.VCM_ENVIRONMENT || 'not_set',
        supabase_configured: !!process.env.NEXT_PUBLIC_SUPABASE_URL,
        build_time: new Date().toISOString()
      }
    };

    console.log('✅ Retornando status:', mockExecutionStatus);
    
    return NextResponse.json(mockExecutionStatus, {
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