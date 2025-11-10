import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Shield, 
  AlertTriangle, 
  CheckCircle2, 
  XCircle, 
  Clock, 
  TrendingUp,
  TrendingDown,
  Users,
  Building2,
  Search,
  RefreshCw
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
    personas_count: 20,
    auditoria_score: 85,
    last_audit: '2024-12-01'
  },
  {
    id: '2', 
    nome: 'HealthCare Plus',
    industry: 'Saúde',
    ativa: true,
    personas_count: 15,
    auditoria_score: 92,
    last_audit: '2024-11-28'
  },
  {
    id: '3',
    nome: 'EduTech Academy',
    industry: 'Educação', 
    ativa: false,
    personas_count: 12,
    auditoria_score: 78,
    last_audit: '2024-11-15'
  }
];

const mockPersonas = [
  {
    id: '1',
    nome_completo: 'Ana Silva',
    cargo: 'CEO',
    categoria: 'executivos',
    compatibilidade_score: 95,
    issues_count: 1,
    last_check: '2024-12-01'
  },
  {
    id: '2',
    nome_completo: 'Carlos Santos',
    cargo: 'CTO', 
    categoria: 'executivos',
    compatibilidade_score: 88,
    issues_count: 3,
    last_check: '2024-12-01'
  },
  {
    id: '3',
    nome_completo: 'Maria Costa',
    cargo: 'Desenvolvedora Senior',
    categoria: 'especialistas',
    compatibilidade_score: 92,
    issues_count: 0,
    last_check: '2024-12-01'
  }
];

const mockAuditorias = [
  {
    id: '1',
    tipo: 'Compatibilidade de Cargo',
    status: 'aprovado',
    score: 95,
    descricao: 'Habilidades e experiência totalmente alinhadas com o cargo de CEO',
    data_verificacao: '2024-12-01',
    issues: []
  },
  {
    id: '2', 
    tipo: 'Competências Técnicas',
    status: 'aprovado',
    score: 88,
    descricao: 'Competências técnicas adequadas para liderança tecnológica',
    data_verificacao: '2024-12-01',
    issues: [
      'Experiência limitada em blockchain',
      'Certificação em cloud computing pendente'
    ]
  },
  {
    id: '3',
    tipo: 'Adequação Cultural',
    status: 'aprovado',
    score: 92,
    descricao: 'Perfil comportamental alinhado com a cultura organizacional',
    data_verificacao: '2024-12-01',
    issues: []
  },
  {
    id: '4',
    tipo: 'Metas e Objetivos',
    status: 'atenção',
    score: 75,
    descricao: 'Algumas metas apresentam riscos de não cumprimento',
    data_verificacao: '2024-12-01',
    issues: [
      'Meta de Q4 com 65% de progresso',
      'Atraso na entrega do projeto Alpha'
    ]
  }
];

export function AuditoriaSystem() {
  const [selectedEmpresa, setSelectedEmpresa] = useState<string>('1');
  const [selectedPersona, setSelectedPersona] = useState<string>('');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'aprovado':
        return 'bg-green-500';
      case 'atenção':
        return 'bg-yellow-500';
      case 'reprovado':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'aprovado':
        return <CheckCircle2 className="h-4 w-4" />;
      case 'atenção':
        return <AlertTriangle className="h-4 w-4" />;
      case 'reprovado':
        return <XCircle className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 75) return 'text-yellow-600';
    return 'text-red-600';
  };

  const filteredPersonas = mockPersonas;
  const filteredAuditorias = selectedPersona 
    ? mockAuditorias.filter(audit => audit.id !== '4') // Simular filtro por persona
    : mockAuditorias;

  return (
    <div className="w-full">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Sistema de Auditoria</h2>
        <p className="text-gray-600">Monitore a compatibilidade e adequação das personas</p>
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
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900">{empresa.nome}</h4>
                    <p className="text-sm text-gray-600">{empresa.industry}</p>
                  </div>
                  <Badge 
                    variant={empresa.ativa ? "default" : "secondary"}
                    className="text-xs"
                  >
                    {empresa.ativa ? 'Ativa' : 'Inativa'}
                  </Badge>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Score Geral:</span>
                    <span className={`font-semibold ${getScoreColor(empresa.auditoria_score)}`}>
                      {empresa.auditoria_score}%
                    </span>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    <div>{empresa.personas_count} personas</div>
                    <div>Última auditoria: {format(new Date(empresa.last_audit), 'dd/MM', { locale: ptBR })}</div>
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
                  
                  <div className="mt-2 space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">Score:</span>
                      <span className={`font-semibold ${getScoreColor(persona.compatibilidade_score)}`}>
                        {persona.compatibilidade_score}%
                      </span>
                    </div>
                    
                    <div className="flex justify-between text-xs">
                      <span className="text-gray-500">Issues:</span>
                      <Badge 
                        variant={persona.issues_count === 0 ? "default" : "destructive"} 
                        className="text-xs h-4"
                      >
                        {persona.issues_count}
                      </Badge>
                    </div>
                    
                    <div className="text-xs text-gray-500">
                      {format(new Date(persona.last_check), 'dd/MM', { locale: ptBR })}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Coluna 3: Resultados das Auditorias (50%) */}
        <div className="col-span-5 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-gray-600" />
              <h3 className="font-semibold">
                {selectedPersona 
                  ? `Auditoria - ${filteredPersonas.find(p => p.id === selectedPersona)?.nome_completo}` 
                  : 'Auditorias Gerais'
                }
              </h3>
            </div>
            <Button size="sm">
              <RefreshCw className="h-4 w-4 mr-2" />
              Nova Auditoria
            </Button>
          </div>

          <div className="space-y-4">
            {filteredAuditorias.map((auditoria) => (
              <Card key={auditoria.id} className="relative">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="text-lg flex items-center gap-2">
                        {auditoria.tipo}
                        {getStatusIcon(auditoria.status)}
                      </CardTitle>
                      <CardDescription className="mt-1">
                        {auditoria.descricao}
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge 
                        className={`${getStatusColor(auditoria.status)} text-white`}
                      >
                        {auditoria.status}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-3">
                    {/* Score */}
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Pontuação</span>
                        <span className={`font-semibold ${getScoreColor(auditoria.score)}`}>
                          {auditoria.score}%
                        </span>
                      </div>
                      <Progress value={auditoria.score} className="h-2" />
                    </div>

                    {/* Data da verificação */}
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Data da verificação:</span>
                      <span className="font-medium text-gray-900">
                        {format(new Date(auditoria.data_verificacao), 'dd/MM/yyyy', { locale: ptBR })}
                      </span>
                    </div>

                    {/* Issues */}
                    {auditoria.issues && auditoria.issues.length > 0 && (
                      <div>
                        <h5 className="text-sm font-medium text-gray-900 mb-2">
                          Pontos de Atenção:
                        </h5>
                        <ul className="space-y-1">
                          {auditoria.issues.map((issue, index) => (
                            <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                              <AlertTriangle className="h-3 w-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                              {issue}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Status positivo */}
                    {auditoria.issues && auditoria.issues.length === 0 && auditoria.status === 'aprovado' && (
                      <div className="flex items-center gap-2 text-sm text-green-600">
                        <CheckCircle2 className="h-4 w-4" />
                        Nenhum ponto de atenção identificado
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}

            {filteredAuditorias.length === 0 && (
              <div className="text-center py-12">
                <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900">Nenhuma auditoria encontrada</h3>
                <p className="text-gray-600 mt-2">
                  {selectedPersona 
                    ? 'Esta persona ainda não possui auditorias registradas.'
                    : 'Selecione uma empresa para visualizar as auditorias.'
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