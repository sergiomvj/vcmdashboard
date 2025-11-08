-- ===================================================
-- VCM Dashboard - Schema Completo para Supabase
-- Virtual Company Manager - Sistema de Automação Empresarial
-- ===================================================
--
-- PROPÓSITO:
-- Este schema implementa o sistema VCM (Virtual Company Manager) que automatiza
-- a criação e gerenciamento de empresas virtuais com 20 personas cada, incluindo
-- sistema RAG com embeddings, workflows N8N e sincronização de dados.
--
-- ARQUITETURA:
-- - Dual Database Strategy: VCM Central + RAG databases individuais
-- - 5-Script Cascade: biografia → competências → tech specs → RAG → workflows
-- - 20 Personas Padronizadas: executivos(5) + especialistas(10) + assistentes(5)
-- - Sistema RAG com embeddings OpenAI para knowledge base
-- - Integração N8N para automação de processos empresariais
--
-- DEPENDÊNCIAS:
-- - PostgreSQL 14+ com extensões: uuid-ossp, vector (pgvector)
-- - Supabase com RLS habilitado
-- - OpenAI API para embeddings (modelo text-embedding-ada-002)
-- - Python scripts em AUTOMACAO/ para processamento em cascata
--
-- VERSÃO: 2.0
-- ÚLTIMA ATUALIZAÇÃO: Nov 2025
-- ===================================================

-- ===================================================
-- Extensões Necessárias
-- ===================================================

-- Extensão para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extensão para embeddings vetoriais (CRÍTICO para RAG)
-- NOTA: Se falhar, execute manualmente no SQL Editor do Supabase
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Tabela de Empresas (Master Table - VCM Central)
-- Gerencia empresas virtuais com status de scripts em cascata
CREATE TABLE IF NOT EXISTS empresas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo VARCHAR(50) UNIQUE NOT NULL,              -- Código único (ex: LIFEWAY, TECHCORP)
    nome VARCHAR(255) NOT NULL,                      -- Nome da empresa virtual
    descricao TEXT,                                  -- Descrição do negócio
    pais VARCHAR(10) NOT NULL DEFAULT 'BR',          -- País de operação (ISO code)
    idiomas TEXT[] NOT NULL DEFAULT ARRAY['pt'],     -- Idiomas suportados pelas personas
    total_personas INTEGER NOT NULL DEFAULT 20,      -- Sempre 20 personas por empresa
    status VARCHAR(20) NOT NULL DEFAULT 'ativa' CHECK (status IN ('ativa', 'inativa', 'processando')),
    scripts_status JSONB NOT NULL DEFAULT '{         -- Status da cascata de scripts 1-5
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

-- 2. Tabela Personas (20 por empresa - Estrutura Padronizada)
-- Categorias: executivos(5) + especialistas(10) + assistentes(5)
-- Geradas pelos scripts Python em cascata sequencial
CREATE TABLE IF NOT EXISTS personas (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    persona_code VARCHAR NOT NULL UNIQUE,            -- Código único: EMPRESA_CATEGORIA_NOME
    full_name VARCHAR NOT NULL,                      -- Nome completo da persona
    role VARCHAR NOT NULL,                           -- Cargo/função na empresa
    specialty VARCHAR,                               -- Especialidade técnica
    department VARCHAR,                              -- Departamento/área
    email VARCHAR NOT NULL UNIQUE,                   -- Email corporativo único
    whatsapp VARCHAR NOT NULL,                       -- WhatsApp para contato
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    biografia_completa TEXT,                         -- Biografia gerada pelo Script 1
    personalidade JSONB DEFAULT '{}'::jsonb,         -- Traços de personalidade
    experiencia_anos INTEGER DEFAULT 0,              -- Anos de experiência
    ia_config JSONB DEFAULT '{}'::jsonb,             -- Configuração da IA
    temperatura_ia NUMERIC DEFAULT 0.7,              -- Temperatura para respostas
    max_tokens INTEGER DEFAULT 2000,                 -- Limite de tokens
    system_prompt TEXT,                              -- Prompt do sistema personalizado
    status VARCHAR DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(), -- Última sincronização com RAG DB
    CONSTRAINT personas_pkey PRIMARY KEY (id)
);

