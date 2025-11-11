import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

export async function GET() {
  try {
    // Mock data para development - normalmente isto viria de um banco de dados ou arquivo de log
    const mockExecutionStatus = {
      biografia: { running: false, last_run: null, last_result: null },
      script_1: { running: false, last_run: null, last_result: null },
      script_2: { running: false, last_run: null, last_result: null },
      script_3: { running: false, last_run: null, last_result: null },
      script_4: { running: false, last_run: null, last_result: null },
      script_5: { running: false, last_run: null, last_result: null },
      cascade: { running: false, last_run: null, last_result: null },
    };

    return NextResponse.json(mockExecutionStatus);
  } catch (error) {
    console.error('Erro ao buscar status:', error);
    return NextResponse.json(
      { error: 'Erro interno do servidor' },
      { status: 500 }
    );
  }
}