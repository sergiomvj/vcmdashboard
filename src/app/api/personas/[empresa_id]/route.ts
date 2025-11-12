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
    const personasDir = path.join(process.cwd(), 'AUTOMACAO', '04_BIOS_PERSONAS');
    const personasConfigPath = path.join(process.cwd(), 'AUTOMACAO', 'personas_config.json');
    
    // Primeiro, carregar configuração das personas
    let personasConfig: any = {};
    try {
      const configContent = await readFile(personasConfigPath, 'utf-8');
      personasConfig = JSON.parse(configContent);
    } catch (configError) {
      console.warn('⚠️ Erro ao carregar personas_config.json:', configError);
    }
    
    const categorias = ['executivos', 'especialistas', 'assistentes'];
    
    let allPersonas: any[] = [];

    try {
      for (const categoria of categorias) {
        const categoriaPath = path.join(personasDir, categoria);
        
        try {
          const folders = await readdir(categoriaPath);
          
          for (const folderName of folders) {
            if (folderName === 'test_persona.md') continue; // Pular arquivo de teste
            
            const personaFolderPath = path.join(categoriaPath, folderName);
            const bioFile = `${folderName}_bio.md`;
            const bioFilePath = path.join(personaFolderPath, bioFile);
            
            try {
              const bioContent = await readFile(bioFilePath, 'utf-8');
              
              // Extrair informações básicas do markdown
              const lines = bioContent.split('\n');
              const nomeCompleto = lines[0]?.replace('# ', '').split(' - ')[0] || folderName.replace(/_/g, ' ');
              const cargo = lines[0]?.split(' - ')[1] || 'N/A';
              
              // Buscar dados estruturados no personas_config.json
              let personaData = null;
              if (personasConfig?.ceo && personasConfig.ceo.nomeCompleto === nomeCompleto) {
                personaData = personasConfig.ceo;
              } else if (personasConfig) {
                // Buscar nas outras categorias
                for (const [cat, personas] of Object.entries(personasConfig)) {
                  if (typeof personas === 'object' && personas !== null && !Array.isArray(personas)) {
                    for (const [id, persona] of Object.entries(personas as any)) {
                      if ((persona as any)?.nomeCompleto === nomeCompleto) {
                        personaData = persona;
                        break;
                      }
                    }
                  }
                  if (personaData) break;
                }
              }
              
              allPersonas.push({
                id: folderName,
                nome: nomeCompleto,
                cargo: cargo,
                categoria: categoria,
                email: `${folderName.toLowerCase().replace(/_/g, '.')}@${empresa_id.toLowerCase()}.com`,
                telefone: "+55-11-9999-" + Math.floor(1000 + Math.random() * 9000),
                departamento: categoria.charAt(0).toUpperCase() + categoria.slice(1),
                is_ceo: cargo === 'CEO',
                biografia_markdown: bioContent,
                dados_estruturados: personaData,
                folder_path: folderName,
                bio_file: bioFile
              });
            } catch (bioError) {
              console.warn(`⚠️ Erro ao ler biografia ${bioFile}:`, bioError);
            }
          }
        } catch (dirError) {
          console.warn(`⚠️ Diretório ${categoria} não encontrado:`, dirError);
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