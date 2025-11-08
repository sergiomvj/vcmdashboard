import { supabase } from '../lib/supabase'

export const setupDatabase = async () => {
  console.log('🚀 Iniciando setup do banco de dados...')

  try {
    // Tentar fazer uma consulta simples para verificar se a tabela existe
    const { data, error } = await supabase
      .from('empresas')
      .select('count(*)')
      .limit(1)

    if (error) {
      if (error.message.includes('relation "empresas" does not exist')) {
        console.log('❌ Tabela "empresas" não existe!')
        console.log('📝 Execute o SQL manualmente no Supabase Dashboard:')
        console.log('   1. Acesse: https://supabase.com/dashboard')
        console.log('   2. Selecione seu projeto VCM')
        console.log('   3. Vá em SQL Editor')
        console.log('   4. Execute o conteúdo do arquivo: sql/create_tables.sql')
        return {
          success: false,
          message: 'Tabela empresas não existe. Execute o SQL manualmente.',
          needsManualSetup: true
        }
      } else {
        console.error('❌ Erro na verificação:', error.message)
        return {
          success: false,
          message: `Erro: ${error.message}`,
          needsManualSetup: false
        }
      }
    }

    console.log('✅ Tabela empresas existe!')
    
    // Verificar se há dados  
    const recordCount = Array.isArray(data) ? data.length : 0
    console.log(`📊 Registros encontrados: ${recordCount}`)

    return {
      success: true,
      message: `Banco configurado corretamente! ${recordCount} empresas encontradas.`,
      needsManualSetup: false,
      recordCount: recordCount
    }

  } catch (error) {
    console.error('❌ Erro no setup:', error)
    return {
      success: false,
      message: `Erro inesperado: ${(error as Error).message}`,
      needsManualSetup: false
    }
  }
}

export const testConnection = async () => {
  console.log('🔗 Testando conexão com Supabase...')

  try {
    const { data, error } = await supabase
      .from('empresas')
      .select('id, codigo, nome')
      .limit(5)

    if (error) {
      console.error('❌ Erro na conexão:', error.message)
      return {
        success: false,
        error: error.message
      }
    }

    console.log('✅ Conexão OK!')
    console.log('📊 Empresas encontradas:', data)

    return {
      success: true,
      data: data || []
    }

  } catch (error) {
    console.error('❌ Erro inesperado:', error)
    return {
      success: false,
      error: (error as Error).message
    }
  }
}