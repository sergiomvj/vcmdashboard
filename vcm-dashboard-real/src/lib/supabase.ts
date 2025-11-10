import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Types based on existing database schema
export interface Empresa {
  id: string;
  codigo: string;
  nome: string;
  descricao: string;
  dominio?: string;
  industria: string;
  pais: string;
  idiomas: string[];
  total_personas: number;
  status: 'ativa' | 'inativa' | 'processando';
  scripts_status: {
    rag: boolean;
    fluxos: boolean;
    workflows: boolean;
    biografias: boolean;
    tech_specs: boolean;
    competencias: boolean;
  };
  created_at: string;
  updated_at: string;
  // New columns added for CRUD
  ceo_gender?: 'masculino' | 'feminino';
  industry?: string;
  executives_male?: number;
  executives_female?: number;
  assistants_male?: number;
  assistants_female?: number;
  specialists_male?: number;
  specialists_female?: number;
  nationalities?: { tipo: string; percentual: number }[];
}

export interface SystemConfiguration {
  id: string;
  key: string;
  value: string;
  category: 'api' | 'system' | 'ui' | 'sync';
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Persona {
  id: string;
  persona_code: string;
  full_name: string;
  role: string;
  specialty?: string;
  department?: string;
  email: string;
  whatsapp: string;
  empresa_id: string;
  biografia_completa?: string;
  personalidade: Record<string, unknown>;
  experiencia_anos: number;
  ia_config: Record<string, unknown>;
  temperatura_ia: number;
  max_tokens: number;
  system_prompt?: string;
  status: 'active' | 'inactive' | 'archived';
  created_at: string;
  updated_at: string;
  last_sync: string;
}

// Database table names (using existing schema)
export const TABLES = {
  EMPRESAS: 'empresas',
  CONFIGURATIONS: 'system_configurations',
  PERSONAS: 'personas',
} as const;