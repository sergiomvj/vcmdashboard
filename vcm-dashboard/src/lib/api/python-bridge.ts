/**
 * Python Scripts Bridge API
 * 
 * Esta API faz a ponte entre o dashboard React e os scripts Python existentes
 * Permite executar os scripts de automação diretamente do frontend
 */

export interface PythonScriptResult {
  success: boolean
  message: string
  data?: any
  error?: string
  output?: string
}

export interface BiografiaGenerationParams {
  empresa_codigo: string
  empresa_nome: string
  total_personas?: number
  idiomas?: string[]
  pais?: string
}

export interface CascadeScriptParams {
  empresa_codigo: string
  script_number: 1 | 2 | 3 | 4 | 5
  force_regenerate?: boolean
}

class PythonBridge {
  private baseUrl: string
  
  constructor() {
    this.baseUrl = import.meta.env.VITE_PYTHON_API_URL || 'http://localhost:8000'
  }

  /**
   * Executa o script de geração de biografias (05_auto_biografia_generator.py)
   */
  async generateBiografias(params: BiografiaGenerationParams): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/generate-biografias`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(params)
      })
      
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro na conexão',
        error: `Erro ao conectar com API Python: ${error}`
      }
    }
  }

  /**
   * Executa um script da cascata (Scripts 1-5)
   */
  async executeCascadeScript(params: CascadeScriptParams): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/cascade-script/${params.script_number}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          empresa_codigo: params.empresa_codigo,
          force_regenerate: params.force_regenerate || false
        })
      })
      
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro na execução',
        error: `Erro ao executar script ${params.script_number}: ${error}`
      }
    }
  }

  /**
   * Executa toda a cascata de scripts (1-5) em sequência
   */
  async executeFullCascade(empresaCodigo: string): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/full-cascade`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ empresa_codigo: empresaCodigo })
      })
      
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro na cascata',
        error: `Erro ao executar cascata completa: ${error}`
      }
    }
  }

  /**
   * Verifica o status dos scripts Python
   */
  async getScriptStatus(empresaCodigo: string): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/script-status/${empresaCodigo}`)
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro no status',
        error: `Erro ao verificar status: ${error}`
      }
    }
  }

  /**
   * Lista os outputs gerados pelos scripts
   */
  async listScriptOutputs(empresaCodigo: string): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/script-outputs/${empresaCodigo}`)
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro nos outputs',
        error: `Erro ao listar outputs: ${error}`
      }
    }
  }

  /**
   * Sincroniza dados gerados pelos scripts Python com Supabase
   */
  async syncPythonToSupabase(empresaCodigo: string): Promise<PythonScriptResult> {
    try {
      const response = await fetch(`${this.baseUrl}/sync-to-supabase`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ empresa_codigo: empresaCodigo })
      })
      
      return await response.json()
    } catch (error) {
      return {
        success: false,
        message: 'Erro na sincronização',
        error: `Erro ao sincronizar com Supabase: ${error}`
      }
    }
  }
}

export const pythonBridge = new PythonBridge()

// Hooks para usar no React
export const usePythonBridge = () => {
  return {
    generateBiografias: pythonBridge.generateBiografias.bind(pythonBridge),
    executeCascadeScript: pythonBridge.executeCascadeScript.bind(pythonBridge),
    executeFullCascade: pythonBridge.executeFullCascade.bind(pythonBridge),
    getScriptStatus: pythonBridge.getScriptStatus.bind(pythonBridge),
    listScriptOutputs: pythonBridge.listScriptOutputs.bind(pythonBridge),
    syncPythonToSupabase: pythonBridge.syncPythonToSupabase.bind(pythonBridge)
  }
}