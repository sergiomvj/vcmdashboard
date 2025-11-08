export interface RAGEvalSet {
  id: string
  name: string
  description?: string
  persona_id?: string
  collection_ids: string[]
  metadata: Record<string, any>
  created_at: string
}

export interface CreateRAGEvalSet {
  name: string
  description?: string
  persona_id?: string
  collection_ids?: string[]
  metadata?: Record<string, any>
}

export interface UpdateRAGEvalSet {
  name?: string
  description?: string
  persona_id?: string
  collection_ids?: string[]
  metadata?: Record<string, any>
}

export interface RAGEvalItem {
  id: string
  eval_set_id: string
  query: string
  expected_chunks: string[]
  expected_answer?: string
  difficulty_level: number
  tags: string[]
  created_at: string
}

export interface CreateRAGEvalItem {
  eval_set_id: string
  query: string
  expected_chunks?: string[]
  expected_answer?: string
  difficulty_level?: number
  tags?: string[]
}

export interface UpdateRAGEvalItem {
  query?: string
  expected_chunks?: string[]
  expected_answer?: string
  difficulty_level?: number
  tags?: string[]
}

export interface PersonaCollectionAccess {
  persona_id: string
  collection_id: string
  role: 'reader' | 'editor' | 'owner'
  granted_at: string
  granted_by?: string
}

export interface CreatePersonaCollectionAccess {
  persona_id: string
  collection_id: string
  role?: 'reader' | 'editor' | 'owner'
  granted_by?: string
}

export interface UpdatePersonaCollectionAccess {
  role?: 'reader' | 'editor' | 'owner'
  granted_by?: string
}

// Export all types
export * from './database'
export * from './empresa'
export * from './competencia'
export * from './rag'
export * from './rag-knowledge'
export * from './rag-eval'