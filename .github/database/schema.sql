-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.competencias (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  persona_id uuid NOT NULL,
  tipo character varying NOT NULL CHECK (tipo::text = ANY (ARRAY['principal'::character varying, 'tecnica'::character varying, 'soft_skill'::character varying]::text[])),
  nome character varying NOT NULL,
  descricao text,
  nivel character varying DEFAULT 'avancado'::character varying CHECK (nivel::text = ANY (ARRAY['basico'::character varying, 'intermediario'::character varying, 'avancado'::character varying, 'expert'::character varying]::text[])),
  categoria character varying,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT competencias_pkey PRIMARY KEY (id),
  CONSTRAINT competencias_persona_id_fkey FOREIGN KEY (persona_id) REFERENCES public.personas(id)
);
CREATE TABLE public.empresas (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  codigo character varying NOT NULL UNIQUE,
  nome character varying NOT NULL,
  descricao text,
  pais character varying NOT NULL DEFAULT 'BR'::character varying,
  idiomas ARRAY NOT NULL DEFAULT ARRAY['pt'::text],
  total_personas integer NOT NULL DEFAULT 20,
  status character varying NOT NULL DEFAULT 'ativa'::character varying CHECK (status::text = ANY (ARRAY['ativa'::character varying, 'inativa'::character varying, 'processando'::character varying]::text[])),
  scripts_status jsonb NOT NULL DEFAULT '{"rag": false, "fluxos": false, "workflows": false, "biografias": false, "tech_specs": false, "competencias": false}'::jsonb,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT empresas_pkey PRIMARY KEY (id)
);
CREATE TABLE public.persona_collection_access (
  persona_id uuid NOT NULL,
  collection_id uuid NOT NULL,
  role text NOT NULL DEFAULT 'reader'::text CHECK (role = ANY (ARRAY['reader'::text, 'editor'::text, 'owner'::text])),
  granted_at timestamp with time zone DEFAULT now(),
  granted_by uuid,
  CONSTRAINT persona_collection_access_pkey PRIMARY KEY (persona_id, collection_id),
  CONSTRAINT persona_collection_access_persona_id_fkey FOREIGN KEY (persona_id) REFERENCES public.personas(id),
  CONSTRAINT persona_collection_access_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.rag_collections(id)
);
CREATE TABLE public.personas (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  persona_code character varying NOT NULL UNIQUE,
  full_name character varying NOT NULL,
  role character varying NOT NULL,
  specialty character varying,
  department character varying,
  email character varying NOT NULL UNIQUE,
  whatsapp character varying NOT NULL,
  empresa_id uuid NOT NULL,
  biografia_completa text,
  personalidade jsonb DEFAULT '{}'::jsonb,
  experiencia_anos integer DEFAULT 0,
  ia_config jsonb DEFAULT '{}'::jsonb,
  temperatura_ia numeric DEFAULT 0.7,
  max_tokens integer DEFAULT 2000,
  system_prompt text,
  status character varying DEFAULT 'active'::character varying CHECK (status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying, 'archived'::character varying]::text[])),
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  last_sync timestamp with time zone DEFAULT now(),
  CONSTRAINT personas_pkey PRIMARY KEY (id),
  CONSTRAINT personas_empresa_id_fkey FOREIGN KEY (empresa_id) REFERENCES public.empresas(id)
);
CREATE TABLE public.rag_chunks (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  document_id uuid NOT NULL,
  chunk_index integer NOT NULL,
  content text NOT NULL,
  content_length integer,
  tokens integer,
  metadata jsonb DEFAULT '{}'::jsonb,
  start_char integer,
  end_char integer,
  overlap_prev integer DEFAULT 0,
  overlap_next integer DEFAULT 0,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_chunks_pkey PRIMARY KEY (id),
  CONSTRAINT rag_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.rag_documents(id)
);
CREATE TABLE public.rag_collections (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  code text NOT NULL UNIQUE,
  name text NOT NULL,
  description text,
  visibility text NOT NULL DEFAULT 'public'::text CHECK (visibility = ANY (ARRAY['public'::text, 'internal'::text, 'restricted'::text])),
  tags ARRAY DEFAULT ARRAY[]::text[],
  metadata jsonb DEFAULT '{}'::jsonb,
  is_active boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_collections_pkey PRIMARY KEY (id)
);
CREATE TABLE public.rag_documents (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  collection_id uuid NOT NULL,
  external_id text NOT NULL,
  title text NOT NULL,
  content_raw text,
  content_length integer,
  language text NOT NULL DEFAULT 'en'::text,
  version text DEFAULT 'latest'::text,
  document_type text,
  source_url text,
  checksum text,
  metadata jsonb DEFAULT '{}'::jsonb,
  tags ARRAY DEFAULT ARRAY[]::text[],
  is_active boolean DEFAULT true,
  processed_at timestamp with time zone,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_documents_pkey PRIMARY KEY (id),
  CONSTRAINT rag_documents_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.rag_collections(id)
);
CREATE TABLE public.rag_eval_items (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  eval_set_id uuid NOT NULL,
  query text NOT NULL,
  expected_chunks ARRAY DEFAULT ARRAY[]::uuid[],
  expected_answer text,
  difficulty_level integer CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
  tags ARRAY DEFAULT ARRAY[]::text[],
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_eval_items_pkey PRIMARY KEY (id),
  CONSTRAINT rag_eval_items_eval_set_id_fkey FOREIGN KEY (eval_set_id) REFERENCES public.rag_eval_sets(id)
);
CREATE TABLE public.rag_eval_sets (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  name text NOT NULL UNIQUE,
  description text,
  persona_id uuid,
  collection_ids ARRAY DEFAULT ARRAY[]::uuid[],
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_eval_sets_pkey PRIMARY KEY (id)
);
CREATE TABLE public.rag_feedback (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  persona_id uuid,
  session_id text,
  query text NOT NULL,
  answer_quality integer CHECK (answer_quality >= 1 AND answer_quality <= 5),
  relevance_score numeric CHECK (relevance_score >= 0::numeric AND relevance_score <= 1::numeric),
  response_time_ms integer,
  reasons text,
  top_citations jsonb DEFAULT '[]'::jsonb,
  metadata jsonb DEFAULT '{}'::jsonb,
  user_id uuid,
  created_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_feedback_pkey PRIMARY KEY (id)
);
CREATE TABLE public.rag_ingestion_logs (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  document_id uuid,
  status text NOT NULL CHECK (status = ANY (ARRAY['pending'::text, 'processing'::text, 'completed'::text, 'failed'::text, 'retrying'::text])),
  operation text NOT NULL,
  chunks_created integer DEFAULT 0,
  chunks_updated integer DEFAULT 0,
  processing_time_ms integer,
  error_message text,
  metadata jsonb DEFAULT '{}'::jsonb,
  created_at timestamp with time zone DEFAULT now(),
  completed_at timestamp with time zone,
  CONSTRAINT rag_ingestion_logs_pkey PRIMARY KEY (id),
  CONSTRAINT rag_ingestion_logs_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.rag_documents(id)
);
CREATE TABLE public.rag_knowledge (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  persona_id uuid NOT NULL,
  tipo character varying NOT NULL CHECK (tipo::text = ANY (ARRAY['politica'::character varying, 'procedimento'::character varying, 'documento'::character varying, 'faq'::character varying]::text[])),
  titulo character varying NOT NULL,
  conteudo text NOT NULL,
  chunk_size integer DEFAULT 800,
  tokens_count integer,
  categoria character varying,
  tags jsonb DEFAULT '[]'::jsonb,
  relevancia numeric DEFAULT 1.0,
  ativo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT rag_knowledge_pkey PRIMARY KEY (id),
  CONSTRAINT rag_knowledge_persona_id_fkey FOREIGN KEY (persona_id) REFERENCES public.personas(id)
);
CREATE TABLE public.sync_logs (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  empresa_id uuid NOT NULL,
  tipo_sync character varying NOT NULL,
  status character varying NOT NULL CHECK (status::text = ANY (ARRAY['success'::character varying, 'error'::character varying, 'partial'::character varying]::text[])),
  registros_processados integer DEFAULT 0,
  registros_sucesso integer DEFAULT 0,
  registros_erro integer DEFAULT 0,
  detalhes jsonb DEFAULT '{}'::jsonb,
  error_log text,
  started_at timestamp with time zone DEFAULT now(),
  finished_at timestamp with time zone,
  duration_seconds integer,
  CONSTRAINT sync_logs_pkey PRIMARY KEY (id),
  CONSTRAINT sync_logs_empresa_id_fkey FOREIGN KEY (empresa_id) REFERENCES public.empresas(id)
);
CREATE TABLE public.workflows (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  persona_id uuid NOT NULL,
  nome character varying NOT NULL,
  descricao text,
  tipo character varying NOT NULL CHECK (tipo::text = ANY (ARRAY['tarefa'::character varying, 'fluxo'::character varying, 'responsabilidade'::character varying]::text[])),
  prioridade character varying DEFAULT 'media'::character varying CHECK (prioridade::text = ANY (ARRAY['baixa'::character varying, 'media'::character varying, 'alta'::character varying, 'critica'::character varying]::text[])),
  config jsonb DEFAULT '{}'::jsonb,
  triggers jsonb DEFAULT '[]'::jsonb,
  actions jsonb DEFAULT '[]'::jsonb,
  ativo boolean DEFAULT true,
  created_at timestamp with time zone DEFAULT now(),
  updated_at timestamp with time zone DEFAULT now(),
  CONSTRAINT workflows_pkey PRIMARY KEY (id),
  CONSTRAINT workflows_persona_id_fkey FOREIGN KEY (persona_id) REFERENCES public.personas(id)
);