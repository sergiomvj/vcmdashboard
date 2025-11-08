import React, { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import type { Empresa, Persona } from '../types'

// Import APIs diretamente dos arquivos
import { empresasAPI } from '../lib/api/empresas'
import { personasAPI } from '../lib/api/personas'

export const DatabaseTest: React.FC = () => {
  const [loading, setLoading] = useState(true)
  const [connected, setConnected] = useState(false)
  const [empresas, setEmpresas] = useState<Empresa[]>([])
  const [personas, setPersonas] = useState<Persona[]>([])
  const [error, setError] = useState<string | null>(null)

  // Testar conexão com Supabase
  useEffect(() => {
    const testConnection = async () => {
      try {
        const { data, error } = await supabase.from('empresas').select('*').limit(1)
        if (error) {
          setError(`Erro de conexão: ${error.message}`)
          setConnected(false)
        } else {
          setConnected(true)
          setError(null)
        }
      } catch (err) {
        setError(`Erro de conexão: ${err}`)
        setConnected(false)
      } finally {
        setLoading(false)
      }
    }

    testConnection()
  }, [])

  // Carregar empresas
  useEffect(() => {
    const loadEmpresas = async () => {
      try {
        const data = await empresasAPI.getAll()
        setEmpresas(data)
      } catch (err) {
        console.error('Erro ao carregar empresas:', err)
      }
    }

    if (connected) {
      loadEmpresas()
    }
  }, [connected])

  // Carregar personas
  useEffect(() => {
    const loadPersonas = async () => {
      try {
        const data = await personasAPI.getAll()
        setPersonas(data)
      } catch (err) {
        console.error('Erro ao carregar personas:', err)
      }
    }

    if (connected) {
      loadPersonas()
    }
  }, [connected])

  if (loading) {
    return (
      <div className="p-6 bg-white rounded-lg shadow">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Testando conexão...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Teste de Conexão com Banco de Dados</h2>
      
      {/* Status da Conexão */}
      <div className="mb-6">
        {connected ? (
          <div className="flex items-center text-green-600">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span className="font-medium">Conexão estabelecida com sucesso!</span>
          </div>
        ) : (
          <div className="flex items-center text-red-600">
            <div className="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
            <span className="font-medium">Falha na conexão</span>
          </div>
        )}
        
        {error && (
          <div className="mt-2 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-medium text-gray-900 mb-2">Empresas</h3>
          <p className="text-2xl font-bold text-blue-600">{empresas.length}</p>
          <p className="text-sm text-gray-600">empresas cadastradas</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <h3 className="font-medium text-gray-900 mb-2">Personas</h3>
          <p className="text-2xl font-bold text-green-600">{personas.length}</p>
          <p className="text-sm text-gray-600">personas cadastradas</p>
        </div>
      </div>

      {/* Lista de Empresas */}
      {empresas.length > 0 && (
        <div className="mb-6">
          <h3 className="font-medium text-gray-900 mb-3">Empresas Recentes</h3>
          <div className="space-y-2">
            {empresas.slice(0, 3).map(empresa => (
              <div key={empresa.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{empresa.nome}</p>
                  <p className="text-sm text-gray-600">{empresa.pais}</p>
                </div>
                <span className={`px-2 py-1 text-xs rounded-full ${
                  empresa.status === 'ativa' ? 'bg-green-100 text-green-800' : 
                  empresa.status === 'inativa' ? 'bg-red-100 text-red-800' : 
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {empresa.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Lista de Personas */}
      {personas.length > 0 && (
        <div>
          <h3 className="font-medium text-gray-900 mb-3">Personas Recentes</h3>
          <div className="space-y-2">
            {personas.slice(0, 3).map(persona => (
              <div key={persona.id} className="p-3 bg-gray-50 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{persona.full_name}</p>
                    <p className="text-sm text-gray-600">{persona.role} • {persona.department}</p>
                  </div>
                  <span className={`px-2 py-1 text-xs rounded-full ${
                    persona.status === 'active' ? 'bg-green-100 text-green-800' : 
                    persona.status === 'inactive' ? 'bg-red-100 text-red-800' : 
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {persona.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Informações Técnicas */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="font-medium text-gray-900 mb-2">Informações Técnicas</h3>
        <div className="text-sm text-gray-600 space-y-1">
          <p>• Cliente: Supabase</p>
          <p>• Tabelas: empresas, personas</p>
          <p>• API: REST com TypeScript</p>
          <p>• Status: {connected ? 'Conectado' : 'Desconectado'}</p>
        </div>
      </div>
    </div>
  )
}