-- 3. Tabela Competencias (Script 2 - Análise de Skills)
-- Extraídas automaticamente das biografias usando IA
CREATE TABLE IF NOT EXISTS competencias (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('principal', 'tecnica', 'soft_skill')),
    nome VARCHAR NOT NULL,                           -- Nome da competência
    descricao TEXT,                                  -- Descrição detalhada
    nivel VARCHAR DEFAULT 'avancado' CHECK (nivel IN ('basico', 'intermediario', 'avancado', 'expert')),
    categoria VARCHAR,                               -- Categoria da skill (programação, gestão, etc)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT competencias_pkey PRIMARY KEY (id)
);

-- 4. Tabela RAG Collections
CREATE TABLE IF NOT EXISTS rag_collections (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    visibility TEXT NOT NULL DEFAULT 'public' CHECK (visibility IN ('public', 'internal', 'restricted')),
    tags TEXT[] DEFAULT ARRAY[]::text[],
    metadata JSONB DEFAULT '{}'::jsonb,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT rag_collections_pkey PRIMARY KEY (id)
);

-- 5. Tabela RAG Documents
CREATE TABLE IF NOT EXISTS rag_documents (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    collection_id UUID NOT NULL REFERENCES rag_collections(id) ON DELETE CASCADE,
    external_id TEXT NOT NULL,
    title TEXT NOT NULL,
    content_raw TEXT,
    content_length INTEGER GENERATED ALWAYS AS (length(content_raw)) STORED,
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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT rag_documents_pkey PRIMARY KEY (id)
);

-- 6. Tabela RAG Chunks (Embeddings OpenAI - text-embedding-ada-002)
-- Chunks dos documentos com vetores para busca semântica
-- NOTA: Se a extensão vector falhar, remova temporariamente a coluna embedding
CREATE TABLE IF NOT EXISTS rag_chunks (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,                    -- Índice sequencial do chunk
    content TEXT NOT NULL,                          -- Conteúdo do chunk
    content_length INTEGER GENERATED ALWAYS AS (length(content)) STORED,
    tokens INTEGER,                                 -- Contagem de tokens OpenAI
    metadata JSONB DEFAULT '{}'::jsonb,             -- Metadados do chunk
    start_char INTEGER,                             -- Posição inicial no documento
    end_char INTEGER,                               -- Posição final no documento
    overlap_prev INTEGER DEFAULT 0,                 -- Sobreposição com chunk anterior
    overlap_next INTEGER DEFAULT 0,                 -- Sobreposição com próximo chunk
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT rag_chunks_pkey PRIMARY KEY (id)
);

-- Adicionar coluna embedding apenas se extensão vector estiver disponível
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        ALTER TABLE rag_chunks ADD COLUMN IF NOT EXISTS embedding VECTOR(1536);
        RAISE NOTICE '✅ Coluna embedding adicionada com sucesso!';
    ELSE
        RAISE NOTICE '⚠️ Extensão vector não encontrada - coluna embedding não criada';
    END IF;
END $$;

-- 7. Tabela Workflows (Script 5 - Automação N8N)
-- Workflows gerados automaticamente para cada persona
CREATE TABLE IF NOT EXISTS workflows (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    nome VARCHAR NOT NULL,                           -- Nome do workflow
    descricao TEXT,                                  -- Descrição do processo
    tipo VARCHAR NOT NULL CHECK (tipo IN ('tarefa', 'fluxo', 'responsabilidade')),
    prioridade VARCHAR DEFAULT 'media' CHECK (prioridade IN ('baixa', 'media', 'alta', 'critica')),
    config JSONB DEFAULT '{}'::jsonb,                -- Configuração do N8N
    triggers JSONB DEFAULT '[]'::jsonb,              -- Triggers do workflow
    actions JSONB DEFAULT '[]'::jsonb,               -- Ações do workflow
    ativo BOOLEAN DEFAULT TRUE,                      -- Se o workflow está ativo
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT workflows_pkey PRIMARY KEY (id)
);

