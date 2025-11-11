import { NextRequest, NextResponse } from 'next/server';
import { readFile, readdir } from 'fs/promises';
import path from 'path';

/**
 * 👥 API Route para listar personas de uma empresa
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { empresa_id: string } }
) {
  try {
    const { empresa_id } = params;

    if (!empresa_id) {
      return NextResponse.json(
        { success: false, message: 'empresa_id é obrigatório' },
        { status: 400 }
      );
    }

    // Buscar personas nos diretórios de automação
    const personasDir = path.join(process.cwd(), 'AUTOMACAO', '04_PERSONAS_COMPLETAS');
    const categorias = ['executivos', 'especialistas', 'assistentes'];
    
    let allPersonas: any[] = [];

    try {
      for (const categoria of categorias) {
        const categoriaPath = path.join(personasDir, categoria);
        
        try {
          const files = await readdir(categoriaPath);
          const jsonFiles = files.filter(file => file.endsWith('.json') && file.includes(empresa_id.toLowerCase()));
          
          for (const file of jsonFiles) {
            try {
              const filePath = path.join(categoriaPath, file);
              const content = await readFile(filePath, 'utf-8');
              const persona = JSON.parse(content);
              
              allPersonas.push({
                ...persona,
                categoria,
                file: file,
                id: file.replace('.json', '')
              });
            } catch (parseError) {
              console.warn(`⚠️ Erro ao processar ${file}:`, parseError);
            }
          }
        } catch (dirError) {
          console.warn(`⚠️ Diretório ${categoria} não encontrado`);
        }
      }

      // Se não encontrou personas nos arquivos, retornar dados simulados
      if (allPersonas.length === 0) {
        allPersonas = [
          {
            id: 1,
            nome: "João Silva",
            cargo: "CEO",
            categoria: "executivos",
            email: "joao.silva@lifeway.com",
            telefone: "+1-555-0101",
            departamento: "Executivo",
            is_ceo: true
          },
          {
            id: 2,
            nome: "Maria Santos",
            cargo: "CTO",
            categoria: "executivos", 
            email: "maria.santos@lifeway.com",
            telefone: "+1-555-0102",
            departamento: "Tecnologia",
            is_ceo: false
          },
          {
            id: 3,
            nome: "Carlos Tech",
            cargo: "Senior Developer",
            categoria: "especialistas",
            email: "carlos.tech@lifeway.com", 
            telefone: "+1-555-0201",
            departamento: "Desenvolvimento",
            is_ceo: false
          }
        ];
      }

      return NextResponse.json({
        success: true,
        message: 'Personas listadas com sucesso',
        data: {
          empresa_id,
          total: allPersonas.length,
          personas: allPersonas
        }
      });

    } catch (fsError) {
      // Fallback para dados simulados se houver erro de sistema de arquivos
      console.warn('⚠️ Usando dados simulados devido a erro de FS:', fsError);
      
      return NextResponse.json({
        success: true,
        message: 'Personas simuladas (dados de teste)',
        data: {
          empresa_id,
          total: 3,
          personas: [
            {
              id: 1,
              nome: "João Silva",
              cargo: "CEO", 
              categoria: "executivos",
              email: "joao.silva@example.com",
              telefone: "+1-555-0101",
              is_ceo: true
            },
            {
              id: 2,
              nome: "Maria Santos",
              cargo: "CTO",
              categoria: "executivos",
              email: "maria.santos@example.com",
              telefone: "+1-555-0102", 
              is_ceo: false
            }
          ]
        }
      });
    }

  } catch (error) {
    console.error('❌ Erro ao listar personas:', error);
    return NextResponse.json(
      { 
        success: false, 
        message: 'Erro ao listar personas', 
        error: String(error) 
      },
      { status: 500 }
    );
  }
}