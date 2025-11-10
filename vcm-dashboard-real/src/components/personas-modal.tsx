'use client';

import { useState, useEffect } from 'react';
import { Empresa, Persona } from '@/lib/supabase';
import { usePersonasByEmpresa } from '@/lib/supabase-hooks';
import { X, User, Mail, MapPin, Briefcase, Calendar, Users } from 'lucide-react';

interface PersonasModalProps {
  empresa: Empresa | null;
  isOpen: boolean;
  onClose: () => void;
}

export function PersonasModal({ empresa, isOpen, onClose }: PersonasModalProps) {
  const { data: personas, isLoading, error } = usePersonasByEmpresa(empresa?.id || '', isOpen);

  if (!isOpen || !empresa) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg w-full max-w-6xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b bg-gray-50">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                Personas - {empresa.nome}
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
              <p className="text-sm text-gray-600">{error.message}</p>
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
                      {persona.full_name.split(' ').map((n: string) => n[0]).join('').substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{persona.full_name}</h3>
                      <p className="text-sm text-gray-600">{persona.role}</p>
                    </div>
                  </div>

                  {/* Informações Básicas */}
                  <div className="space-y-2 text-sm">
                    {persona.experiencia_anos && (
                      <div className="flex items-center gap-2 text-gray-600">
                        <Calendar size={14} />
                        <span>{persona.experiencia_anos} anos de experiência</span>
                      </div>
                    )}
                    
                    {persona.specialty && (
                      <div className="flex items-center gap-2 text-gray-600">
                        <MapPin size={14} />
                        <span>{persona.specialty}</span>
                      </div>
                    )}
                    
                    {persona.email && (
                      <div className="flex items-center gap-2 text-gray-600">
                        <Mail size={14} />
                        <span className="truncate">{persona.email}</span>
                      </div>
                    )}
                    
                    {persona.department && (
                      <div className="flex items-center gap-2 text-gray-600">
                        <Briefcase size={14} />
                        <span>{persona.department}</span>
                      </div>
                    )}
                  </div>

                  {/* Tipo */}
                  <div className="mt-3 pt-3 border-t">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      persona.role.toLowerCase().includes('executive') || persona.role.toLowerCase().includes('ceo')
                        ? 'bg-purple-100 text-purple-800'
                        : persona.role.toLowerCase().includes('specialist') || persona.role.toLowerCase().includes('especialista')
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-green-100 text-green-800'
                    }`}>
                      {persona.role}
                    </span>
                    
                    {persona.role.toLowerCase().includes('ceo') && (
                      <span className="ml-2 inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                        CEO
                      </span>
                    )}
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