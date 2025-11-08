import { createClient } from '@supabase/supabase-js'

const VCM_SUPABASE_URL = import.meta.env.VITE_VCM_SUPABASE_URL || 'https://fzyokrvdyeczhfqlwxzb.supabase.co'
const VCM_SUPABASE_ANON_KEY = import.meta.env.VITE_VCM_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ6eW9rcnZkeWVjemhmcWx3eHpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI1MDQzMzAsImV4cCI6MjA3ODA4MDMzMH0.mf3TC1PxNd9pe9M9o-D_lgqZunUl0kPumS0tU4oKodY'

export const supabase = createClient(VCM_SUPABASE_URL, VCM_SUPABASE_ANON_KEY)

// Para operações administrativas (backend apenas)
const VCM_SUPABASE_SERVICE_ROLE_KEY = import.meta.env.VITE_VCM_SUPABASE_SERVICE_ROLE_KEY

export const supabaseAdmin = VCM_SUPABASE_SERVICE_ROLE_KEY 
  ? createClient(VCM_SUPABASE_URL, VCM_SUPABASE_SERVICE_ROLE_KEY)
  : null

// Função para criar cliente de empresa específica
export const createCompanyClient = (companyUrl: string, companyAnonKey: string) => {
  if (!companyAnonKey) {
    console.warn('Chave de API não fornecida para cliente da empresa')
    return null
  }
  return createClient(companyUrl, companyAnonKey)
}

// Cliente LifewayUSA (apenas se as variáveis estiverem configuradas)
const lifewayUrl = import.meta.env.VITE_LIFEWAY_SUPABASE_URL
const lifewayKey = import.meta.env.VITE_LIFEWAY_SUPABASE_SERVICE_KEY

export const lifewayClient = lifewayUrl && lifewayKey 
  ? createCompanyClient(lifewayUrl, lifewayKey)
  : null