-- 8. Tabela RAG Knowledge
CREATE TABLE IF NOT EXISTS rag_knowledge (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT rag_knowledge_pkey PRIMARY KEY (id)
);

-- Adicionar coluna embedding apenas se extensão vector estiver disponível
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        ALTER TABLE rag_knowledge ADD COLUMN IF NOT EXISTS embedding VECTOR(1536);
        RAISE NOTICE '✅ Coluna embedding adicionada à rag_knowledge!';
    ELSE
        RAISE NOTICE '⚠️ Coluna embedding não criada em rag_knowledge - extensão vector não encontrada';
    END IF;
END $$;

-- 9. Tabela Sync Logs (Monitoramento de Sincronização)
-- Logs de sincronização entre VCM Central e RAG databases individuais
CREATE TABLE IF NOT EXISTS sync_logs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    tipo_sync VARCHAR NOT NULL,                      -- Tipo: biografia, competencia, rag, workflow
    status VARCHAR NOT NULL CHECK (status IN ('success', 'error', 'partial')),
    registros_processados INTEGER DEFAULT 0,         -- Total de registros processados
    registros_sucesso INTEGER DEFAULT 0,             -- Registros sincronizados com sucesso
    registros_erro INTEGER DEFAULT 0,                -- Registros com erro
    detalhes JSONB DEFAULT '{}'::jsonb,              -- Detalhes da sincronização
    error_log TEXT,                                  -- Log de erros detalhado
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,            -- Timestamp de finalização
    duration_seconds INTEGER,                        -- Duração em segundos
    CONSTRAINT sync_logs_pkey PRIMARY KEY (id)
);

