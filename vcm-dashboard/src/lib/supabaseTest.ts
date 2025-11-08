import type { SupabaseClient } from '@supabase/supabase-js'
import type { Empresa } from '../types/empresa'

export const testSupabaseConnection = async (supabase: SupabaseClient) => {
  console.log('🔍 Testando conexão com Supabase...')
  
  try {
    const { data: healthCheck, error: healthError } = await supabase
      .from('_health_check')
      .select('*')
      .limit(1)
    
    if (healthError && healthError.code !== 'PGRST116') { // PGRST116 = tabela não existe, que é ok
      console.log('⚠️ Erro de health check (normal se tabela não existir):', healthError.message)
    } else {
      console.log('✅ Conexão Supabase OK')
    }

    // Teste 2: Verificar se tabela empresas existe
    const { data: empresas, error: empresasError } = await supabase
      .from(TABLES.EMPRESAS)
      .select('count')
      .limit(1)

    if (empresasError) {
      console.error('❌ Tabela empresas não existe ou erro de acesso:', empresasError)
      return {
        connected: true,
        hasTable: false,
        error: empresasError.message
      }
    }

    console.log('✅ Tabela empresas acessível')
    
    // Teste 3: Contar registros
    const { count, error: countError } = await supabase
      .from(TABLES.EMPRESAS)
      .select('*', { count: 'exact', head: true })

    if (countError) {
      console.error('❌ Erro ao contar registros:', countError)
    } else {
      console.log(`📊 Total de empresas no DB: ${count}`)
    }

    return {
      connected: true,
      hasTable: true,
      count: count || 0
    }

  } catch (error) {
    console.error('❌ Erro geral na conexão:', error)
    return {
      connected: false,
      error: (error as Error).message
    }
  }
}

// SQL para criar a tabela (se necessário)
export const createEmpresasTable = async () => {
  console.log('🔧 Criando tabela empresas...')
  
  const createTableSQL = `
    CREATE TABLE IF NOT EXISTS empresas (
      id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
      codigo VARCHAR(50) UNIQUE NOT NULL,
      nome VARCHAR(255) NOT NULL,
      descricao TEXT,
      pais VARCHAR(10) NOT NULL,
      idiomas JSONB NOT NULL DEFAULT '[]',
      total_personas INTEGER NOT NULL DEFAULT 20,
      status VARCHAR(20) NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa', 'inativa', 'processando')),
      scripts_status JSONB NOT NULL DEFAULT '{
        "biografias": false,
        "competencias": false,
        "tech_specs": false,
        "rag": false,
        "fluxos": false,
        "workflows": false
      }',
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW()
    );

    -- RLS (Row Level Security)
    ALTER TABLE empresas ENABLE ROW LEVEL SECURITY;
    
    -- Política para permitir leitura pública
    CREATE POLICY "Enable read access for all users" ON empresas FOR SELECT USING (true);
    
    -- Política para permitir inserção pública (ajustar conforme necessário)
    CREATE POLICY "Enable insert for all users" ON empresas FOR INSERT WITH CHECK (true);
    
    -- Política para permitir atualização pública (ajustar conforme necessário)
    CREATE POLICY "Enable update for all users" ON empresas FOR UPDATE USING (true);
    
    -- Política para permitir exclusão pública (ajustar conforme necessário)
    CREATE POLICY "Enable delete for all users" ON empresas FOR DELETE USING (true);
  `

  try {
    const { error } = await supabase.rpc('exec_sql', { sql: createTableSQL })
    
    if (error) {
      console.error('❌ Erro ao criar tabela:', error)
      return { success: false, error: error.message }
    }

    console.log('✅ Tabela empresas criada com sucesso')
    return { success: true }
  } catch (error) {
    console.error('❌ Erro ao executar SQL:', error)
    return { success: false, error: (error as Error).message }
  }
}