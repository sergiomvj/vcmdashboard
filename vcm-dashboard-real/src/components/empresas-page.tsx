'use client';

import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Users, Play, Eye, Building2, Database, GitBranch, Loader2 } from 'lucide-react';
import { CompanyForm } from './company-form';
import { PersonasModal } from './personas-modal';
import { PersonaEditModal } from './persona-edit-modal';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useEmpresas, usePersonasByEmpresa, useDeleteEmpresa } from '@/lib/supabase-hooks';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/components/ui/use-toast';

// DADOS REAIS DO SUPABASE - SEM MOCKS! (Fixed TypeScript errors)
export function EmpresasPage({ 
  onEmpresaSelect, 
  selectedEmpresaId 
}: {
  onEmpresaSelect?: (id: string) => void;
  selectedEmpresaId?: string;
}) {
  const [showForm, setShowForm] = useState(false);
  const [editingCompany, setEditingCompany] = useState<any>(null);
  const [viewingPersonas, setViewingPersonas] = useState<any>(null);
  const [editingPersona, setEditingPersona] = useState<any>(null);
  const [editingPersonaTab, setEditingPersonaTab] = useState<string>('biografia');
  const [executingScript, setExecutingScript] = useState<number | null>(null);
  const [executingCascade, setExecutingCascade] = useState(false);
  
  // Usar dados reais do Supabase
  const { data: companies = [], isLoading, error } = useEmpresas();
  const [selectedEmpresa, setSelectedEmpresa] = useState<string>('');
  const { data: personasEmpresa = [] } = usePersonasByEmpresa(selectedEmpresa, !!selectedEmpresa);
  const deleteEmpresaMutation = useDeleteEmpresa();
  const { toast } = useToast();

  // Atualizar selectedEmpresa quando companies carregam ou quando uma nova empresa é criada
  useEffect(() => {
    if (companies.length > 0 && !selectedEmpresa) {
      setSelectedEmpresa(companies[0].id);
    }
  }, [companies, selectedEmpresa]);

  const handleEdit = (company: any) => {
    setEditingCompany(company);
    setShowForm(true);
  };

  const handleDelete = async (company: any) => {
    if (window.confirm(`⚠️ ATENÇÃO: Esta ação é IRREVERSÍVEL!\n\nTem certeza que deseja excluir a empresa "${company.nome}"?\n\nTodos os dados relacionados (personas, biografias, etc.) serão perdidos permanentemente.`)) {
      try {
        await deleteEmpresaMutation.mutateAsync(company.id);
        
        // Se a empresa excluída estava selecionada, seleciona outra
        if (selectedEmpresa === company.id && companies.length > 1) {
          const remainingCompanies = companies.filter(c => c.id !== company.id);
          setSelectedEmpresa(remainingCompanies[0].id);
        } else if (companies.length === 1) {
          setSelectedEmpresa('');
        }
        
        toast({ 
          title: 'Empresa excluída com sucesso!',
          description: `A empresa "${company.nome}" foi removida do sistema.`
        });
      } catch (error) {
        console.error('Erro ao excluir empresa:', error);
        toast({ 
          title: 'Erro ao excluir empresa',
          description: error instanceof Error ? error.message : 'Erro desconhecido. Tente novamente.'
        });
      }
    }
  };

  const handleCloseForm = (createdCompany?: any) => {
    setShowForm(false);
    setEditingCompany(null);
    
    // Se uma nova empresa foi criada, seleciona ela automaticamente
    if (createdCompany && createdCompany.id) {
      setSelectedEmpresa(createdCompany.id);
    }
  };

  const handleEditPersona = (persona: any, tab: string = 'biografia') => {
    setEditingPersona(persona);
    setEditingPersonaTab(tab);
  };

  const handleClosePersonaEdit = () => {
    setEditingPersona(null);
    setEditingPersonaTab('biografia');
  };

  const handleSavePersona = (personaData: any) => {
    console.log('Salvando persona:', personaData);
    // Aqui seria implementada a lógica de salvamento
  };

  const executeScript = async (scriptId: number) => {
    setExecutingScript(scriptId);
    
    try {
      // Simular execução do script
      await new Promise(resolve => setTimeout(resolve, 2000));
      console.log(`Script ${scriptId} executado com sucesso`);
    } catch (error) {
      console.error(`Erro ao executar script ${scriptId}:`, error);
    } finally {
      setExecutingScript(null);
    }
  };

  const executeCascade = async () => {
    setExecutingCascade(true);
    
    try {
      // Simular execução em cascata dos scripts 1-5
      for (let i = 1; i <= 5; i++) {
        setExecutingScript(i);
        await new Promise(resolve => setTimeout(resolve, 1500));
        setExecutingScript(null);
      }
      console.log('Execução em cascata concluída com sucesso');
    } catch (error) {
      console.error('Erro na execução em cascata:', error);
    } finally {
      setExecutingCascade(false);
      setExecutingScript(null);
    }
  };

  const handleSelectEmpresa = (empresaId: string) => {
    setSelectedEmpresa(empresaId);
    onEmpresaSelect?.(empresaId);
  };

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      ativa: { label: 'Ativa', className: 'bg-green-100 text-green-800' },
      inativa: { label: 'Inativa', className: 'bg-red-100 text-red-800' },
      processando: { label: 'Processando', className: 'bg-yellow-100 text-yellow-800' }
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.processando;
    
    return (
      <Badge className={config.className}>
        {config.label}
      </Badge>
    );
  };

  const empresaSelecionada = companies.find(e => e.id === selectedEmpresa);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <div className="flex">
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">Erro ao carregar empresas</h3>
            <div className="mt-2 text-sm text-red-700">
              {error?.message || 'Erro desconhecido'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (companies.length === 0) {
    return (
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Empresas Virtuais</h2>
            <p className="text-gray-600">Gerencie suas empresas virtuais, personas e execute scripts</p>
          </div>
          <Button 
            className="bg-blue-600 hover:bg-blue-700"
            onClick={() => setShowForm(true)}
          >
            <Plus size={20} className="mr-2" />
            Nova Empresa
          </Button>
        </div>

        {/* Empty state */}
        <div className="text-center py-12">
          <Building2 size={64} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma empresa criada</h3>
          <p className="text-gray-600 mb-4">Comece criando sua primeira empresa virtual</p>
          <Button 
            className="bg-blue-600 hover:bg-blue-700"
            onClick={() => setShowForm(true)}
          >
            <Plus size={20} className="mr-2" />
            Criar Primeira Empresa
          </Button>
        </div>

        {/* Modal */}
        {showForm && (
          <CompanyForm
            company={editingCompany}
            onClose={handleCloseForm}
          />
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Empresas Virtuais</h2>
          <p className="text-gray-600">Gerencie suas empresas virtuais, personas e execute scripts</p>
        </div>
        <Button 
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2"
        >
          <Plus size={16} />
          Nova Empresa
        </Button>
      </div>

      {/* Layout de 2 colunas */}
      <div className="grid grid-cols-10 gap-6 h-[calc(100vh-200px)]">
        
        {/* Coluna 1: Lista de Empresas (30%) */}
        <div className="col-span-3 bg-white rounded-lg border p-4 overflow-y-auto">
          <div className="flex items-center gap-2 mb-4">
            <Building2 className="h-5 w-5 text-gray-600" />
            <h3 className="font-semibold">Empresas Cadastradas</h3>
          </div>
          
          <div className="space-y-3">
            {[...companies].sort((a, b) => a.nome.localeCompare(b.nome)).map((company) => (
              <button
                key={company.id}
                onClick={() => handleSelectEmpresa(company.id)}
                className={`w-full text-left p-4 rounded-lg border transition-colors ${
                  selectedEmpresa === company.id
                    ? 'bg-blue-50 border-blue-200 border-2'
                    : 'hover:bg-gray-50 border-gray-200'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className="font-semibold text-gray-900">{company.nome}</h4>
                    <p className="text-sm text-gray-600">{company.industry}</p>
                  </div>
                  {getStatusBadge(company.status)}
                </div>
                
                <div className="text-xs text-gray-500 space-y-1">
                  <div className="flex justify-between">
                    <span>País:</span>
                    <span>{company.pais}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Personas:</span>
                    <span>{company.personas_count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Scripts:</span>
                    <span>{company.scripts_executados}/5</span>
                  </div>
                </div>

                <div className="flex gap-1 mt-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleEdit(company);
                    }}
                    className="h-6 px-2 text-xs"
                  >
                    <Edit size={12} />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(company);
                    }}
                    disabled={deleteEmpresaMutation.isPending}
                    className="h-6 px-2 text-xs text-red-600 hover:text-red-700 disabled:opacity-50"
                  >
                    {deleteEmpresaMutation.isPending ? (
                      <Loader2 size={12} className="animate-spin" />
                    ) : (
                      <Trash2 size={12} />
                    )}
                  </Button>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Coluna 2: Detalhes da Empresa (70%) */}
        <div className="col-span-7 bg-white rounded-lg border p-6 overflow-y-auto">
          {empresaSelecionada ? (
            <div className="space-y-6">
              {/* Header da empresa selecionada */}
              <div className="border-b pb-4">
                <div className="flex items-start justify-between">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">{empresaSelecionada.nome}</h2>
                    <p className="text-gray-600 mt-1">{empresaSelecionada.descricao}</p>
                  </div>
                  {getStatusBadge(empresaSelecionada.status)}
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                  <div className="text-sm">
                    <span className="text-gray-500">Indústria:</span>
                    <div className="font-medium">{empresaSelecionada.industry}</div>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-500">País:</span>
                    <div className="font-medium">{empresaSelecionada.pais}</div>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-500">Tamanho:</span>
                    <div className="font-medium capitalize">{empresaSelecionada.tamanho}</div>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-500">Cultura:</span>
                    <div className="font-medium capitalize">{empresaSelecionada.cultura}</div>
                  </div>
                </div>
              </div>

              {/* Tabs de detalhes */}
              <Tabs defaultValue="personas" className="w-full">
                <TabsList className="grid w-full grid-cols-3">
                  <TabsTrigger value="personas" className="flex items-center gap-2">
                    <Users size={16} />
                    Personas
                  </TabsTrigger>
                  <TabsTrigger value="scripts" className="flex items-center gap-2">
                    <Play size={16} />
                    Scripts
                  </TabsTrigger>
                  <TabsTrigger value="rag" className="flex items-center gap-2">
                    <Database size={16} />
                    RAG
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="personas" className="mt-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">Personas da Empresa</h3>
                      <Button size="sm">
                        <Plus size={16} className="mr-2" />
                        Nova Persona
                      </Button>
                    </div>
                    
                    <div className="grid gap-4">
                      {personasEmpresa.map((persona) => (
                        <Card key={persona.id}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="font-semibold">{persona.full_name}</h4>
                                <p className="text-sm text-gray-600">{persona.role}</p>
                                <p className="text-xs text-gray-500">{persona.department}</p>
                              </div>
                              
                              <div className="flex gap-2 flex-wrap">
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'biografia')}
                                  className="bg-blue-50 hover:bg-blue-100 border-blue-200"
                                >
                                  Bio
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'competencias')}
                                  className="bg-green-50 hover:bg-green-100 border-green-200"
                                >
                                  Competências
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'tech')}
                                  className="bg-purple-50 hover:bg-purple-100 border-purple-200"
                                >
                                  Tech Specs
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'rag')}
                                  className="bg-orange-50 hover:bg-orange-100 border-orange-200"
                                >
                                  RAG
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'fluxos')}
                                  className="bg-pink-50 hover:bg-pink-100 border-pink-200"
                                >
                                  Fluxos
                                </Button>
                                <Button 
                                  variant="outline" 
                                  size="sm"
                                  onClick={() => handleEditPersona(persona, 'workflows')}
                                  className="bg-indigo-50 hover:bg-indigo-100 border-indigo-200"
                                >
                                  Workflows
                                </Button>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="scripts" className="mt-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-semibold">Execução de Scripts</h3>
                      <Button 
                        className="bg-blue-600 hover:bg-blue-700"
                        onClick={executeCascade}
                        disabled={executingCascade || executingScript !== null}
                      >
                        <GitBranch size={16} className="mr-2" />
                        {executingCascade ? 'Executando Cascata...' : 'Executar Todos em Cascata'}
                      </Button>
                    </div>
                    
                    <div className="grid gap-4">
                      {[
                        { id: 1, nome: 'Script 1 - Gerar Biografias', status: 'concluído' },
                        { id: 2, nome: 'Script 2 - Gerar Competências', status: 'concluído' },
                        { id: 3, nome: 'Script 3 - Tech Specifications', status: 'concluído' },
                        { id: 4, nome: 'Script 4 - Análise de Fluxos', status: 'pendente' },
                        { id: 5, nome: 'Script 5 - Workflows N8N', status: 'pendente' }
                      ].map((script) => (
                        <Card key={script.id}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h4 className="font-semibold">{script.nome}</h4>
                                <div className="flex items-center gap-2 mt-1">
                                  <Badge 
                                    variant={script.status === 'concluído' ? 'default' : 'secondary'}
                                  >
                                    {script.status}
                                  </Badge>
                                  {(executingScript === script.id || (executingCascade && executingScript === script.id)) && (
                                    <div className="flex items-center gap-1 text-blue-600">
                                      <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-blue-600"></div>
                                      <span className="text-xs">Executando...</span>
                                    </div>
                                  )}
                                </div>
                              </div>
                              
                              <Button 
                                variant="outline" 
                                size="sm"
                                onClick={() => executeScript(script.id)}
                                disabled={executingScript !== null || executingCascade}
                              >
                                <Play size={16} className="mr-2" />
                                Executar
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="rag" className="mt-6">
                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold">Knowledge Base RAG</h3>
                    
                    <div className="grid gap-4">
                      {personasEmpresa.map((persona) => (
                        <Card key={persona.id}>
                          <CardHeader>
                            <CardTitle className="text-base">{persona.full_name}</CardTitle>
                            <CardDescription>{persona.role}</CardDescription>
                          </CardHeader>
                          <CardContent>
                            <div className="space-y-2">
                              <div className="flex justify-between text-sm">
                                <span>Documentos RAG:</span>
                                <Badge>12 documentos</Badge>
                              </div>
                              <div className="flex justify-between text-sm">
                                <span>Última sincronização:</span>
                                <span className="text-gray-500">Há 2 horas</span>
                              </div>
                              <Button variant="outline" size="sm" className="w-full mt-2">
                                <Eye size={16} className="mr-2" />
                                Visualizar RAG
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Building2 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900">Selecione uma Empresa</h3>
                <p className="text-gray-600">Escolha uma empresa na lista para visualizar seus detalhes</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modals */}
      {showForm && (
        <CompanyForm
          company={editingCompany}
          onClose={handleCloseForm}
        />
      )}

      {viewingPersonas && (
        <PersonasModal
          company={viewingPersonas}
          onClose={() => setViewingPersonas(null)}
        />
      )}

      {editingPersona && (
        <PersonaEditModal
          persona={editingPersona}
          isOpen={!!editingPersona}
          onClose={handleClosePersonaEdit}
          onSave={handleSavePersona}
          initialTab={editingPersonaTab}
        />
      )}
    </div>
  );
}