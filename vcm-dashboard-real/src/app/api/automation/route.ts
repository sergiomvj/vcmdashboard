import { NextRequest, NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { action, ...otherParams } = body;
    
    console.log('API automation:', action);
    
    if (action === 'generate-biografias') {
      const novaEmpresa = {
        codigo: otherParams.codigo || 'NEW_COMPANY',
        nome: otherParams.nome || 'Nova Empresa',
        descricao: otherParams.descricao || '',
        industria: otherParams.industria || 'Tecnologia',
        pais: otherParams.pais || 'Brasil',
        idiomas: otherParams.idiomas || ['pt'],
        total_personas: otherParams.total_personas || 20,
        status: 'ativa' as const,
        scripts_status: {
          biografias: true,
          competencias: false,
          tech_specs: false,
          rag: false,
          fluxos: false,
          workflows: false
        }
      };
      
      const { data: empresaCriada, error: empresaError } = await supabase
        .from('empresas')
        .insert([novaEmpresa])
        .select()
        .single();
        
      if (empresaError) {
        return NextResponse.json({
          success: false,
          message: empresaError.message
        }, { status: 500 });
      }
      
      return NextResponse.json({
        success: true,
        message: 'Nova empresa criada!',
        data: empresaCriada
      });
    }
    
    return NextResponse.json({
      success: false,
      message: 'Ação não reconhecida'
    }, { status: 400 });
    
  } catch (error) {
    return NextResponse.json({
      success: false,
      message: 'Erro interno'
    }, { status: 500 });
  }
}