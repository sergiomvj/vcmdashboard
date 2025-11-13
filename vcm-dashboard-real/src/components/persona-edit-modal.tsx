'use client';

import { useState } from 'react';
import { X, Save, User, Brain, Code, Database, GitBranch, Workflow } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';

interface PersonaEditModalProps {
  persona: any;
  isOpen: boolean;
  onClose: () => void;
  onSave?: (personaData: any) => void;
  initialTab?: string;
}

// Mock data para demonstração
const mockPersonaData = {
  biografia: {
    informacoes_pessoais: "Ana Silva, 42 anos, natural de São Paulo...",
    background_profissional: "Mais de 15 anos de experiência em tecnologia...",
    personalidade: "Líder visionária, comunicativa e estratégica...",
    valores: "Inovação, transparência, desenvolvimento de pessoas...",
    hobbies: "Leitura de livros de negócios, corrida, viagens..."
  },
  competencias: {
    tecnicas: [
      { nome: "Gestão Estratégica", nivel: "Avançado" },
      { nome: "Liderança de Equipes", nivel: "Expert" },
      { nome: "Transformação Digital", nivel: "Avançado" },
      { nome: "Análise de Dados", nivel: "Intermediário" }
    ],
    comportamentais: [
      { nome: "Comunicação", nivel: "Expert" },
      { nome: "Pensamento Crítico", nivel: "Avançado" },
      { nome: "Adaptabilidade", nivel: "Avançado" },
      { nome: "Resolução de Problemas", nivel: "Expert" }
    ]
  },
  tech_specs: {
    ferramentas_principais: ["Slack", "Microsoft 365", "Salesforce", "Tableau"],
    sistemas_preferidos: "MacOS, Cloud-first architecture",
    nivel_tecnico: "Intermediário",
    experiencia_digital: "Avançada"
  },
  rag: {
    documentos_processados: 24,
    ultima_atualizacao: "2024-11-15 10:30:00",
    topicos_principais: ["Gestão", "Estratégia", "Inovação", "Liderança"],
    qualidade_embeddings: "Alta"
  },
  fluxos: {
    processos_mapeados: 8,
    workflows_ativo: 5,
    integrações: ["Email", "CRM", "Analytics", "Comunicação"],
    performance: "Otimizada"
  },
  workflows: {
    n8n_workflows: 12,
    automações_ativas: 9,
    triggers_configurados: 15,
    ultima_execucao: "2024-11-15 09:45:00"
  }
};

