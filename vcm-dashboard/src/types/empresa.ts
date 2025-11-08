// Tipos específicos para cada tabela

export interface Empresa {
  id: string
  codigo: string
  nome: string
  descricao?: string
  pais: string
  idiomas: string[]
  total_personas: number
  status: 'ativa' | 'inativa' | 'processando'
  scripts_status: {
    rag: boolean
    fluxos: boolean
    workflows: boolean
    biografias: boolean
    tech_specs: boolean
    competencias: boolean
  }
  created_at: string
  updated_at: string
}

export interface CreateEmpresa {
  codigo: string
  nome: string
  descricao?: string
  pais?: string
  idiomas?: string[]
  total_personas?: number
  status?: 'ativa' | 'inativa' | 'processando'
  scripts_status?: {
    rag?: boolean
    fluxos?: boolean
    workflows?: boolean
    biografias?: boolean
    tech_specs?: boolean
    competencias?: boolean
  }
}

export interface UpdateEmpresa {
  codigo?: string
  nome?: string
  descricao?: string
  pais?: string
  idiomas?: string[]
  total_personas?: number
  status?: 'ativa' | 'inativa' | 'processando'
  scripts_status?: {
    rag?: boolean
    fluxos?: boolean
    workflows?: boolean
    biografias?: boolean
    tech_specs?: boolean
    competencias?: boolean
  }
  updated_at?: string
}

export interface Persona {
  id: string
  persona_code: string
  full_name: string
  role: string
  specialty?: string
  department?: string
  email: string
  whatsapp: string
  empresa_id: string
  biografia_completa?: string
  personalidade: Record<string, any>
  experiencia_anos: number
  ia_config: Record<string, any>
  temperatura_ia: number
  max_tokens: number
  system_prompt?: string
  status: 'active' | 'inactive' | 'archived'
  created_at: string
  updated_at: string
  last_sync: string
}

export interface CreatePersona {
  persona_code: string
  full_name: string
  role: string
  specialty?: string
  department?: string
  email: string
  whatsapp: string
  empresa_id: string
  biografia_completa?: string
  personalidade?: Record<string, any>
  experiencia_anos?: number
  ia_config?: Record<string, any>
  temperatura_ia?: number
  max_tokens?: number
  system_prompt?: string
  status?: 'active' | 'inactive' | 'archived'
}

export interface UpdatePersona {
  persona_code?: string
  full_name?: string
  role?: string
  specialty?: string
  department?: string
  email?: string
  whatsapp?: string
  biografia_completa?: string
  personalidade?: Record<string, any>
  experiencia_anos?: number
  ia_config?: Record<string, any>
  temperatura_ia?: number
  max_tokens?: number
  system_prompt?: string
  status?: 'active' | 'inactive' | 'archived'
  updated_at?: string
  last_sync?: string
}