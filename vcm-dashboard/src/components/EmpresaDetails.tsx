import type { Empresa } from '../types/empresa'

interface EmpresaDetailsProps {
  empresa: Empresa;
  onClose: () => void;
  onEdit: () => void;
}

const EmpresaDetails: React.FC<EmpresaDetailsProps> = ({ empresa, onClose, onEdit }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ativa': return 'bg-green-100 text-green-800 border-green-300'
      case 'inativa': return 'bg-red-100 text-red-800 border-red-300'
      case 'processando': return 'bg-yellow-100 text-yellow-800 border-yellow-300'
      default: return 'bg-gray-100 text-gray-800 border-gray-300'
    }
  }

  const getScriptStatus = (status: boolean) => {
    return status ? '✅ Concluído' : '⏳ Pendente'
  }

  const getScriptStatusColor = (status: boolean) => {
    return status ? 'text-green-600' : 'text-yellow-600'
  }

  const scriptsInfo = [
    { key: 'biografias', name: 'Biografias', description: 'Geração das biografias das personas' },
    { key: 'competencias', name: 'Competências', description: 'Análise de competências técnicas e comportamentais' },
    { key: 'tech_specs', name: 'Especificações Técnicas', description: 'Definição de tecnologias e ferramentas' },
    { key: 'rag', name: 'RAG Database', description: 'População do banco de conhecimento RAG' },
    { key: 'fluxos', name: 'Análise de Fluxos', description: 'Mapeamento de processos de negócio' },
    { key: 'workflows', name: 'Workflows N8N', description: 'Geração de automações N8N' }
  ]

  const progress = Object.values(empresa.scripts_status).filter(Boolean).length
  const total = Object.keys(empresa.scripts_status).length
  const percentage = (progress / total) * 100

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        
        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{empresa.nome}</h2>
            <p className="text-gray-600">Código: {empresa.codigo}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(empresa.status)}`}>
              {empresa.status}
            </span>
            <button
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-xl p-1"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Informações Básicas */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          
          {/* Informações Gerais */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Informações Gerais</h3>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-gray-700">Descrição</label>
                <p className="text-gray-900">{empresa.descricao || 'Não informado'}</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">País</label>
                  <p className="text-gray-900">{empresa.pais}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Total Personas</label>
                  <p className="text-gray-900">{empresa.total_personas}</p>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700">Idiomas</label>
                <div className="flex flex-wrap gap-2 mt-1">
                  {empresa.idiomas.map(idioma => (
                    <span 
                      key={idioma}
                      className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      {idioma.toUpperCase()}
                    </span>
                  ))}
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Criado em</label>
                  <p className="text-gray-900 text-sm">
                    {new Date(empresa.created_at).toLocaleDateString('pt-BR')}
                  </p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Atualizado em</label>
                  <p className="text-gray-900 text-sm">
                    {new Date(empresa.updated_at).toLocaleDateString('pt-BR')}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Progresso dos Scripts */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Progresso dos Scripts</h3>
            
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-700">Progresso Geral</span>
                <span className="font-medium">{progress}/{total} ({Math.round(percentage)}%)</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full transition-all"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
            </div>

            <div className="space-y-3">
              {scriptsInfo.map((script) => (
                <div key={script.key} className="border border-gray-200 rounded-lg p-3">
                  <div className="flex justify-between items-start mb-1">
                    <h4 className="font-medium text-gray-900">{script.name}</h4>
                    <span className={`text-sm font-medium ${getScriptStatusColor(empresa.scripts_status[script.key as keyof typeof empresa.scripts_status])}`}>
                      {getScriptStatus(empresa.scripts_status[script.key as keyof typeof empresa.scripts_status])}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600">{script.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Botões de Ação */}
        <div className="flex justify-end space-x-3 pt-4 border-t">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Fechar
          </button>
          <button
            onClick={onEdit}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Editar Empresa
          </button>
        </div>
      </div>
    </div>
  )
}

export default EmpresaDetails