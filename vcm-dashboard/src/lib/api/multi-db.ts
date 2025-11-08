import { createClient } from '@supabase/supabase-js'
import type { Empresa } from '../../types/empresa'

export const createCompanyClient = (empresa: Empresa) => {
  if (!empresa.supabase_url || !empresa.supabase_anon_key) {
    throw new Error(`A empresa ${empresa.nome_empresa} não possui as credenciais do Supabase configuradas.`)
  }

  return createClient(
    empresa.supabase_url,
    empresa.supabase_anon_key
  )
}
