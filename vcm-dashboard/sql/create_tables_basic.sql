-- ===================================================
-- VCM Dashboard - Schema BÁSICO (SEM EMBEDDINGS)
-- Para usar quando extensão vector não estiver disponível
-- ===================================================

-- Extensão básica para UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabela de Empresas
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

-- 2. Tabela Personas
CREATE TABLE IF NOT EXISTS personas (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    persona_code VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    specialty VARCHAR,
    department VARCHAR,
    email VARCHAR NOT NULL UNIQUE,
    whatsapp VARCHAR NOT NULL,
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
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
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT personas_pkey PRIMARY KEY (id)
);

-- 3. Tabela Competencias
CREATE TABLE IF NOT EXISTS competencias (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    persona_id UUID NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    tipo VARCHAR NOT NULL CHECK (tipo IN ('principal', 'tecnica', 'soft_skill')),
    nome VARCHAR NOT NULL,
    descricao TEXT,
    nivel VARCHAR DEFAULT 'avancado' CHECK (nivel IN ('basico', 'intermediario', 'avancado', 'expert')),
    categoria VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT competencias_pkey PRIMARY KEY (id)
);

-- 4. Tabela Workflows
CREATE TABLE IF NOT EXISTS workflows (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT workflows_pkey PRIMARY KEY (id)
);

-- 5. Tabela Sync Logs
CREATE TABLE IF NOT EXISTS sync_logs (
    id UUID NOT NULL DEFAULT gen_random_uuid(),
    empresa_id UUID NOT NULL REFERENCES empresas(id) ON DELETE CASCADE,
    tipo_sync VARCHAR NOT NULL,
    status VARCHAR NOT NULL CHECK (status IN ('success', 'error', 'partial')),
    registros_processados INTEGER DEFAULT 0,
    registros_sucesso INTEGER DEFAULT 0,
    registros_erro INTEGER DEFAULT 0,
    detalhes JSONB DEFAULT '{}'::jsonb,
    error_log TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    CONSTRAINT sync_logs_pkey PRIMARY KEY (id)
);

-- Índices básicos
CREATE INDEX IF NOT EXISTS idx_empresas_codigo ON empresas(codigo);
CREATE INDEX IF NOT EXISTS idx_personas_empresa_id ON personas(empresa_id);
CREATE INDEX IF NOT EXISTS idx_competencias_persona_id ON competencias(persona_id);
CREATE INDEX IF NOT EXISTS idx_workflows_persona_id ON workflows(persona_id);
CREATE INDEX IF NOT EXISTS idx_sync_logs_empresa_id ON sync_logs(empresa_id);

-- Triggers para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_empresas_updated_at 
    BEFORE UPDATE ON empresas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_personas_updated_at 
    BEFORE UPDATE ON personas 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at 
    BEFORE UPDATE ON workflows 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Dados de exemplo
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

CREATE POLICY "Allow all on empresas" ON empresas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on personas" ON personas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on competencias" ON competencias FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on workflows" ON workflows FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all on sync_logs" ON sync_logs FOR ALL USING (true) WITH CHECK (true);

-- Verificação final
DO $$
DECLARE
    table_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO table_count 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name IN ('empresas', 'personas', 'competencias', 'workflows', 'sync_logs');
    
    RAISE NOTICE '✅ VCM Schema Básico: % tabelas criadas!', table_count;
    
    IF table_count = 5 THEN
        RAISE NOTICE '🎉 Schema básico pronto! Para RAG completo, habilite extensão vector.';
    END IF;
END $$;