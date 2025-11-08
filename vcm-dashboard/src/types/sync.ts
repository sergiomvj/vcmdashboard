export type SyncStatus = 
  | 'synchronized'  // ✅ Em sync
  | 'pending'       // 🔄 Pendente
  | 'syncing'       // ⏳ Sincronizando
  | 'error'         // ❌ Erro
  | 'conflict'      // ⚠️ Conflito
  | 'never_synced'  // 🔘 Nunca sincronizado

export interface SyncLog {
  id: string
  empresa_id: string
  tipo_sync: 'manual' | 'automatico' | 'agendado'
  direcao: 'vcm_to_company' | 'company_to_vcm' | 'bidirectional'
  status: 'pending' | 'running' | 'success' | 'error' | 'partial' | 'cancelled'
  tabelas_afetadas: string[]
  registros_processados: number
  registros_sucesso: number
  registros_erro: number
  registros_conflito: number
  detalhes: Record<string, any>
  error_log?: string
  conflitos: any[]
  started_at: string
  finished_at?: string
  duration_seconds?: number
}

export interface SyncResult {
  success: boolean
  message: string
  syncLog: SyncLog
  conflicts?: any[]
}