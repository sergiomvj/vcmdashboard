'use client';

import { useState } from 'react';
import { useEmpresas, useDeleteEmpresa } from '@/lib/supabase-hooks';
import { Empresa } from '@/lib/supabase';
import { Plus, Edit, Trash2, Users, Play, Eye, Calendar, Building2 } from 'lucide-react';
import { CompanyForm } from './company-form';
import { PersonasModal } from './personas-modal';

export function EmpresasPage({ 
  onEmpresaSelect, 
  selectedEmpresaId 
}: {
  onEmpresaSelect?: (id: string) => void;
  selectedEmpresaId?: string;
}) {
  const [showForm, setShowForm] = useState(false);
  const [editingCompany, setEditingCompany] = useState<Empresa | null>(null);
  const [viewingPersonas, setViewingPersonas] = useState<Empresa | null>(null);
  
  const { data: companies, isLoading, error } = useEmpresas();
  const deleteCompanyMutation = useDeleteEmpresa();

  const handleEdit = (company: Empresa) => {
    setEditingCompany(company);
    setShowForm(true);
  };

  const handleDelete = async (company: Empresa) => {
    if (window.confirm(`Tem certeza que deseja excluir a empresa "${company.nome}"?`)) {
      try {
        await deleteCompanyMutation.mutateAsync(company.id);
      } catch (error) {
        console.error('Erro ao excluir empresa:', error);
        alert('Erro ao excluir empresa. Tente novamente.');
      }
    }
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingCompany(null);
  };

  const handleViewPersonas = (company: Empresa) => {
    setViewingPersonas(company);
  };

  const handleExecuteScripts = (company: Empresa) => {
    // TODO: Integrar com a API para executar scripts para esta empresa específica
    alert(`Executar scripts para: ${company.nome}\n\nEsta funcionalidade será implementada em breve.`);
  };

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      ativa: { label: 'Ativa', className: 'bg-green-100 text-green-800' },
      inativa: { label: 'Inativa', className: 'bg-red-100 text-red-800' },
      processando: { label: 'Processando', className: 'bg-yellow-100 text-yellow-800' }
    };
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.processando;
    
    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${config.className}`}>
        {config.label}
      </span>
    );
  };

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
              {error instanceof Error ? error.message : 'Erro desconhecido'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Empresas Virtuais</h2>
          <p className="text-gray-600">Gerencie suas empresas virtuais e personas</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        >
          <Plus size={20} />
          Nova Empresa
        </button>
      </div>

      {/* Company Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <CompanyForm 
              company={editingCompany}
              onClose={handleCloseForm}
            />
          </div>
        </div>
      )}

      {/* Companies List */}
      {companies && companies.length === 0 ? (
        <div className="text-center py-12">
          <Building2 size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Nenhuma empresa encontrada</h3>
          <p className="text-gray-600 mb-4">Comece criando sua primeira empresa virtual</p>
          <button
            onClick={() => setShowForm(true)}
            className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            <Plus size={20} />
            Criar Primeira Empresa
          </button>
        </div>
      ) : (
        <div className="grid gap-6">
          {companies?.map((company: Empresa) => (
            <div key={company.id} className="bg-white border rounded-lg p-6 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{company.nome}</h3>
                    {getStatusBadge(company.status)}
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{company.industry || 'Indústria não definida'}</p>
                  {company.descricao && (
                    <p className="text-gray-500 text-sm">{company.descricao}</p>
                  )}
                </div>
                
                <div className="flex gap-2">
                  <button
                    onClick={() => handleEdit(company)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-md"
                    title="Editar"
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => handleDelete(company)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-md"
                    title="Excluir"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>

              {/* Company Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <Users size={16} className="text-gray-400" />
                  <span className="text-gray-600">
                    {company.total_personas} personas
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar size={16} className="text-gray-400" />
                  <span className="text-gray-600">
                    {new Date(company.created_at).toLocaleDateString('pt-BR')}
                  </span>
                </div>
                <div className="text-gray-600">
                  CEO: {company.ceo_gender === 'masculino' ? 'Masculino' : 'Feminino'}
                </div>
                <div className="text-gray-600">
                  Equipe: {((company.executives_male || 0) + (company.executives_female || 0) + 
                           (company.assistants_male || 0) + (company.assistants_female || 0) + 
                           (company.specialists_male || 0) + (company.specialists_female || 0))} pessoas
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-2 mt-4 pt-4 border-t">
                {onEmpresaSelect && (
                  <button 
                    onClick={() => onEmpresaSelect(company.id)}
                    className={`flex items-center gap-2 px-3 py-1 text-sm rounded-md transition-colors ${
                      selectedEmpresaId === company.id
                        ? 'bg-purple-100 text-purple-700 border border-purple-300'
                        : 'bg-purple-50 text-purple-700 hover:bg-purple-100'
                    }`}
                  >
                    <Building2 size={14} />
                    {selectedEmpresaId === company.id ? 'Selecionada' : 'Selecionar'}
                  </button>
                )}
                <button 
                  onClick={() => handleViewPersonas(company)}
                  className="flex items-center gap-2 px-3 py-1 text-sm bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors"
                >
                  <Eye size={14} />
                  Ver Personas
                </button>
                <button 
                  onClick={() => handleExecuteScripts(company)}
                  className="flex items-center gap-2 px-3 py-1 text-sm bg-green-50 text-green-700 rounded-md hover:bg-green-100 transition-colors"
                >
                  <Play size={14} />
                  Executar Scripts
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <PersonasModal
        empresa={viewingPersonas}
        isOpen={!!viewingPersonas}
        onClose={() => setViewingPersonas(null)}
      />
    </div>
  );
}