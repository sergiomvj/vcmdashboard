import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/lib/supabase';
import { 
  MetaGlobal, 
  MetaPersona, 
  EmpresaCompleta,
  PersonaCompleta 
} from '@/types/database';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { NovaMetaModal } from '@/components/nova-meta-modal';
import { 
  Target, 
  Users, 
  Building2,
  CheckCircle2,
  Clock,
  AlertCircle,
  Plus
} from 'lucide-react';
import { format } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// Mock data para demonstração
const mockEmpresas = [
  {
    id: '1',
    nome: 'TechVision Solutions',
    industry: 'Tecnologia',
    ativa: true,
    personas_count: 20
  },
  {
    id: '2', 
    nome: 'HealthCare Plus',
    industry: 'Saúde',
    ativa: true,
    personas_count: 15
  },
  {
    id: '3',
    nome: 'EduTech Academy',
    industry: 'Educação', 
    ativa: false,
    personas_count: 12
  }
];

const mockPersonas = [
  {
    id: '1',
    empresa_id: '1',
    nome_completo: 'Ana Silva',
    cargo: 'CEO',
    email: 'ana.silva@techvision.com',
    metas_count: 3,
    metas_concluidas: 2
  },
  {
    id: '2',
    empresa_id: '1', 
    nome_completo: 'Carlos Santos',
    cargo: 'CTO',
    email: 'carlos.santos@techvision.com',
    metas_count: 5,
    metas_concluidas: 3
  },
  {
    id: '3',
    empresa_id: '1',
    nome_completo: 'Maria Costa', 
    cargo: 'Tech Lead',
    email: 'maria.costa@techvision.com',
    metas_count: 4,
    metas_concluidas: 4
  }
];

const mockMetas = [
  {
    id: '1',
    titulo: 'Aumentar Produtividade em 25%',
    descricao: 'Implementar ferramentas de automação para aumentar a produtividade da equipe',
    status: 'em_progresso',
    data_limite: '2024-12-31',
    progresso: 65,
    tipo: 'performance'
  },
  {
    id: '2',
    titulo: 'Certificação AWS',
    descricao: 'Obter certificação AWS Solutions Architect',
    status: 'concluida',
    data_limite: '2024-11-30',
    progresso: 100,
    tipo: 'desenvolvimento'
  },
  {
    id: '3',
    titulo: 'Treinamento em React',
    descricao: 'Completar curso avançado de React e TypeScript',
    status: 'pendente',
    data_limite: '2025-01-15', 
    progresso: 20,
    tipo: 'desenvolvimento'
  }
];

