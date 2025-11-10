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
import { 
  Target, 
  Users, 
  Building2,
  CheckCircle2,
  Clock,
  AlertCircle
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
    nome_completo: 'Ana Silva',
    cargo: 'CEO',
    categoria: 'executivos',
    metas_count: 3,
    metas_concluidas: 2
  },
  {
    id: '2',
    nome_completo: 'Carlos Santos',
    cargo: 'CTO', 
    categoria: 'executivos',
    metas_count: 5,
    metas_concluidas: 3
  },
  {
    id: '3',
    nome_completo: 'Maria Costa',
    cargo: 'Desenvolvedora Senior',
    categoria: 'especialistas',
    metas_count: 4,
    metas_concluidas: 4
  }
];

const mockMetas = [
  {
    id: '1',
    titulo: 'Implementar Sistema de Autenticação',
    descricao: 'Desenvolver sistema completo de login e controle de acesso',
    status: 'concluida',
    data_limite: '2024-12-15',
    progresso: 100,
    tipo: 'tecnica'
  },
  {
    id: '2', 
    titulo: 'Otimizar Performance da API',
    descricao: 'Melhorar tempo de resposta em 40%',
    status: 'em_progresso',
    data_limite: '2024-12-30',
    progresso: 65,
    tipo: 'tecnica'
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
        return <Clock className="h-4 w-4" />;
    }
  };

  const filteredPersonas = mockPersonas;
  const filteredMetas = selectedPersona 
    ? mockMetas.filter(meta => meta.id !== '3') // Simular filtro por persona
    : mockMetas;

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
                    <h4 className="font-medium text-gray-900">{empresa.nome}</h4>
                    <p className="text-sm text-gray-600">{empresa.industry}</p>
                  </div>
                  <div className="flex flex-col items-end">
                    <Badge 
                      variant={empresa.ativa ? "default" : "secondary"}
                      className="mb-1"
                    >
                      {empresa.ativa ? 'Ativa' : 'Inativa'}
                    </Badge>
                    <span className="text-xs text-gray-500">
                      {empresa.personas_count} personas
                    </span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Coluna 2: Lista de Personas (20%) */}
        <div className="col-span-2 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center gap-2 mb-4">
            <Users className="h-5 w-5 text-gray-600" />
            <h3 className="font-semibold">Personas</h3>
          </div>
          
          <div className="space-y-2">
            {filteredPersonas.map((persona) => (
              <button
                key={persona.id}
                onClick={() => setSelectedPersona(persona.id)}
                className={`w-full text-left p-3 rounded-lg transition-colors ${
                  selectedPersona === persona.id
                    ? 'bg-green-50 border-2 border-green-200'
                    : 'hover:bg-gray-50 border-2 border-transparent'
                }`}
              >
                <div>
                  <h4 className="font-medium text-gray-900 text-sm">{persona.nome_completo}</h4>
                  <p className="text-xs text-gray-600">{persona.cargo}</p>
                  <div className="mt-2 text-xs">
                    <Badge variant="outline" className="text-xs">
                      {persona.categoria}
                    </Badge>
                    <div className="mt-1 text-gray-500">
                      {persona.metas_concluidas}/{persona.metas_count} metas
                    </div>
                  </div>
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
            <Button size="sm">
              <Target className="h-4 w-4 mr-2" />
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
                      <CardDescription className="mt-1">
                        {meta.descricao}
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge 
                        className={`${getStatusColor(meta.status)} text-white`}
                      >
                        <span className="flex items-center gap-1">
                          {getStatusIcon(meta.status)}
                          {meta.status.replace('_', ' ')}
                        </span>
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-3">
                    {/* Progresso */}
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Progresso</span>
                        <span>{meta.progresso}%</span>
                      </div>
                      <Progress value={meta.progresso} className="h-2" />
                    </div>

                    {/* Data limite */}
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Data limite:</span>
                      <span className={`font-medium ${
                        new Date(meta.data_limite) < new Date() ? 'text-red-600' : 'text-gray-900'
                      }`}>
                        {format(new Date(meta.data_limite), 'dd/MM/yyyy', { locale: ptBR })}
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
    </div>
  );
}