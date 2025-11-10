'use client';

import { useState, useEffect } from 'react';
import { Empresa, Persona } from '@/lib/supabase';
import { usePersonasByEmpresa } from '@/lib/supabase-hooks';
import { X, User, Mail, MapPin, Briefcase, Calendar, Users } from 'lucide-react';

interface PersonasModalProps {
  company: any;
  onClose: () => void;
}

export function PersonasModal({ company, onClose }: PersonasModalProps) {
  const isOpen = !!company;
  
  // Mock data for development
  const mockPersonas = [
    {
      id: '1',
      nome_completo: 'Ana Silva',
      cargo: 'CEO',
      email: 'ana.silva@techvision.com',
      localizacao: 'São Paulo, SP',
      data_nascimento: '1985-03-15',
      bio_profissional: 'CEO experiente com 15 anos de liderança em tecnologia'
    },
    {
      id: '2', 
      nome_completo: 'Carlos Santos',
      cargo: 'CTO',
      email: 'carlos.santos@techvision.com',
      localizacao: 'Rio de Janeiro, RJ',
      data_nascimento: '1982-07-22',
      bio_profissional: 'CTO especialista em arquitetura de sistemas e inovação'
    }
  ];
  
  const personas = mockPersonas;
  const isLoading = false;
  const error = null;

  if (!isOpen || !company) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg w-full max-w-6xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b bg-gray-50">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Personas - {company.nome}
              </h2>
              <p className="text-sm text-gray-600">
                {personas?.length || 0} personas cadastradas
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-200 rounded-full transition-colors"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <span className="ml-2 text-gray-600">Carregando personas...</span>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <div className="text-red-600 mb-2">Erro ao carregar personas</div>
              <p className="text-sm text-gray-600">Tente novamente mais tarde</p>
            </div>
          ) : !personas || personas.length === 0 ? (
            <div className="text-center py-12">
              <Users size={48} className="mx-auto text-gray-400 mb-4" />
              <div className="text-gray-600 mb-2">Nenhuma persona encontrada</div>
              <p className="text-sm text-gray-500">
                Execute o gerador de biografias para criar personas para esta empresa.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {personas.map((persona) => (
                <div key={persona.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  {/* Avatar e Nome */}
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                      {persona.nome_completo.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{persona.nome_completo}</h3>
                      <p className="text-sm text-gray-600">{persona.cargo}</p>
                    </div>
                  </div>

                  {/* Informações Básicas */}
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2 text-gray-600">
                      <Mail size={14} />
                      <span>{persona.email}</span>
                    </div>
                    
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin size={14} />
                      <span>{persona.localizacao}</span>
                    </div>
                    
                    <div className="flex items-center gap-2 text-gray-600">
                      <Calendar size={14} />
                      <span>Nascido em {new Date(persona.data_nascimento).toLocaleDateString('pt-BR')}</span>
                    </div>
                  </div>
                  
                  {/* Bio Profissional */}
                  <div className="mt-3 pt-3 border-t">
                    <p className="text-sm text-gray-600">{persona.bio_profissional}</p>
                  </div>
                  
                  {/* Tipo baseado no cargo */}
                  <div className="mt-3">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      persona.cargo.toLowerCase().includes('ceo')
                        ? 'bg-purple-100 text-purple-800'
                        : persona.cargo.toLowerCase().includes('cto') || persona.cargo.toLowerCase().includes('tech')
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {persona.cargo}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t bg-gray-50">
          <div className="flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Fechar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}