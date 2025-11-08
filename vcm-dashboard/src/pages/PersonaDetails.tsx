import React from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'

const PersonaDetails: React.FC = () => {
  const { id } = useParams()

  return (
    <div className="p-6">
      <div className="flex items-center mb-6">
        <Link to="/personas">
          <button className="inline-flex items-center px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar
          </button>
        </Link>
        <h1 className="text-2xl font-bold text-gray-900 ml-4">Detalhes da Persona #{id}</h1>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div className="text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Persona não encontrada</h3>
          <p className="text-gray-500">A persona com ID {id} não foi encontrada.</p>
        </div>
      </div>
    </div>
  )
}

export default PersonaDetails