export function PersonaEditModal({ persona, isOpen, onClose, onSave, initialTab = 'biografia' }: PersonaEditModalProps) {
  const [personaData, setPersonaData] = useState(mockPersonaData);
  const [activeTab, setActiveTab] = useState(initialTab);
  const [hasChanges, setHasChanges] = useState(false);

  const handleSave = () => {
    onSave?.(personaData);
    setHasChanges(false);
    onClose();
  };

  const updateBiografia = (field: string, value: string) => {
    setPersonaData(prev => ({
      ...prev,
      biografia: {
        ...prev.biografia,
        [field]: value
      }
    }));
    setHasChanges(true);
  };

  const updateCompetencia = (tipo: 'tecnicas' | 'comportamentais', index: number, field: string, value: string) => {
    setPersonaData(prev => ({
      ...prev,
      competencias: {
        ...prev.competencias,
        [tipo]: prev.competencias[tipo].map((comp, i) => 
          i === index ? { ...comp, [field]: value } : comp
        )
      }
    }));
    setHasChanges(true);
  };

  if (!persona) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <User className="h-5 w-5" />
            Editar Persona: {persona.nome_completo}
          </DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-hidden">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full flex flex-col">
            <TabsList className="grid w-full grid-cols-6">
              <TabsTrigger value="biografia" className="flex items-center gap-1 text-xs">
                <User size={14} />
                Bio
              </TabsTrigger>
              <TabsTrigger value="competencias" className="flex items-center gap-1 text-xs">
                <Brain size={14} />
                Competências
              </TabsTrigger>
              <TabsTrigger value="tech" className="flex items-center gap-1 text-xs">
                <Code size={14} />
                Tech
              </TabsTrigger>
              <TabsTrigger value="rag" className="flex items-center gap-1 text-xs">
                <Database size={14} />
                RAG
              </TabsTrigger>
              <TabsTrigger value="fluxos" className="flex items-center gap-1 text-xs">
                <GitBranch size={14} />
                Fluxos
              </TabsTrigger>
              <TabsTrigger value="workflows" className="flex items-center gap-1 text-xs">
                <Workflow size={14} />
                Workflows
              </TabsTrigger>
            </TabsList>

            <div className="flex-1 overflow-y-auto mt-4">
              <TabsContent value="biografia" className="space-y-4 mt-0">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="info-pessoais">Informações Pessoais</Label>
                    <Textarea
                      id="info-pessoais"
                      value={personaData.biografia.informacoes_pessoais}
                      onChange={(e) => updateBiografia('informacoes_pessoais', e.target.value)}
                      className="mt-1 min-h-[100px]"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="background">Background Profissional</Label>
                    <Textarea
                      id="background"
                      value={personaData.biografia.background_profissional}
                      onChange={(e) => updateBiografia('background_profissional', e.target.value)}
                      className="mt-1 min-h-[100px]"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="personalidade">Personalidade</Label>
                    <Textarea
                      id="personalidade"
                      value={personaData.biografia.personalidade}
                      onChange={(e) => updateBiografia('personalidade', e.target.value)}
                      className="mt-1 min-h-[80px]"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="valores">Valores</Label>
                    <Textarea
                      id="valores"
                      value={personaData.biografia.valores}
                      onChange={(e) => updateBiografia('valores', e.target.value)}
                      className="mt-1 min-h-[80px]"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="hobbies">Hobbies e Interesses</Label>
                    <Textarea
                      id="hobbies"
                      value={personaData.biografia.hobbies}
                      onChange={(e) => updateBiografia('hobbies', e.target.value)}
                      className="mt-1 min-h-[80px]"
                    />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="competencias" className="space-y-6 mt-0">
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Competências Técnicas</h3>
                    <div className="space-y-3">
                      {personaData.competencias.tecnicas.map((comp, index) => (
                        <div key={index} className="flex gap-3 items-center">
                          <Input
                            value={comp.nome}
                            onChange={(e) => updateCompetencia('tecnicas', index, 'nome', e.target.value)}
                            placeholder="Nome da competência"
                            className="flex-1"
                          />
                          <select
                            value={comp.nivel}
                            onChange={(e) => updateCompetencia('tecnicas', index, 'nivel', e.target.value)}
                            className="px-3 py-2 border rounded-md"
                          >
                            <option value="Básico">Básico</option>
                            <option value="Intermediário">Intermediário</option>
                            <option value="Avançado">Avançado</option>
                            <option value="Expert">Expert</option>
                          </select>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-semibold mb-3">Competências Comportamentais</h3>
                    <div className="space-y-3">
                      {personaData.competencias.comportamentais.map((comp, index) => (
                        <div key={index} className="flex gap-3 items-center">
                          <Input
                            value={comp.nome}
                            onChange={(e) => updateCompetencia('comportamentais', index, 'nome', e.target.value)}
                            placeholder="Nome da competência"
                            className="flex-1"
                          />
                          <select
                            value={comp.nivel}
                            onChange={(e) => updateCompetencia('comportamentais', index, 'nivel', e.target.value)}
                            className="px-3 py-2 border rounded-md"
                          >
                            <option value="Básico">Básico</option>
                            <option value="Intermediário">Intermediário</option>
                            <option value="Avançado">Avançado</option>
                            <option value="Expert">Expert</option>
                          </select>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="tech" className="space-y-4 mt-0">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="ferramentas">Ferramentas Principais</Label>
                    <Input
                      id="ferramentas"
                      value={personaData.tech_specs.ferramentas_principais.join(', ')}
                      onChange={(e) => setPersonaData(prev => ({
                        ...prev,
                        tech_specs: {
                          ...prev.tech_specs,
                          ferramentas_principais: e.target.value.split(', ')
                        }
                      }))}
                      className="mt-1"
                      placeholder="Separar com vírgulas"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="sistemas">Sistemas Preferidos</Label>
                    <Input
                      id="sistemas"
                      value={personaData.tech_specs.sistemas_preferidos}
                      onChange={(e) => setPersonaData(prev => ({
                        ...prev,
                        tech_specs: {
                          ...prev.tech_specs,
                          sistemas_preferidos: e.target.value
                        }
                      }))}
                      className="mt-1"
                    />
                  </div>
                  
                  <div>
                    <Label htmlFor="nivel-tecnico">Nível Técnico</Label>
                    <select
                      id="nivel-tecnico"
                      value={personaData.tech_specs.nivel_tecnico}
                      onChange={(e) => setPersonaData(prev => ({
                        ...prev,
                        tech_specs: {
                          ...prev.tech_specs,
                          nivel_tecnico: e.target.value
                        }
                      }))}
                      className="mt-1 w-full px-3 py-2 border rounded-md"
                    >
                      <option value="Básico">Básico</option>
                      <option value="Intermediário">Intermediário</option>
                      <option value="Avançado">Avançado</option>
                      <option value="Expert">Expert</option>
                    </select>
                  </div>
                  
                  <div>
                    <Label htmlFor="exp-digital">Experiência Digital</Label>
                    <select
                      id="exp-digital"
                      value={personaData.tech_specs.experiencia_digital}
                      onChange={(e) => setPersonaData(prev => ({
                        ...prev,
                        tech_specs: {
                          ...prev.tech_specs,
                          experiencia_digital: e.target.value
                        }
                      }))}
                      className="mt-1 w-full px-3 py-2 border rounded-md"
                    >
                      <option value="Básica">Básica</option>
                      <option value="Intermediária">Intermediária</option>
                      <option value="Avançada">Avançada</option>
                      <option value="Expert">Expert</option>
                    </select>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="rag" className="space-y-4 mt-0">
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">
                        {personaData.rag.documentos_processados}
                      </div>
                      <div className="text-sm text-gray-600">Documentos Processados</div>
                    </div>
                    
                    <div className="bg-green-50 p-4 rounded-lg">
                      <div className="text-sm font-medium text-green-600">
                        {personaData.rag.qualidade_embeddings}
                      </div>
                      <div className="text-sm text-gray-600">Qualidade dos Embeddings</div>
                    </div>
                  </div>
                  
                  <div>
                    <Label>Tópicos Principais</Label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {personaData.rag.topicos_principais.map((topico, index) => (
                        <Badge key={index} variant="outline">{topico}</Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <Label>Última Atualização</Label>
                    <div className="text-sm text-gray-600 mt-1">
                      {new Date(personaData.rag.ultima_atualizacao).toLocaleString('pt-BR')}
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Reprocessar RAG</Button>
                    <Button variant="outline" size="sm">Visualizar Embeddings</Button>
                    <Button variant="outline" size="sm">Exportar Dados</Button>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="fluxos" className="space-y-4 mt-0">
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {personaData.fluxos.processos_mapeados}
                      </div>
                      <div className="text-sm text-gray-600">Processos Mapeados</div>
                    </div>
                    
                    <div className="bg-orange-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">
                        {personaData.fluxos.workflows_ativo}
                      </div>
                      <div className="text-sm text-gray-600">Workflows Ativos</div>
                    </div>
                    
                    <div className="bg-teal-50 p-4 rounded-lg">
                      <div className="text-sm font-medium text-teal-600">
                        {personaData.fluxos.performance}
                      </div>
                      <div className="text-sm text-gray-600">Performance</div>
                    </div>
                  </div>
                  
                  <div>
                    <Label>Integrações Configuradas</Label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {personaData.fluxos.integrações.map((integracao, index) => (
                        <Badge key={index} variant="secondary">{integracao}</Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Analisar Fluxos</Button>
                    <Button variant="outline" size="sm">Otimizar Performance</Button>
                    <Button variant="outline" size="sm">Relatório Detalhado</Button>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="workflows" className="space-y-4 mt-0">
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-indigo-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-indigo-600">
                        {personaData.workflows.n8n_workflows}
                      </div>
                      <div className="text-sm text-gray-600">N8N Workflows</div>
                    </div>
                    
                    <div className="bg-cyan-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-cyan-600">
                        {personaData.workflows.automações_ativas}
                      </div>
                      <div className="text-sm text-gray-600">Automações Ativas</div>
                    </div>
                    
                    <div className="bg-pink-50 p-4 rounded-lg">
                      <div className="text-2xl font-bold text-pink-600">
                        {personaData.workflows.triggers_configurados}
                      </div>
                      <div className="text-sm text-gray-600">Triggers Configurados</div>
                    </div>
                  </div>
                  
                  <div>
                    <Label>Última Execução</Label>
                    <div className="text-sm text-gray-600 mt-1">
                      {new Date(personaData.workflows.ultima_execucao).toLocaleString('pt-BR')}
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm">Executar Workflows</Button>
                    <Button variant="outline" size="sm">Configurar Triggers</Button>
                    <Button variant="outline" size="sm">Logs de Execução</Button>
                    <Button variant="outline" size="sm">Exportar para N8N</Button>
                  </div>
                </div>
              </TabsContent>
            </div>
          </Tabs>
        </div>

        <div className="flex justify-between items-center pt-4 border-t">
          <div className="text-sm text-gray-500">
            {hasChanges && (
              <span className="text-orange-600">• Existem alterações não salvas</span>
            )}
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button onClick={handleSave} disabled={!hasChanges}>
              <Save className="h-4 w-4 mr-2" />
              Salvar Alterações
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}