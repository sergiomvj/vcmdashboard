import { useState, useEffect } from 'react'
import { type Empresa } from '../types/empresa'
import { useEmpresaStore } from '../store/empresaStore'
import EmpresaForm from './EmpresaForm'
import ScriptExecutor from './ScriptExecutor'
import EmpresaDetails from './EmpresaDetails'
import { setupDatabase, testConnection } from '../utils/database-setup'
import { testSupabaseConnection } from '../lib/supabaseTest'

const EmpresaList: React.FC = () => {
  const { 
    empresas, 
    loading, 
    error, 
    fetchEmpresas, 
    deleteEmpresaAPI, 
    setSelectedEmpresa 
  } = useEmpresaStore()
  
  const [showForm, setShowForm] = useState(false)
  const [editingEmpresa, setEditingEmpresa] = useState<Empresa | null>(null)
  const [showScriptExecutor, setShowScriptExecutor] = useState(false)
  const [executingEmpresa, setExecutingEmpresa] = useState<Empresa | null>(null)
  const [showDetails, setShowDetails] = useState(false)
  const [detailsEmpresa, setDetailsEmpresa] = useState<Empresa | null>(null)
  const [dbStatus, setDbStatus] = useState<string>('')

  useEffect(() => {
    fetchEmpresas()
  }, [fetchEmpresas])

  const handleEdit = (empresa: Empresa) => {
    setEditingEmpresa(empresa)
    setShowForm(true)
  }

  const handleExecuteScripts = (empresa: Empresa) => {
    setExecutingEmpresa(empresa)
    setShowScriptExecutor(true)
  }

  const handleViewDetails = (empresa: Empresa) => {
    setDetailsEmpresa(empresa)
    setShowDetails(true)
  }

  const handleDelete = async (empresa: Empresa) => {
    if (window.confirm(`Tem certeza que deseja excluir a empresa ${empresa.nome}?`)) {
      await deleteEmpresaAPI(empresa.id)
    }
  }

  const handleCloseForm = () => {
    setShowForm(false)
    setEditingEmpresa(null)
  }

  const handleCloseScriptExecutor = () => {
    setShowScriptExecutor(false)
    setExecutingEmpresa(null)
  }

  const handleCloseDetails = () => {
    setShowDetails(false)
    setDetailsEmpresa(null)
  }

  const handleEditFromDetails = () => {
    if (detailsEmpresa) {
      setEditingEmpresa(detailsEmpresa)
      setShowDetails(false)
      setDetailsEmpresa(null)
      setShowForm(true)
    }
  }

  const handleSetupDatabase = async () => {
    setDbStatus('🔄 Verificando banco...')
    const result = await setupDatabase()
    setDbStatus(result.message)
    
    if (result.needsManualSetup) {
      alert('⚠️ AÇÃO NECESSÁRIA:\n\n' +
            '1. Abra o Supabase Dashboard\n' +
            '2. Vá em SQL Editor\n' +
            '3. Execute o arquivo sql/create_tables.sql\n' +
            '4. Clique novamente em "Setup DB"')
    }
  }

  const handleTestConnection = async () => {
    setDbStatus('🔗 Testando conexão...')
    const result = await testConnection()
    
    if (result.success) {
      setDbStatus(`✅ Conexão OK! ${result.data.length} empresas encontradas`)
    } else {
      setDbStatus(`❌ Erro: ${result.error}`)
    }
  }

  const handleSubmitForm = () => {
    // Não é mais necessário recarregar, pois o store já atualiza automaticamente
    // fetchEmpresas() // Removido para evitar sobrescrever mudanças
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ativa': return 'bg-green-100 text-green-800'
      case 'inativa': return 'bg-red-100 text-red-800'
      case 'processando': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getScriptsProgress = (scripts_status: Empresa['scripts_status']) => {
    const total = Object.keys(scripts_status).length
    const completed = Object.values(scripts_status).filter(Boolean).length
    return { completed, total, percentage: (completed / total) * 100 }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Erro ao carregar empresas:</strong> {error.message}
        </div>
        <button
          onClick={handleTestConnection}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 mr-2"
        >
          🧪 Testar Conexão
        </button>
        <button
          onClick={handleSetupDatabase}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
        >
          🔧 Setup DB
        </button>
        {dbStatus && (
          <div className="mt-2 text-sm text-gray-600">
            {dbStatus}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Empresas Virtuais</h1>
        <div className="flex space-x-2">
          <button
            onClick={handleTestConnection}
            className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
          >
            🧪 Testar DB
          </button>
          <button
            onClick={handleSetupDatabase}
            className="bg-orange-600 text-white px-4 py-2 rounded-md hover:bg-orange-700"
          >
            🔧 Setup DB
          </button>
          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            + Nova Empresa
          </button>
        </div>
      </div>

      {/* Status do Banco */}
      {dbStatus && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">{dbStatus}</p>
        </div>
      )}

      {empresas.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Nenhuma empresa encontrada
          </h3>
          <p className="text-gray-500 mb-4">
            Comece criando sua primeira empresa virtual
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Criar Primeira Empresa
          </button>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {empresas.map((empresa) => {
            const progress = getScriptsProgress(empresa.scripts_status)
            
            return (
              <div
                key={empresa.id}
                className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow"
              >
                {/* Header */}
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {empresa.nome}
                    </h3>
                    <p className="text-sm text-gray-500">
                      Código: {empresa.codigo}
                    </p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(empresa.status)}`}>
                    {empresa.status}
                  </span>
                </div>

                {/* Descrição */}
                {empresa.descricao && (
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {empresa.descricao}
                  </p>
                )}

                {/* Informações */}
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">País:</span>
                    <span className="font-medium">{empresa.pais}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Personas:</span>
                    <span className="font-medium">{empresa.total_personas}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Idiomas:</span>
                    <span className="font-medium">
                      {empresa.idiomas.join(', ').toUpperCase()}
                    </span>
                  </div>
                </div>

                {/* Progresso dos Scripts */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-500">Scripts:</span>
                    <span className="text-gray-700">
                      {progress.completed}/{progress.total}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ width: `${progress.percentage}%` }}
                    ></div>
                  </div>
                </div>

                {/* Botões de Ação */}
                <div className="flex flex-col space-y-2">
                  <button
                    onClick={() => handleExecuteScripts(empresa)}
                    className="w-full bg-green-100 text-green-700 px-3 py-2 rounded-md text-sm hover:bg-green-200"
                  >
                    🚀 Executar Scripts
                  </button>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleViewDetails(empresa)}
                      className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded-md text-sm hover:bg-blue-200"
                    >
                      Ver Detalhes
                    </button>
                    <button
                      onClick={() => handleEdit(empresa)}
                      className="bg-gray-100 text-gray-700 px-3 py-2 rounded-md text-sm hover:bg-gray-200"
                    >
                      Editar
                    </button>
                    <button
                      onClick={() => handleDelete(empresa)}
                      className="bg-red-100 text-red-700 px-3 py-2 rounded-md text-sm hover:bg-red-200"
                    >
                      Excluir
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Modal do Formulário */}
      {showForm && (
        <EmpresaForm
          empresa={editingEmpresa}
          onClose={handleCloseForm}
          onSubmit={handleSubmitForm}
        />
      )}

      {/* Modal do Executor de Scripts */}
      {showScriptExecutor && executingEmpresa && (
        <ScriptExecutor
          empresa={executingEmpresa}
          onClose={handleCloseScriptExecutor}
        />
      )}

      {/* Modal de Detalhes */}
      {showDetails && detailsEmpresa && (
        <EmpresaDetails
          empresa={detailsEmpresa}
          onClose={handleCloseDetails}
          onEdit={handleEditFromDetails}
        />
      )}
    </div>
  )
}

export default EmpresaList