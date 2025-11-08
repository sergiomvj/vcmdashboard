-- ===================================================
-- VCM Dashboard - Schema SIMPLES e FUNCIONAL
-- ===================================================

-- Extensões
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Empresas (NOVA TABELA - não existe no schema original)
CREATE TABLE IF NOT EXISTS empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    pais VARCHAR(10) NOT NULL DEFAULT 'BR',
    idiomas TEXT[] NOT NULL DEFAULT ARRAY['pt'],
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Personas (COMPATÍVEL com schema existente)
CREATE TABLE IF NOT EXISTS personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_code VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    specialty VARCHAR,
    department VARCHAR,
    email VARCHAR NOT NULL UNIQUE,
    whatsapp VARCHAR NOT NULL,
    empresa_id VARCHAR NOT NULL DEFAULT 'lifewayusa',  -- VARCHAR como no schema original
    biografia_completa TEXT,
    personalidade JSONB DEFAULT '{}'::jsonb,
    experiencia_anos INTEGER DEFAULT 0,
    ia_config JSONB DEFAULT '{}'::jsonb,
    temperatura_ia NUMERIC DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2000,
    system_prompt TEXT,
    status VARCHAR DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Competencias
CREATE TABLE IF NOT EXISTS competencias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('principal', 'tecnica', 'soft_skill')),
    nome VARCHAR NOT NULL,
    descricao TEXT,
    nivel VARCHAR DEFAULT 'avancado' CHECK (nivel IN ('basico', 'intermediario', 'avancado', 'expert')),
    categoria VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Workflows
CREATE TABLE IF NOT EXISTS workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    nome VARCHAR NOT NULL,
    descricao TEXT,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('tarefa', 'fluxo', 'responsabilidade')),
    prioridade VARCHAR DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    config JSONB DEFAULT '{}'::jsonb,
    triggers JSONB DEFAULT '[]'::jsonb,
    actions JSONB DEFAULT '[]'::jsonb,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Sync Logs (COMPATÍVEL)
CREATE TABLE IF NOT EXISTS sync_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id VARCHAR NOT NULL,  -- VARCHAR como no schema original
    tipo_sync VARCHAR NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('success', 'error', 'partial')),
    registros_processados INTEGER DEFAULT 0,
    registros_sucesso INTEGER DEFAULT 0,
    registros_erro INTEGER DEFAULT 0,
    detalhes JSONB DEFAULT '{}'::jsonb,
    error_log TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER
);

-- 6. RAG Collections (COMPATÍVEL com uuid_generate_v4)
CREATE TABLE IF NOT EXISTS rag_collections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    visibility TEXT NOT NULL DEFAULT 'public' CHECK (visibility IN ('public', 'internal', 'restricted')),
    tags TEXT[] DEFAULT ARRAY[]::text[],
    metadata JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. RAG Documents (COMPATÍVEL)
CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    collection_id UUID NOT NULL REFERENCES rag_collections(id) ON DELETE CASCADE,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content_raw TEXT,
    content_length INTEGER,
    language TEXT NOT NULL DEFAULT 'en',
    version TEXT DEFAULT 'latest',
    document_type TEXT,
    source_url TEXT,
    checksum TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    tags TEXT[] DEFAULT ARRAY[]::text[],
    is_active BOOLEAN DEFAULT TRUE,
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 8. RAG Chunks (COMPATÍVEL sem embedding)
CREATE TABLE IF NOT EXISTS rag_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    content_length INTEGER,
    tokens INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    start_char INTEGER,
    end_char INTEGER,
    overlap_prev INTEGER DEFAULT 0,
    overlap_next INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. RAG Knowledge
CREATE TABLE IF NOT EXISTS rag_knowledge (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('politica', 'procedimento', 'documento', 'faq')),
    titulo VARCHAR NOT NULL,
    conteudo TEXT NOT NULL,
    chunk_size INTEGER DEFAULT 800,
    tokens_count INTEGER,
    categoria VARCHAR,
    tags JSONB DEFAULT '[]'::jsonb,
    relevancia NUMERIC DEFAULT 1.0,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 10. Persona Collection Access (COMPATÍVEL)
