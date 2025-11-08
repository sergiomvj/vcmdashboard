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
  last_sync?: string
}

export interface PersonaTemplate {
  id: string
  categoria: 'executivos' | 'especialistas' | 'assistentes'
  codigo_template: string
  nome_template: string
  role_template: string
  department_template?: string
  specialty_template?: string
  config_padrao: Record<string, any>
  competencias_padrao: any[]
  ia_config_padrao: Record<string, any>
  biografia_template?: string
  system_prompt_template?: string
  temperatura_padrao: number
  max_tokens_padrao: number
  ordem_criacao: number
  ativo: boolean
}