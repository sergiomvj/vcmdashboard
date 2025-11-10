'use client';

import { useOutputs } from '@/lib/hooks';
import { Loader2, FileText, Folder, Users, Target, Database } from 'lucide-react';

interface OutputsResponse {
  success: boolean;
  data: {
    personas_config?: {
      size: number;
      modified: string;
    };
    biografias: BiografiasData;
    competencias: CompetenciasData;
  };
}

interface BiografiasData {
  [key: string]: unknown[];
}

interface CompetenciasData {
  [key: string]: unknown[];
}

interface Persona {
  nome: string;
  cargo: string;
  persona: string;
  [key: string]: unknown;
}

interface Competencia {
  nome: string;
  tipo: string;
  [key: string]: unknown;
}

export function OutputsPanel() {
  const { data: outputsData, isLoading } = useOutputs();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-lg font-semibold mb-4">Outputs Gerados</h3>
        <div className="flex items-center gap-2">
          <Loader2 size={20} className="animate-spin" />
          <span>Carregando outputs...</span>
        </div>
      </div>
    );
  }

  if (!outputsData || !(outputsData as OutputsResponse).success) {
    return (
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-lg font-semibold mb-4">Outputs Gerados</h3>
        <div className="text-red-600">Erro ao carregar outputs</div>
      </div>
    );
  }

  const outputs = (outputsData as OutputsResponse).data || {
    biografias: {},
    competencias: {}
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'executivos': return Users;
      case 'assistentes': return Target;
      case 'especialistas': return Database;
      default: return Folder;
    }
  };

  const countPersonas = (biografias: BiografiasData) => {
    return Object.values(biografias).reduce((total: number, category: unknown[]) => {
      return total + (Array.isArray(category) ? category.length : 0);
    }, 0);
  };

  const countCompetencias = (competencias: CompetenciasData) => {
    return Object.values(competencias).reduce((total: number, category: unknown[]) => {
      return total + (Array.isArray(category) ? category.length : 0);
    }, 0);
  };

  return (
    <div className="bg-white rounded-lg border p-6">
      <h3 className="text-lg font-semibold mb-4">Outputs Gerados</h3>
      
      <div className="space-y-6">
        {/* Personas Config */}
        {outputs.personas_config && (
          <div className="border-l-4 border-blue-500 pl-4">
            <div className="flex items-center gap-2 mb-2">
              <FileText size={20} className="text-blue-600" />
              <h4 className="font-medium">Configuração de Personas</h4>
            </div>
            <p className="text-sm text-gray-600 mb-1">
              Arquivo principal com todas as personas geradas
            </p>
            <div className="text-xs text-gray-500">
              Tamanho: {(outputs.personas_config.size / 1024).toFixed(1)} KB | 
              Modificado: {new Date(outputs.personas_config.modified).toLocaleString()}
            </div>
          </div>
        )}

        {/* Biografias */}
        {Object.keys(outputs.biografias).length > 0 && (
          <div className="border-l-4 border-green-500 pl-4">
            <div className="flex items-center gap-2 mb-2">
              <Users size={20} className="text-green-600" />
              <h4 className="font-medium">Biografias ({countPersonas(outputs.biografias)} personas)</h4>
            </div>
            
            <div className="space-y-2">
              {Object.entries(outputs.biografias).map(([categoria, personas]: [string, unknown[]]) => {
                if (!Array.isArray(personas) || personas.length === 0) return null;
                
                const Icon = getCategoryIcon(categoria);
                
                return (
                  <div key={categoria} className="bg-gray-50 rounded p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <Icon size={16} className="text-gray-600" />
                      <span className="font-medium text-sm capitalize">{categoria}</span>
                      <span className="text-xs text-gray-500">({personas.length})</span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-1 text-xs">
                      {(personas as Persona[]).slice(0, 6).map((persona: Persona, index: number) => (
                        <div key={index} className="text-gray-600">
                          • {persona.persona.replace(/_/g, ' ')}
                        </div>
                      ))}
                      {personas.length > 6 && (
                        <div className="text-gray-500 italic">
                          +{personas.length - 6} mais...
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Competências */}
        {Object.keys(outputs.competencias).length > 0 && (
          <div className="border-l-4 border-purple-500 pl-4">
            <div className="flex items-center gap-2 mb-2">
              <Target size={20} className="text-purple-600" />
              <h4 className="font-medium">Competências ({countCompetencias(outputs.competencias)} personas)</h4>
            </div>
            
            <div className="space-y-2">
              {Object.entries(outputs.competencias).map(([categoria, competencias]: [string, unknown[]]) => {
                if (!Array.isArray(competencias) || competencias.length === 0) return null;
                
                const Icon = getCategoryIcon(categoria);
                
                return (
                  <div key={categoria} className="bg-gray-50 rounded p-3">
                    <div className="flex items-center gap-2 mb-2">
                      <Icon size={16} className="text-gray-600" />
                      <span className="font-medium text-sm capitalize">{categoria}</span>
                      <span className="text-xs text-gray-500">({competencias.length})</span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-1 text-xs">
                      {(competencias as Competencia[]).slice(0, 4).map((comp: Competencia, index: number) => (
                        <div key={index} className="text-gray-600 flex items-center gap-1">
                          <Target size={12} />
                          {(comp.persona as string).replace(/_/g, ' ')}
                        </div>
                      ))}
                      {competencias.length > 4 && (
                        <div className="text-gray-500 italic">
                          +{competencias.length - 4} mais...
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Status quando não há outputs */}
        {!outputs.personas_config && Object.keys(outputs.biografias).length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <Folder size={48} className="mx-auto mb-4 opacity-50" />
            <p>Nenhum output encontrado</p>
            <p className="text-sm">Execute o gerador de biografias para começar</p>
          </div>
        )}
      </div>

      <div className="mt-6 pt-4 border-t text-xs text-gray-500">
        Última verificação: {new Date().toLocaleString()}
      </div>
    </div>
  );
}