CREATE TABLE IF NOT EXISTS persona_collection_access (
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    collection_id UUID NOT NULL REFERENCES rag_collections(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'reader' CHECK (role IN ('reader', 'editor', 'owner')),
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by UUID,
    PRIMARY KEY (persona_id, collection_id)
);

-- 11. RAG Eval Sets (do schema original)
CREATE TABLE IF NOT EXISTS rag_eval_sets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    persona_id UUID,
    collection_ids UUID[] DEFAULT ARRAY[]::uuid[],
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 12. RAG Eval Items (do schema original)
CREATE TABLE IF NOT EXISTS rag_eval_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    eval_set_id UUID NOT NULL REFERENCES rag_eval_sets(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    expected_chunks UUID[] DEFAULT ARRAY[]::uuid[],
    expected_answer TEXT,
    difficulty_level INTEGER CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    tags TEXT[] DEFAULT ARRAY[]::text[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 13. RAG Feedback (do schema original)
CREATE TABLE IF NOT EXISTS rag_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    persona_id UUID,
    session_id TEXT,
    query TEXT NOT NULL,
    answer_quality INTEGER CHECK (answer_quality >= 1 AND answer_quality <= 5),
    relevance_score NUMERIC CHECK (relevance_score >= 0 AND relevance_score <= 1),
    response_time_ms INTEGER,
    reasons TEXT,
    top_citations JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    user_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 14. RAG Ingestion Logs (do schema original)
CREATE TABLE IF NOT EXISTS rag_ingestion_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES rag_documents(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'retrying')),
    operation TEXT NOT NULL,
    chunks_created INTEGER DEFAULT 0,
    chunks_updated INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_empresas_codigo ON empresas(codigo);
CREATE INDEX IF NOT EXISTS idx_personas_empresa_id ON personas(empresa_id);
CREATE INDEX IF NOT EXISTS idx_competencias_persona_id ON competencias(persona_id);
CREATE INDEX IF NOT EXISTS idx_workflows_persona_id ON workflows(persona_id);
CREATE INDEX IF NOT EXISTS idx_sync_logs_empresa_id ON sync_logs(empresa_id);
CREATE INDEX IF NOT EXISTS idx_rag_collections_code ON rag_collections(code);
CREATE INDEX IF NOT EXISTS idx_rag_documents_collection_id ON rag_documents(collection_id);
CREATE INDEX IF NOT EXISTS idx_rag_chunks_document_id ON rag_chunks(document_id);
CREATE INDEX IF NOT EXISTS idx_rag_knowledge_persona_id ON rag_knowledge(persona_id);

-- Função para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Função para calcular content_length
CREATE OR REPLACE FUNCTION update_content_length()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_TABLE_NAME = 'rag_documents' THEN
        NEW.content_length = length(NEW.content_raw);
    ELSIF TG_TABLE_NAME = 'rag_chunks' THEN
        NEW.content_length = length(NEW.content);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers (removendo se existirem)
DO $$
BEGIN
    DROP TRIGGER IF EXISTS update_empresas_updated_at ON empresas;
    DROP TRIGGER IF EXISTS update_personas_updated_at ON personas;
    DROP TRIGGER IF EXISTS update_workflows_updated_at ON workflows;
    DROP TRIGGER IF EXISTS update_rag_collections_updated_at ON rag_collections;
    DROP TRIGGER IF EXISTS update_rag_documents_updated_at ON rag_documents;
    DROP TRIGGER IF EXISTS update_rag_knowledge_updated_at ON rag_knowledge;
    DROP TRIGGER IF EXISTS update_rag_documents_content_length ON rag_documents;
    DROP TRIGGER IF EXISTS update_rag_chunks_content_length ON rag_chunks;
    
    CREATE TRIGGER update_empresas_updated_at 
        BEFORE UPDATE ON empresas 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    CREATE TRIGGER update_personas_updated_at 
        BEFORE UPDATE ON personas 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    CREATE TRIGGER update_workflows_updated_at 
        BEFORE UPDATE ON workflows 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    CREATE TRIGGER update_rag_collections_updated_at 
        BEFORE UPDATE ON rag_collections 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    CREATE TRIGGER update_rag_documents_updated_at 
        BEFORE UPDATE ON rag_documents 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    CREATE TRIGGER update_rag_knowledge_updated_at 
        BEFORE UPDATE ON rag_knowledge 
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        
    -- Triggers para content_length
    CREATE TRIGGER update_rag_documents_content_length
        BEFORE INSERT OR UPDATE ON rag_documents
        FOR EACH ROW EXECUTE FUNCTION update_content_length();
        
    CREATE TRIGGER update_rag_chunks_content_length
        BEFORE INSERT OR UPDATE ON rag_chunks
        FOR EACH ROW EXECUTE FUNCTION update_content_length();
END $$;

-- Dados iniciais
INSERT INTO empresas (
    codigo, nome, descricao, pais, idiomas, total_personas, status, scripts_status
) VALUES (
    'LIFEWAY',
    'LifewayUSA', 
    'Empresa de tecnologia e inovação nos Estados Unidos',
    'US',
    ARRAY['en', 'es'],
    20,
    'ativa',
    '{
        "biografias": true,
        "competencias": true,
        "tech_specs": false,
        "rag": false,
        "fluxos": false,
        "workflows": false
    }'::jsonb
) ON CONFLICT (codigo) DO UPDATE SET
    nome = EXCLUDED.nome,
    descricao = EXCLUDED.descricao,
    updated_at = NOW();

-- RLS
ALTER TABLE empresas ENABLE ROW LEVEL SECURITY;
ALTER TABLE personas ENABLE ROW LEVEL SECURITY;
ALTER TABLE competencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE sync_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE persona_collection_access ENABLE ROW LEVEL SECURITY;

-- Políticas (removendo se existirem)
DO $$
BEGIN
    DROP POLICY IF EXISTS "Allow all on empresas" ON empresas;
    DROP POLICY IF EXISTS "Allow all on personas" ON personas;
    DROP POLICY IF EXISTS "Allow all on competencias" ON competencias;
    DROP POLICY IF EXISTS "Allow all on workflows" ON workflows;
    DROP POLICY IF EXISTS "Allow all on sync_logs" ON sync_logs;
    DROP POLICY IF EXISTS "Allow all on rag_collections" ON rag_collections;
    DROP POLICY IF EXISTS "Allow all on rag_documents" ON rag_documents;
    DROP POLICY IF EXISTS "Allow all on rag_chunks" ON rag_chunks;
    DROP POLICY IF EXISTS "Allow all on rag_knowledge" ON rag_knowledge;
    DROP POLICY IF EXISTS "Allow all on persona_collection_access" ON persona_collection_access;
    
    CREATE POLICY "Allow all on empresas" ON empresas FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on personas" ON personas FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on competencias" ON competencias FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on workflows" ON workflows FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on sync_logs" ON sync_logs FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on rag_collections" ON rag_collections FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on rag_documents" ON rag_documents FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on rag_chunks" ON rag_chunks FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on rag_knowledge" ON rag_knowledge FOR ALL USING (true) WITH CHECK (true);
    CREATE POLICY "Allow all on persona_collection_access" ON persona_collection_access FOR ALL USING (true) WITH CHECK (true);
END $$;

-- Verificação final
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('empresas', 'personas', 'competencias', 'workflows', 'sync_logs', 
                       'rag_collections', 'rag_documents', 'rag_chunks', 'rag_knowledge', 
                       'persona_collection_access', 'rag_eval_sets', 'rag_eval_items', 
                       'rag_feedback', 'rag_ingestion_logs');
    
    RAISE NOTICE '✅ VCM Schema: % tabelas criadas com sucesso!', table_count;
    
    IF table_count = 14 THEN
        RAISE NOTICE '🎉 Sistema VCM COMPLETO - COMPATÍVEL com schema existente!';
        RAISE NOTICE '📋 Tabelas principais:';
        RAISE NOTICE '   • empresas (NOVA) - Master table para VCM Dashboard';
        RAISE NOTICE '   • personas - empresa_id como VARCHAR (compatível)';
        RAISE NOTICE '   • Todas tabelas RAG do schema original incluídas';
        RAISE NOTICE '   • Total: 14 tabelas vs schema original';
    END IF;
END $$;