export interface Competencia {
  id: string
  persona_id: string
  tipo: 'principal' | 'tecnica' | 'soft_skill'
  nome: string
  descricao?: string
  nivel: 'basico' | 'intermediario' | 'avancado' | 'expert'
  categoria?: string
  created_at: string
}

export interface CreateCompetencia {
  persona_id: string
  tipo: 'principal' | 'tecnica' | 'soft_skill'
  nome: string
  descricao?: string
  nivel?: 'basico' | 'intermediario' | 'avancado' | 'expert'
  categoria?: string
}

export interface UpdateCompetencia {
  tipo?: 'principal' | 'tecnica' | 'soft_skill'
  nome?: string
  descricao?: string
  nivel?: 'basico' | 'intermediario' | 'avancado' | 'expert'
  categoria?: string
}

export interface Workflow {
  id: string
  persona_id: string
  nome: string
  descricao?: string
  tipo: 'tarefa' | 'fluxo' | 'responsabilidade'
  prioridade: 'baixa' | 'media' | 'alta' | 'critica'
  config: Record<string, any>
  triggers: Record<string, any>[]
  actions: Record<string, any>[]
  ativo: boolean
  created_at: string
  updated_at: string
}

export interface CreateWorkflow {
  persona_id: string
  nome: string
  descricao?: string
  tipo: 'tarefa' | 'fluxo' | 'responsabilidade'
  prioridade?: 'baixa' | 'media' | 'alta' | 'critica'
  config?: Record<string, any>
  triggers?: Record<string, any>[]
  actions?: Record<string, any>[]
  ativo?: boolean
}

export interface UpdateWorkflow {
  nome?: string
  descricao?: string
  tipo?: 'tarefa' | 'fluxo' | 'responsabilidade'
  prioridade?: 'baixa' | 'media' | 'alta' | 'critica'
  config?: Record<string, any>
  triggers?: Record<string, any>[]
  actions?: Record<string, any>[]
  ativo?: boolean
  updated_at?: string
}

export interface SyncLog {
  id: string
  empresa_id: string
  tipo_sync: string
  status: 'success' | 'error' | 'partial'
  registros_processados: number
  registros_sucesso: number
  registros_erro: number
  detalhes: Record<string, any>
  error_log?: string
  started_at: string
  finished_at?: string
  duration_seconds?: number
}

export interface CreateSyncLog {
  empresa_id: string
  tipo_sync: string
  status: 'success' | 'error' | 'partial'
  registros_processados?: number
  registros_sucesso?: number
  registros_erro?: number
  detalhes?: Record<string, any>
  error_log?: string
}

export interface UpdateSyncLog {
  status?: 'success' | 'error' | 'partial'
  registros_processados?: number
  registros_sucesso?: number
  registros_erro?: number
  detalhes?: Record<string, any>
  error_log?: string
  finished_at?: string
  duration_seconds?: number
}