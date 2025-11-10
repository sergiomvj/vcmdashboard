import './style.css'
import { useState, useEffect } from 'react'

interface Persona {
  nome_completo: string
  pais_origem: string
  role: string
  especializacao: string
  anos_experiencia: number
  idiomas: string[]
}

interface PersonasData {
  ceo: Persona
  executivos: { [key: string]: Persona }
  especialistas: { [key: string]: Persona }
  assistentes: { [key: string]: Persona }
}

function App() {
  const [personas, setPersonas] = useState<PersonasData | null>(null)
  const [status, setStatus] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  // Carrega dados reais das personas
  useEffect(() => {
    loadPersonasData()
  }, [])

  const loadPersonasData = async () => {
    try {
      // Carrega o arquivo personas_config.json real
      const response = await fetch('/AUTOMACAO/01_SETUP_E_CRIACAO/test_biografias_output/personas_config.json')
      if (!response.ok) {
        throw new Error('Arquivo personas_config.json não encontrado')
      }
      const data = await response.json()
      setPersonas(data)
    } catch (error) {
      setError('Não foi possível carregar os dados das personas')
      console.error('Erro ao carregar personas:', error)
    }
  }

  // Executa script Python real
  const executarScriptPython = async (scriptPath: string, scriptName: string) => {
    setLoading(true)
    setStatus(`Executando ${scriptName}...`)
    
    try {
      // Chamada para API Python que executa os scripts reais
      const response = await fetch('/api/execute-script', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script_path: scriptPath,
          working_directory: 'C:\\Users\\Sergio Castro\\Documents\\Projetos\\1NewTools\\vcm_vite_react\\AUTOMACAO'
        })
      })

      if (!response.ok) {
        throw new Error(`Erro ao executar ${scriptName}`)
      }

      const result = await response.json()
      setStatus(`✅ ${scriptName} executado com sucesso!`)
      return result
      
    } catch (error) {
      setStatus(`❌ Erro ao executar ${scriptName}: ${error instanceof Error ? error.message : 'Erro desconhecido'}`)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const processarPersonas = async () => {
    try {
      // Executa os 5 scripts do cascade real
      await executarScriptPython('02_PROCESSAMENTO_PERSONAS/01_generate_competencias.py', 'Geração de Competências')
      await executarScriptPython('02_PROCESSAMENTO_PERSONAS/02_generate_tech_specs.py', 'Especificações Técnicas')
      await executarScriptPython('02_PROCESSAMENTO_PERSONAS/03_generate_rag.py', 'População RAG Database')
      await executarScriptPython('02_PROCESSAMENTO_PERSONAS/04_generate_fluxos_analise.py', 'Análise de Fluxos')
      await executarScriptPython('02_PROCESSAMENTO_PERSONAS/05_generate_workflows_n8n.py', 'Workflows N8N')
      
      setStatus('✅ Cascade completo executado com sucesso!')
    } catch (error) {
      setStatus('❌ Erro no processamento do cascade')
    }
  }

  const criarNovaEmpresa = async () => {
    await executarScriptPython('01_SETUP_E_CRIACAO/05_auto_biografia_generator.py', 'Criação de Nova Empresa')
  }

  const testarSupabase = async () => {
    setLoading(true)
    setStatus('Testando conexão com Supabase...')
    
    try {
      const response = await fetch('/api/test-supabase', {
        method: 'POST'
      })
      
      if (!response.ok) {
        throw new Error('Erro na conexão com Supabase')
      }
      
      const result = await response.json()
      setStatus(`✅ Supabase: ${result.vcm_central ? 'VCM Central OK' : 'VCM Central ERRO'}, ${result.lifeway_rag ? 'LifewayUSA OK' : 'LifewayUSA ERRO'}`)
    } catch (error) {
      setStatus(`❌ Erro no teste Supabase: ${error instanceof Error ? error.message : 'Erro desconhecido'}`)
    } finally {
      setLoading(false)
    }
  }

  // Calcula estatísticas reais
  const totalPersonas = personas ? 
    1 + // CEO
    Object.keys(personas.executivos || {}).length +
    Object.keys(personas.especialistas || {}).length +
    Object.keys(personas.assistentes || {}).length : 0

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">VCM Dashboard</h1>
            </div>
            <div className="text-sm text-gray-500">
              Virtual Company Manager - Dados Reais
            </div>
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mx-4 mt-4">
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Dashboard VCM - Sistema Real</h2>
            <p className="text-gray-600">Dados reais do TechVision Solutions</p>
          </div>

          {/* Status Bar */}
          {status && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center">
                {loading && (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-3"></div>
                )}
                <span className={loading ? 'text-blue-600' : 'text-gray-900'}>{status}</span>
              </div>
            </div>
          )}

          {/* Dados Reais */}
          {personas && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">CEO Ativo</p>
                    <p className="text-lg font-bold text-gray-900">{personas.ceo.nome_completo}</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">{personas.ceo.pais_origem} - {personas.ceo.especializacao}</p>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Personas</p>
                    <p className="text-2xl font-bold text-gray-900">{totalPersonas}</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                  {Object.keys(personas.executivos || {}).length} Executivos, 
                  {Object.keys(personas.especialistas || {}).length} Especialistas, 
                  {Object.keys(personas.assistentes || {}).length} Assistentes
                </p>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Idiomas Total</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {Array.from(new Set(personas.ceo.idiomas)).length}
                    </p>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">CEO: {personas.ceo.idiomas.join(', ')}</p>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Experiência Média</p>
                    <p className="text-2xl font-bold text-gray-900">{personas.ceo.anos_experiencia}</p>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-2">anos de experiência (CEO)</p>
              </div>
            </div>
          )}

          {/* Scripts Reais */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Executar Scripts Python Reais</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button 
                onClick={criarNovaEmpresa}
                disabled={loading}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <h4 className="font-medium text-gray-900">Executar Gerador de Biografias</h4>
                <p className="text-sm text-gray-500">Script: 05_auto_biografia_generator.py</p>
              </button>
              
              <button 
                onClick={processarPersonas}
                disabled={loading}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <h4 className="font-medium text-gray-900">Cascade Completo</h4>
                <p className="text-sm text-gray-500">Scripts 1-5: Competências → N8N</p>
              </button>
              
              <button 
                onClick={testarSupabase}
                disabled={loading}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 text-left disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <h4 className="font-medium text-gray-900">Testar Supabase</h4>
                <p className="text-sm text-gray-500">Conexão VCM Central + LifewayUSA</p>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App