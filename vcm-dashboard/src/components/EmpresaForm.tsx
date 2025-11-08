import { useState, useEffect } from 'react'
import type { Empresa, CreateEmpresa, UpdateEmpresa } from '../types/empresa'
import { useEmpresaStore } from '../store/empresaStore'

interface EmpresaFormProps {
  empresa?: Empresa | null
  onClose: () => void
  onSubmit: () => void
}

const EmpresaForm: React.FC<EmpresaFormProps> = ({ empresa, onClose, onSubmit }) => {
  const { createEmpresa, updateEmpresaAPI, loading } = useEmpresaStore()
  
  const [formData, setFormData] = useState({
    codigo: '',
    nome: '',
    descricao: '',
    pais: 'BR',
    idiomas: ['pt'],
    total_personas: 20,
    status: 'ativa' as 'ativa' | 'inativa'
  })

  useEffect(() => {
    if (empresa) {
      setFormData({
        codigo: empresa.codigo,
        nome: empresa.nome,
        descricao: empresa.descricao,
        pais: empresa.pais,
        idiomas: empresa.idiomas,
        total_personas: empresa.total_personas,
        status: empresa.status === 'processando' ? 'ativa' : empresa.status
      })
    }
  }, [empresa])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    console.log('🔄 Salvando empresa...', { empresa: empresa?.id, formData })
    
    try {
      if (empresa) {
        console.log('✏️ Atualizando empresa existente:', empresa.id)
        await updateEmpresaAPI(empresa.id, formData)
        console.log('✅ Empresa atualizada com sucesso!')
      } else {
        console.log('➕ Criando nova empresa')
        await createEmpresa({
          ...formData,
          scripts_status: {
            biografias: false,
            competencias: false,
            tech_specs: false,
            rag: false,
            fluxos: false,
            workflows: false
          }
        })
        console.log('✅ Empresa criada com sucesso!')
      }
      onSubmit()
      onClose()
    } catch (error) {
      console.error('❌ Erro ao salvar empresa:', error)
    }
  }

  const handleIdiomaChange = (idioma: string, checked: boolean) => {
    if (checked) {
      setFormData(prev => ({
        ...prev,
        idiomas: [...prev.idiomas, idioma]
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        idiomas: prev.idiomas.filter(i => i !== idioma)
      }))
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">
            {empresa ? 'Editar Empresa' : 'Nova Empresa'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Código da Empresa */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Código da Empresa *
            </label>
            <input
              type="text"
              value={formData.codigo}
              onChange={(e) => setFormData(prev => ({ ...prev, codigo: e.target.value.toUpperCase() }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: LIFEWAY"
              required
              disabled={!!empresa} // Não permite editar código de empresa existente
            />
          </div>

          {/* Nome da Empresa */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nome da Empresa *
            </label>
            <input
              type="text"
              value={formData.nome}
              onChange={(e) => setFormData(prev => ({ ...prev, nome: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: LifewayUSA"
              required
            />
          </div>

          {/* Descrição */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Descrição
            </label>
            <textarea
              value={formData.descricao}
              onChange={(e) => setFormData(prev => ({ ...prev, descricao: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
              placeholder="Descrição da empresa..."
            />
          </div>

          {/* País */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              País *
            </label>
            <select
              value={formData.pais}
              onChange={(e) => setFormData(prev => ({ ...prev, pais: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="BR">Brasil</option>
              <option value="US">Estados Unidos</option>
              <option value="ES">Espanha</option>
              <option value="MX">México</option>
              <option value="AR">Argentina</option>
            </select>
          </div>

          {/* Idiomas */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Idiomas das Personas *
            </label>
            <div className="space-y-2">
              {[
                { code: 'pt', name: 'Português' },
                { code: 'en', name: 'Inglês' },
                { code: 'es', name: 'Espanhol' },
                { code: 'fr', name: 'Francês' },
                { code: 'de', name: 'Alemão' }
              ].map(idioma => (
                <label key={idioma.code} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.idiomas.includes(idioma.code)}
                    onChange={(e) => handleIdiomaChange(idioma.code, e.target.checked)}
                    className="mr-2"
                  />
                  {idioma.name}
                </label>
              ))}
            </div>
          </div>

          {/* Total de Personas */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Total de Personas *
            </label>
            <select
              value={formData.total_personas}
              onChange={(e) => setFormData(prev => ({ ...prev, total_personas: parseInt(e.target.value) }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value={10}>10 Personas</option>
              <option value={15}>15 Personas</option>
              <option value={20}>20 Personas (Recomendado)</option>
              <option value={25}>25 Personas</option>
              <option value={30}>30 Personas</option>
            </select>
          </div>

          {/* Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={formData.status}
              onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value as 'ativa' | 'inativa' }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ativa">Ativa</option>
              <option value="inativa">Inativa</option>
            </select>
          </div>

          {/* Botões */}
          <div className="flex justify-end space-x-2 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
              disabled={loading}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              disabled={loading}
            >
              {loading ? 'Salvando...' : empresa ? 'Atualizar' : 'Criar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default EmpresaForm