import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useEmpresaStore } from '../store/empresaStore';

function Dashboard() {
  const { empresas, fetchEmpresas } = useEmpresaStore()

  useEffect(() => {
    fetchEmpresas();
  }, [fetchEmpresas]);

  // Calcular estatísticas
  const totalEmpresas = empresas.length
  const empresasAtivas = empresas.filter(emp => emp.status === 'ativa').length
  const totalPersonas = empresas.reduce((acc, emp) => acc + emp.total_personas, 0)
  
  // Calcular progresso geral dos scripts
  const totalScripts = empresas.length * 6 // 6 scripts por empresa
  const scriptsCompletos = empresas.reduce((acc, emp) => {
    return acc + Object.values(emp.scripts_status).filter(Boolean).length
  }, 0)
  const progressoGeral = totalScripts > 0 ? (scriptsCompletos / totalScripts) * 100 : 0

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard VCM</h1>
        <p className="text-gray-600">Visão geral do Virtual Company Manager</p>
      </div>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        {/* Empresas Totais */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Empresas Virtuais</p>
              <p className="text-2xl font-bold text-gray-900">{totalEmpresas}</p>
            </div>
            <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🏢</span>
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <span className="text-green-600 font-medium">{empresasAtivas} ativas</span>
          </div>
        </div>

        {/* Total Personas */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Personas</p>
              <p className="text-2xl font-bold text-gray-900">{totalPersonas}</p>
            </div>
            <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">👥</span>
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <span className="text-gray-500">Distribuídas em {totalEmpresas} empresa{totalEmpresas !== 1 ? 's' : ''}</span>
          </div>
        </div>

        {/* Scripts Executados */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Scripts Executados</p>
              <p className="text-2xl font-bold text-gray-900">{scriptsCompletos}/{totalScripts}</p>
            </div>
            <div className="h-12 w-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">⚙️</span>
            </div>
          </div>
          <div className="mt-2">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-yellow-600 h-2 rounded-full transition-all"
                style={{ width: `${progressoGeral}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Status Sincronização */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Sincronização</p>
              <p className="text-2xl font-bold text-green-600">Online</p>
            </div>
            <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
              <span className="text-2xl">🔄</span>
            </div>
          </div>
          <div className="mt-2 flex items-center text-sm">
            <div className="h-2 w-2 bg-green-500 rounded-full mr-2"></div>
            <span className="text-green-600">Supabase conectado</span>
          </div>
        </div>
      </div>

      {/* Seção de Ações Rápidas */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <Link
            to="/empresas"
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <span className="text-xl">➕</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Nova Empresa</h3>
                <p className="text-sm text-gray-500">Criar empresa virtual</p>
              </div>
            </div>
          </Link>

          <Link
            to="/empresas"
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 bg-green-100 rounded-lg flex items-center justify-center">
                <span className="text-xl">🚀</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Executar Scripts</h3>
                <p className="text-sm text-gray-500">Gerar personas e workflows</p>
              </div>
            </div>
          </Link>

          <div className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 bg-purple-100 rounded-lg flex items-center justify-center">
                <span className="text-xl">📊</span>
              </div>
              <div>
                <h3 className="font-medium text-gray-900">Ver Relatórios</h3>
                <p className="text-sm text-gray-500">Análises e métricas</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lista de Empresas Recentes */}
      {empresas.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Empresas Recentes</h2>
            <Link
              to="/empresas"
              className="text-sm text-blue-600 hover:text-blue-800"
            >
              Ver todas →
            </Link>
          </div>
          
          <div className="space-y-3">
            {empresas.slice(0, 3).map((empresa) => {
              const progress = Object.values(empresa.scripts_status).filter(Boolean).length
              const total = Object.keys(empresa.scripts_status).length
              const percentage = (progress / total) * 100
              
              return (
                <div key={empresa.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="h-8 w-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-sm font-medium">{empresa.codigo.charAt(0)}</span>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{empresa.nome}</h4>
                      <p className="text-sm text-gray-500">{empresa.total_personas} personas</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">{progress}/{total}</p>
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${percentage}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      empresa.status === 'ativa' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {empresa.status}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard