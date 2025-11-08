import { useState } from 'react'
import { type Empresa } from '../types/empresa'

interface ScriptExecutorProps {
  empresa: Empresa
  onClose: () => void
}

interface ScriptStatus {
  biografia: 'idle' | 'running' | 'success' | 'error'
  competencias: 'idle' | 'running' | 'success' | 'error'
  tech_specs: 'idle' | 'running' | 'success' | 'error'
  rag: 'idle' | 'running' | 'success' | 'error'
  fluxos: 'idle' | 'running' | 'success' | 'error'
  workflows: 'idle' | 'running' | 'success' | 'error'
}

interface ScriptOutput {
  script: string
  output: string
  error?: string
  timestamp: string
}

const ScriptExecutor: React.FC<ScriptExecutorProps> = ({ empresa, onClose }) => {
  const [scriptStatus, setScriptStatus] = useState<ScriptStatus>({
    biografia: 'idle',
    competencias: 'idle',
    tech_specs: 'idle',
    rag: 'idle',
    fluxos: 'idle',
    workflows: 'idle'
  })
  
  const [outputs, setOutputs] = useState<ScriptOutput[]>([])
  const [isRunningCascade, setIsRunningCascade] = useState(false)

  const scripts = [
    { key: 'biografia', name: 'Gerar Biografias', description: 'Cria biografias das 20 personas' },
    { key: 'competencias', name: 'Competências', description: 'Analisa competências técnicas e comportamentais' },
    { key: 'tech_specs', name: 'Especificações Técnicas', description: 'Define tecnologias e ferramentas' },
    { key: 'rag', name: 'RAG Database', description: 'Popula banco de conhecimento RAG' },
    { key: 'fluxos', name: 'Análise de Fluxos', description: 'Mapeia processos de negócio' },
    { key: 'workflows', name: 'Workflows N8N', description: 'Gera automações N8N' }
  ]

  const addOutput = (script: string, output: string, error?: string) => {
    const newOutput: ScriptOutput = {
      script,
      output,
      error,
      timestamp: new Date().toLocaleTimeString()
    }
    setOutputs(prev => [newOutput, ...prev])
  }

  const executeScript = async (scriptKey: string) => {
    setScriptStatus(prev => ({ ...prev, [scriptKey]: 'running' }))
    
    try {
      // Simular chamada para API
      addOutput(scriptKey, `Iniciando execução do script ${scriptKey}...`)
      
      // TODO: Substituir por chamada real para API
      await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 3000))
      
      // Simular sucesso/erro
      const success = Math.random() > 0.3
      
      if (success) {
        setScriptStatus(prev => ({ ...prev, [scriptKey]: 'success' }))
        addOutput(scriptKey, `Script ${scriptKey} executado com sucesso! ✅`)
      } else {
        setScriptStatus(prev => ({ ...prev, [scriptKey]: 'error' }))
        addOutput(scriptKey, `Erro na execução do script ${scriptKey}`, 'Erro simulado para demonstração')
      }
      
    } catch (error) {
      setScriptStatus(prev => ({ ...prev, [scriptKey]: 'error' }))
      addOutput(scriptKey, `Erro inesperado no script ${scriptKey}`, (error as Error).message)
    }
  }

  const executeCascade = async () => {
    setIsRunningCascade(true)
    addOutput('cascade', 'Iniciando execução em cascata de todos os scripts...')
    
    for (const script of scripts) {
      if (scriptStatus[script.key as keyof ScriptStatus] === 'success') {
        addOutput(script.key, `Script ${script.key} já executado, pulando...`)
        continue
      }
      
      await executeScript(script.key)
      
      // Se erro, para a cascata
      if (scriptStatus[script.key as keyof ScriptStatus] === 'error') {
        addOutput('cascade', `Cascata interrompida devido ao erro no script ${script.key}`)
        break
      }
      
      // Pequena pausa entre scripts
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    
    setIsRunningCascade(false)
    addOutput('cascade', 'Cascata de scripts finalizada!')
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return '⏳'
      case 'success': return '✅'
      case 'error': return '❌'
      default: return '⚪'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      case 'success': return 'bg-green-100 text-green-800 border-green-300'
      case 'error': return 'bg-red-100 text-red-800 border-red-300'
      default: return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-5xl max-h-[90vh] overflow-hidden flex flex-col">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold">Executar Scripts - {empresa.nome}</h2>
            <p className="text-gray-600">Código: {empresa.codigo}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ✕
          </button>
        </div>

        <div className="flex flex-1 space-x-6 overflow-hidden">
          
          {/* Painel de Scripts */}
          <div className="w-1/2 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">Scripts Disponíveis</h3>
              <button
                onClick={executeCascade}
                disabled={isRunningCascade}
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {isRunningCascade ? 'Executando...' : 'Executar Cascata'}
              </button>
            </div>
            
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {scripts.map((script, index) => (
                <div
                  key={script.key}
                  className={`border rounded-lg p-4 ${getStatusColor(scriptStatus[script.key as keyof ScriptStatus])}`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">
                        {getStatusIcon(scriptStatus[script.key as keyof ScriptStatus])}
                      </span>
                      <h4 className="font-medium">{index + 1}. {script.name}</h4>
                    </div>
                    <button
                      onClick={() => executeScript(script.key)}
                      disabled={scriptStatus[script.key as keyof ScriptStatus] === 'running' || isRunningCascade}
                      className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700 disabled:opacity-50"
                    >
                      Executar
                    </button>
                  </div>
                  <p className="text-sm opacity-80">{script.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Painel de Output */}
          <div className="w-1/2 flex flex-col">
            <h3 className="text-lg font-semibold mb-4">Log de Execução</h3>
            <div className="flex-1 bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-sm overflow-y-auto">
              {outputs.length === 0 ? (
                <div className="text-gray-500">
                  Aguardando execução de scripts...
                </div>
              ) : (
                outputs.map((output, index) => (
                  <div key={index} className="mb-3">
                    <div className="text-yellow-400 text-xs">
                      [{output.timestamp}] {output.script}
                    </div>
                    <div className="ml-2">
                      {output.output}
                    </div>
                    {output.error && (
                      <div className="ml-2 text-red-400">
                        Error: {output.error}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
            
            <button
              onClick={() => setOutputs([])}
              className="mt-2 bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700"
            >
              Limpar Log
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-end space-x-2 mt-6 pt-4 border-t">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  )
}

export default ScriptExecutor