-- 10. Tabela Persona Collection Access
CREATE TABLE IF NOT EXISTS persona_collection_access (
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    collection_id UUID NOT NULL REFERENCES rag_collections(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'reader' CHECK (role IN ('reader', 'editor', 'owner')),
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    granted_by UUID,
    CONSTRAINT persona_collection_access_pkey PRIMARY KEY (persona_id, collection_id)
);

-- ===================================================
-- Índices para Performance Otimizada
-- Criados com base nos padrões de consulta do VCM
-- ===================================================

-- Empresas - Consultas por código e status
CREATE INDEX IF NOT EXISTS idx_empresas_codigo ON empresas(codigo);
CREATE INDEX IF NOT EXISTS idx_empresas_status ON empresas(status);
CREATE INDEX IF NOT EXISTS idx_empresas_created_at ON empresas(created_at);

-- Personas - Consultas por empresa e filtros
CREATE INDEX IF NOT EXISTS idx_personas_empresa_id ON personas(empresa_id);
CREATE INDEX IF NOT EXISTS idx_personas_persona_code ON personas(persona_code);
CREATE INDEX IF NOT EXISTS idx_personas_email ON personas(email);
CREATE INDEX IF NOT EXISTS idx_personas_status ON personas(status);

-- Competencias - Busca por persona e tipo
CREATE INDEX IF NOT EXISTS idx_competencias_persona_id ON competencias(persona_id);
CREATE INDEX IF NOT EXISTS idx_competencias_tipo ON competencias(tipo);

-- RAG Collections - Busca por código e visibilidade
CREATE INDEX IF NOT EXISTS idx_rag_collections_code ON rag_collections(code);
CREATE INDEX IF NOT EXISTS idx_rag_collections_visibility ON rag_collections(visibility);

-- RAG Documents - Consultas por collection e idioma
CREATE INDEX IF NOT EXISTS idx_rag_documents_collection_id ON rag_documents(collection_id);
CREATE INDEX IF NOT EXISTS idx_rag_documents_external_id ON rag_documents(external_id);
CREATE INDEX IF NOT EXISTS idx_rag_documents_language ON rag_documents(language);

-- RAG Chunks - Busca semântica com embeddings (CRÍTICO para performance)
CREATE INDEX IF NOT EXISTS idx_rag_chunks_document_id ON rag_chunks(document_id);

-- Índice vetorial apenas se extensão vector estiver disponível
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') AND 
       EXISTS (SELECT 1 FROM information_schema.columns 
               WHERE table_name = 'rag_chunks' AND column_name = 'embedding') THEN
        CREATE INDEX IF NOT EXISTS idx_rag_chunks_embedding 
        ON rag_chunks USING ivfflat (embedding vector_cosine_ops);
        RAISE NOTICE '✅ Índice vetorial criado para rag_chunks.embedding';
    ELSE
        RAISE NOTICE '⚠️ Índice vetorial não criado - extensão vector ou coluna embedding não disponível';
    END IF;
END $$;

-- Workflows - Consultas por persona e status
CREATE INDEX IF NOT EXISTS idx_workflows_persona_id ON workflows(persona_id);
CREATE INDEX IF NOT EXISTS idx_workflows_tipo ON workflows(tipo);
CREATE INDEX IF NOT EXISTS idx_workflows_ativo ON workflows(ativo);

-- Sync Logs - Monitoramento por empresa e status
CREATE INDEX IF NOT EXISTS idx_sync_logs_empresa_id ON sync_logs(empresa_id);
CREATE INDEX IF NOT EXISTS idx_sync_logs_status ON sync_logs(status);
CREATE INDEX IF NOT EXISTS idx_sync_logs_started_at ON sync_logs(started_at);

-- ===================================================
-- Triggers para Updated_at
-- ===================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers (com DROP IF EXISTS para evitar conflitos)
DROP TRIGGER IF EXISTS update_empresas_updated_at ON empresas;
CREATE TRIGGER update_empresas_updated_at 
    BEFORE UPDATE ON empresas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_personas_updated_at ON personas;
CREATE TRIGGER update_personas_updated_at 
    BEFORE UPDATE ON personas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_rag_collections_updated_at ON rag_collections;
CREATE TRIGGER update_rag_collections_updated_at 
    BEFORE UPDATE ON rag_collections 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_rag_documents_updated_at ON rag_documents;
CREATE TRIGGER update_rag_documents_updated_at 
    BEFORE UPDATE ON rag_documents 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_workflows_updated_at ON workflows;
CREATE TRIGGER update_workflows_updated_at 
    BEFORE UPDATE ON workflows 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_rag_knowledge_updated_at ON rag_knowledge;
CREATE TRIGGER update_rag_knowledge_updated_at 
    BEFORE UPDATE ON rag_knowledge 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ===================================================
-- Dados de Exemplo e Configuração Inicial
-- ===================================================

-- Inserir LifewayUSA como empresa de referência
-- Empresa real já processada com Scripts 1-2 completos
INSERT INTO empresas (
    codigo, nome, descricao, pais, idiomas, total_personas, status, scripts_status
) VALUES (
    'LIFEWAY',
    'LifewayUSA', 
    'Empresa de tecnologia e inovação nos Estados Unidos - Referência VCM',
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

-- Verificar se extensão pgvector está disponível
-- INSTRUÇÕES para Supabase:
-- 1. Vá em Database > Extensions
-- 2. Procure por "vector" 
-- 3. Clique em Enable
-- 4. Execute novamente este script para adicionar colunas embedding

-- ===================================================
-- Row Level Security (RLS)
-- ===================================================

-- Ativar RLS em todas as tabelas
ALTER TABLE empresas ENABLE ROW LEVEL SECURITY;
ALTER TABLE personas ENABLE ROW LEVEL SECURITY;
ALTER TABLE competencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_knowledge ENABLE ROW LEVEL SECURITY;
ALTER TABLE sync_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE persona_collection_access ENABLE ROW LEVEL SECURITY;

-- Políticas permissivas para desenvolvimento (ajustar em produção)
DROP POLICY IF EXISTS "Allow all on empresas" ON empresas;
CREATE POLICY "Allow all on empresas" ON empresas FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on personas" ON personas;
CREATE POLICY "Allow all on personas" ON personas FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on competencias" ON competencias;
CREATE POLICY "Allow all on competencias" ON competencias FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on rag_collections" ON rag_collections;
CREATE POLICY "Allow all on rag_collections" ON rag_collections FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on rag_documents" ON rag_documents;
CREATE POLICY "Allow all on rag_documents" ON rag_documents FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on rag_chunks" ON rag_chunks;
CREATE POLICY "Allow all on rag_chunks" ON rag_chunks FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on workflows" ON workflows;
CREATE POLICY "Allow all on workflows" ON workflows FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on rag_knowledge" ON rag_knowledge;
CREATE POLICY "Allow all on rag_knowledge" ON rag_knowledge FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on sync_logs" ON sync_logs;
CREATE POLICY "Allow all on sync_logs" ON sync_logs FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all on persona_collection_access" ON persona_collection_access;
CREATE POLICY "Allow all on persona_collection_access" ON persona_collection_access FOR ALL USING (true) WITH CHECK (true);

-- ===================================================
-- Verificações Finais e Validação do Schema
-- ===================================================

DO $$
DECLARE
    table_count INTEGER;
    extension_exists BOOLEAN;
BEGIN
    -- Verificar se todas as 10 tabelas foram criadas
    SELECT COUNT(*) INTO table_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('empresas', 'personas', 'competencias', 'rag_collections', 
                       'rag_documents', 'rag_chunks', 'workflows', 'rag_knowledge', 
                       'sync_logs', 'persona_collection_access');
    
    -- Verificar se extensão vector está disponível
    SELECT EXISTS(
        SELECT 1 FROM pg_extension WHERE extname = 'vector'
    ) INTO extension_exists;
    
    RAISE NOTICE '✅ VCM Schema Complete: % tables created successfully!', table_count;
    
    IF table_count = 10 THEN
        RAISE NOTICE '🎉 All VCM tables are ready for use!';
        
        IF extension_exists THEN
            RAISE NOTICE '🔍 pgvector extension detected - RAG embeddings ready!';
        ELSE
            RAISE NOTICE '⚠️ pgvector extension not found - run: CREATE EXTENSION IF NOT EXISTS vector;';
        END IF;
        
        RAISE NOTICE '📋 Next steps:';
        RAISE NOTICE '   1. Run Python scripts in AUTOMACAO/02_PROCESSAMENTO_PERSONAS/';
        RAISE NOTICE '   2. Execute scripts 1-5 in sequence for each company';
        RAISE NOTICE '   3. Monitor sync_logs for processing status';
        RAISE NOTICE '   4. Access VCM Dashboard for management interface';
        
    ELSE
        RAISE NOTICE '⚠️ Expected 10 tables, found %. Please check for errors.', table_count;
    END IF;
    
    RAISE NOTICE '';
    RAISE NOTICE '🏗️ VCM System Architecture Ready:';
    RAISE NOTICE '   • Dual Database Strategy: VCM Central + Individual RAG DBs';
    RAISE NOTICE '   • 5-Script Cascade: biografia → competencias → tech → rag → workflows';
    RAISE NOTICE '   • 20 Standardized Personas per Company';
    RAISE NOTICE '   • OpenAI Embeddings Integration';
    RAISE NOTICE '   • N8N Workflow Automation';
    RAISE NOTICE '   • Real-time Dashboard Interface';
    
END $$;