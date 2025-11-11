import { NextResponse } from 'next/server';
import { readFile, readdir } from 'fs/promises';
import path from 'path';

/**
 * 🏢 API Route para listar empresas disponíveis
 */
export async function GET() {
  try {
    // Lista empresas baseada em diretórios ou configuração
    const empresas = [
      {
        id: 'lifeway',
        nome: 'LifewayUSA',
        status: 'active',
        descricao: 'Empresa de tecnologia focada em soluções inovadoras',
        personas_count: 20,
        created_at: '2024-01-15',
        supabase_url: process.env.LIFEWAY_SUPABASE_URL
      },
      {
        id: 'carntrack',
        nome: 'CarnTrack',
        status: 'planned',
        descricao: 'Sistema de rastreamento automotivo',
        personas_count: 0,
        created_at: null,
        supabase_url: null
      }
    ];

    return NextResponse.json({
      success: true,
      message: 'Empresas listadas com sucesso',
      data: empresas
    });

  } catch (error) {
    console.error('❌ Erro ao listar empresas:', error);
    return NextResponse.json(
      { 
        success: false, 
        message: 'Erro ao listar empresas', 
        error: String(error) 
      },
      { status: 500 }
    );
  }
}