export interface RAGKnowledge {
  id: string
  persona_id: string
  tipo: 'politica' | 'procedimento' | 'documento' | 'faq'
  titulo: string
  conteudo: string
  chunk_size: number
  tokens_count?: number
  categoria?: string
  tags: Record<string, any>
  relevancia: number
  ativo: boolean
  created_at: string
  updated_at: string
}

export interface CreateRAGKnowledge {
  persona_id: string
  tipo: 'politica' | 'procedimento' | 'documento' | 'faq'
  titulo: string
  conteudo: string
  chunk_size?: number
  tokens_count?: number
  categoria?: string
  tags?: Record<string, any>
  relevancia?: number
  ativo?: boolean
}

export interface UpdateRAGKnowledge {
  tipo?: 'politica' | 'procedimento' | 'documento' | 'faq'
  titulo?: string
  conteudo?: string
  chunk_size?: number
  tokens_count?: number
  categoria?: string
  tags?: Record<string, any>
  relevancia?: number
  ativo?: boolean
  updated_at?: string
}

export interface RAGFeedback {
  id: string
  persona_id?: string
  session_id?: string
  query: string
  answer_quality: number
  relevance_score: number
  response_time_ms?: number
  reasons?: string
  top_citations: Record<string, any>[]
  metadata: Record<string, any>
  user_id?: string
  created_at: string
}

export interface CreateRAGFeedback {
  persona_id?: string
  session_id?: string
  query: string
  answer_quality: number
  relevance_score: number
  response_time_ms?: number
  reasons?: string
  top_citations?: Record<string, any>[]
  metadata?: Record<string, any>
  user_id?: string
}

export interface UpdateRAGFeedback {
  answer_quality?: number
  relevance_score?: number
  response_time_ms?: number
  reasons?: string
  top_citations?: Record<string, any>[]
  metadata?: Record<string, any>
}

export interface RAGIngestionLog {
  id: string
  document_id?: string
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'retrying'
  operation: string
  chunks_created: number
  chunks_updated: number
  processing_time_ms?: number
  error_message?: string
  metadata: Record<string, any>
  created_at: string
  completed_at?: string
}

export interface CreateRAGIngestionLog {
  document_id?: string
  status: 'pending' | 'processing' | 'completed' | 'failed' | 'retrying'
  operation: string
  chunks_created?: number
  chunks_updated?: number
  processing_time_ms?: number
  error_message?: string
  metadata?: Record<string, any>
}

export interface UpdateRAGIngestionLog {
  status?: 'pending' | 'processing' | 'completed' | 'failed' | 'retrying'
  chunks_created?: number
  chunks_updated?: number
  processing_time_ms?: number
  error_message?: string
  completed_at?: string
}