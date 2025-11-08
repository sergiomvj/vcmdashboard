export interface RAGCollection {
  id: string
  code: string
  name: string
  description?: string
  visibility: 'public' | 'internal' | 'restricted'
  tags: string[]
  metadata: Record<string, any>
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface CreateRAGCollection {
  code: string
  name: string
  description?: string
  visibility?: 'public' | 'internal' | 'restricted'
  tags?: string[]
  metadata?: Record<string, any>
  is_active?: boolean
}

export interface UpdateRAGCollection {
  name?: string
  description?: string
  visibility?: 'public' | 'internal' | 'restricted'
  tags?: string[]
  metadata?: Record<string, any>
  is_active?: boolean
  updated_at?: string
}

export interface RAGDocument {
  id: string
  collection_id: string
  external_id: string
  title: string
  content_raw?: string
  content_length?: number
  language: string
  version: string
  document_type?: string
  source_url?: string
  checksum?: string
  metadata: Record<string, any>
  tags: string[]
  is_active: boolean
  processed_at?: string
  created_at: string
  updated_at: string
}

export interface CreateRAGDocument {
  collection_id: string
  external_id: string
  title: string
  content_raw?: string
  language?: string
  version?: string
  document_type?: string
  source_url?: string
  checksum?: string
  metadata?: Record<string, any>
  tags?: string[]
  is_active?: boolean
}

export interface UpdateRAGDocument {
  title?: string
  content_raw?: string
  language?: string
  version?: string
  document_type?: string
  source_url?: string
  checksum?: string
  metadata?: Record<string, any>
  tags?: string[]
  is_active?: boolean
  processed_at?: string
  updated_at?: string
}

export interface RAGChunk {
  id: string
  document_id: string
  chunk_index: number
  content: string
  content_length?: number
  tokens?: number
  metadata: Record<string, any>
  start_char?: number
  end_char?: number
  overlap_prev: number
  overlap_next: number
  created_at: string
}

export interface CreateRAGChunk {
  document_id: string
  chunk_index: number
  content: string
  content_length?: number
  tokens?: number
  metadata?: Record<string, any>
  start_char?: number
  end_char?: number
  overlap_prev?: number
  overlap_next?: number
}

export interface UpdateRAGChunk {
  content?: string
  content_length?: number
  tokens?: number
  metadata?: Record<string, any>
  start_char?: number
  end_char?: number
  overlap_prev?: number
  overlap_next?: number
}