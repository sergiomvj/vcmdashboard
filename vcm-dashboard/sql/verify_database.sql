-- ===================================================
-- Script de Verificação do Banco VCM
-- ===================================================

-- 1. Verificar se a tabela empresas existe
SELECT 
    table_name,
    table_type,
    is_insertable_into
FROM information_schema.tables 
WHERE table_name = 'empresas';

-- 2. Verificar estrutura da tabela
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'empresas'
ORDER BY ordinal_position;

-- 3. Verificar índices
SELECT 
    indexname,
    indexdef
FROM pg_indexes 
WHERE tablename = 'empresas';

-- 4. Verificar RLS (Row Level Security)
SELECT 
    tablename,
    rowsecurity
FROM pg_tables 
WHERE tablename = 'empresas';

-- 5. Verificar policies
SELECT 
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies 
WHERE tablename = 'empresas';

-- 6. Verificar dados existentes
SELECT 
    id,
    codigo,
    nome,
    status,
    created_at
FROM empresas
ORDER BY created_at DESC;

-- 7. Teste de inserção (será revertido)
BEGIN;
INSERT INTO empresas (codigo, nome, pais) 
VALUES ('TEST', 'Empresa Teste', 'BR');
SELECT 'Teste de inserção: OK' as status;
ROLLBACK;