export function ObjetivosMetas() {
  const [selectedEmpresa, setSelectedEmpresa] = useState<string>('1');
  const [selectedPersona, setSelectedPersona] = useState<string>('');
  const [showNovaMetaModal, setShowNovaMetaModal] = useState(false);
  const [metas, setMetas] = useState(mockMetas);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'concluida':
        return 'bg-green-500';
      case 'em_progresso':
        return 'bg-blue-500';
      case 'atrasada':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'concluida':
        return <CheckCircle2 className="h-4 w-4" />;
      case 'em_progresso':
        return <Clock className="h-4 w-4" />;
      case 'atrasada':
        return <AlertCircle className="h-4 w-4" />;
      default:
        return <Target className="h-4 w-4" />;
    }
  };

  const handleSaveMeta = (metaData: any) => {
    setMetas(prev => [...prev, metaData]);
    console.log('Nova meta criada:', metaData);
  };

  const filteredPersonas = mockPersonas;
  const filteredMetas = selectedPersona 
    ? metas.filter((meta: any) => meta.id !== '3') // Simular filtro por persona
    : metas;

  return (
    <div className="w-full">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Objetivos e Metas</h2>
        <p className="text-gray-600">Gerencie objetivos e acompanhe o progresso das personas</p>
      </div>

      {/* Layout de 3 colunas */}
      <div className="grid grid-cols-10 gap-6 h-[calc(100vh-200px)]">
        
        {/* Coluna 1: Menu de Empresas (30%) */}
        <div className="col-span-3 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center gap-2 mb-4">
            <Building2 className="h-5 w-5 text-gray-600" />
            <h3 className="font-semibold">Empresas</h3>
          </div>
          
          <div className="space-y-2">
            {mockEmpresas.map((empresa) => (
              <button
                key={empresa.id}
                onClick={() => {
                  setSelectedEmpresa(empresa.id);
                  setSelectedPersona('');
                }}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  selectedEmpresa === empresa.id
                    ? 'bg-blue-50 border-2 border-blue-200'
                    : 'hover:bg-gray-50 border-2 border-transparent'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold text-gray-900">{empresa.nome}</h4>
                    <p className="text-sm text-gray-600">{empresa.industry}</p>
                  </div>
                  <Badge variant={empresa.ativa ? "default" : "secondary"}>
                    {empresa.ativa ? 'Ativa' : 'Inativa'}
                  </Badge>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Coluna 2: Personas (20%) */}
        <div className="col-span-2 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center gap-2 mb-4">
            <Users className="h-5 w-5 text-gray-600" />
            <h3 className="font-semibold">Personas</h3>
          </div>
          
          <div className="space-y-2">
            <button
              onClick={() => setSelectedPersona('')}
              className={`w-full text-left p-2 rounded-md transition-colors ${
                selectedPersona === ''
                  ? 'bg-blue-50 border border-blue-200'
                  : 'hover:bg-gray-50'
              }`}
            >
              <div className="text-sm font-medium">Todas</div>
            </button>
            
            {filteredPersonas.map((persona) => (
              <button
                key={persona.id}
                onClick={() => setSelectedPersona(persona.id)}
                className={`w-full text-left p-2 rounded-md transition-colors ${
                  selectedPersona === persona.id
                    ? 'bg-blue-50 border border-blue-200'
                    : 'hover:bg-gray-50'
                }`}
              >
                <div className="text-sm font-medium text-gray-900">{persona.nome_completo}</div>
                <div className="text-xs text-gray-600">{persona.cargo}</div>
                <div className="text-xs text-blue-600 mt-1">
                  {persona.metas_concluidas}/{persona.metas_count} metas
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Coluna 3: Resultados das Metas (50%) */}
        <div className="col-span-5 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Target className="h-5 w-5 text-gray-600" />
              <h3 className="font-semibold">
                {selectedPersona 
                  ? `Metas - ${filteredPersonas.find(p => p.id === selectedPersona)?.nome_completo}` 
                  : 'Todas as Metas'
                }
              </h3>
            </div>
            <Button 
              size="sm"
              onClick={() => setShowNovaMetaModal(true)}
            >
              <Plus className="h-4 w-4 mr-2" />
              Nova Meta
            </Button>
          </div>

          <div className="space-y-4">
            {filteredMetas.map((meta) => (
              <Card key={meta.id} className="relative">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg">{meta.titulo}</CardTitle>
                      <CardDescription className="mt-1">{meta.descricao}</CardDescription>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      {getStatusIcon(meta.status)}
                      <Badge 
                        variant={meta.status === 'concluida' ? 'default' : 'secondary'}
                        className={`${getStatusColor(meta.status)} text-white`}
                      >
                        {meta.status.replace('_', ' ')}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-4">
                    {/* Progresso */}
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-600">Progresso:</span>
                        <span className="font-medium">{meta.progresso}%</span>
                      </div>
                      <Progress value={meta.progresso} className="h-2" />
                    </div>

                    {/* Data Limite */}
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Data limite:</span>
                      <span className={`font-medium ${
                        new Date(meta.data_limite) < new Date() && meta.status !== 'concluida'
                          ? 'text-red-600'
                          : 'text-gray-900'
                      }`}>
                        {new Date(meta.data_limite).toLocaleDateString('pt-BR')}
                      </span>
                    </div>

                    {/* Tipo */}
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Tipo:</span>
                      <Badge variant="outline" className="text-xs">
                        {meta.tipo}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}

            {filteredMetas.length === 0 && (
              <div className="text-center py-12">
                <Target className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900">Nenhuma meta encontrada</h3>
                <p className="text-gray-600 mt-2">
                  {selectedPersona 
                    ? 'Esta persona ainda não possui metas definidas.'
                    : 'Selecione uma empresa para visualizar as metas.'
                  }
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal Nova Meta */}
      <NovaMetaModal
        isOpen={showNovaMetaModal}
        onClose={() => setShowNovaMetaModal(false)}
        onSave={handleSaveMeta}
        selectedPersona={selectedPersona}
      />
    </div>
  );
}