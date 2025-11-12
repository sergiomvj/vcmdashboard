'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateEmpresa, useUpdateEmpresa } from '@/lib/supabase-hooks';
import { Empresa } from '@/lib/supabase';
import { X, Save, Loader2 } from 'lucide-react';

const companySchema = z.object({
  nome: z.string().min(1, 'Nome é obrigatório'),
  codigo: z.string().min(1, 'Código é obrigatório'),
  industry: z.string().min(1, 'Indústria é obrigatória'),
  dominio: z.string().url('URL inválida').optional().or(z.literal('')),
  descricao: z.string().min(10, 'Descrição deve ter pelo menos 10 caracteres'),
  status: z.enum(['ativa', 'inativa', 'processando']),
  pais: z.string().min(1, 'País é obrigatório'),
  ceo_gender: z.enum(['masculino', 'feminino']),
  executives_male: z.number().min(0).max(10),
  executives_female: z.number().min(0).max(10),
  assistants_male: z.number().min(0).max(10),
  assistants_female: z.number().min(0).max(10),
  specialists_male: z.number().min(0).max(10),
  specialists_female: z.number().min(0).max(10),
  idiomas: z.array(z.string()).optional(),
});

type CompanyFormData = z.infer<typeof companySchema>;

interface CompanyFormProps {
  company?: Empresa | null;
  onClose: () => void;
}

const INDUSTRIES = [
  'tecnologia',
  'saude',
  'educacao',
  'financeiro',
  'servicos',
  'marketing',
  'varejo',
  'consultoria',
  'manufatura',
  'energia',
  'telecomunicacoes'
];

const LANGUAGES = [
  'inglês',
  'espanhol',
  'francês',
  'alemão',
  'italiano',
  'português',
  'chinês',
  'japonês',
  'árabe',
  'russo'
];

export function CompanyForm({ company, onClose }: CompanyFormProps) {
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>(company?.idiomas || []);
  
  const createCompanyMutation = useCreateEmpresa();
  const updateCompanyMutation = useUpdateEmpresa();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch
  } = useForm<CompanyFormData>({
    resolver: zodResolver(companySchema),
    defaultValues: {
      nome: company?.nome || '',
      codigo: company?.codigo || '',
      industry: company?.industria || 'tecnologia',
      dominio: company?.dominio || '',
      descricao: company?.descricao || '',
      status: company?.status || 'ativa',
      pais: company?.pais || 'BR',
      ceo_gender: company?.ceo_gender || 'feminino',
      executives_male: company?.executives_male || 2,
      executives_female: company?.executives_female || 2,
      assistants_male: company?.assistants_male || 2,
      assistants_female: company?.assistants_female || 3,
      specialists_male: company?.specialists_male || 3,
      specialists_female: company?.specialists_female || 3,
      idiomas: company?.idiomas || [],
    }
  });

  const isEditing = !!company;
  const isLoading = createCompanyMutation.isPending || updateCompanyMutation.isPending;

  // Calculate total personas
  const executives_male = watch('executives_male');
  const executives_female = watch('executives_female');
  const assistants_male = watch('assistants_male');
  const assistants_female = watch('assistants_female');
  const specialists_male = watch('specialists_male');
  const specialists_female = watch('specialists_female');
  
  const totalPersonas = executives_male + executives_female + assistants_male + 
                       assistants_female + specialists_male + specialists_female + 1; // +1 for CEO

  const onSubmit = async (data: CompanyFormData) => {
    try {
      console.log('🚀 [FORM] Enviando dados para criação:', data);
      
      if (isEditing && company) {
        // Para edição, usar o hook direto (sem LLM)
        await updateCompanyMutation.mutateAsync({
          id: company.id,
          nome: data.nome,
          codigo: data.codigo,
          industria: data.industry,
          dominio: data.dominio || '',
          descricao: data.descricao,
          pais: data.pais,
          status: data.status,
          idiomas: selectedLanguages,
          total_personas: totalPersonas,
          ceo_gender: data.ceo_gender,
          executives_male: data.executives_male,
          executives_female: data.executives_female,
          assistants_male: data.assistants_male,
          assistants_female: data.assistants_female,
          specialists_male: data.specialists_male,
          specialists_female: data.specialists_female,
        });
        console.log('✅ Empresa atualizada com sucesso');
      } else {
        // Para criação, usar API com LLM
        const response = await fetch('/api/companies/create', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            nome: data.nome,
            codigo: data.codigo,
            industry: data.industry,
            dominio: data.dominio || '',
            descricao: data.descricao,
            pais: data.pais,
            status: data.status,
            idiomas: selectedLanguages,
            ceo_gender: data.ceo_gender,
            executives_male: data.executives_male,
            executives_female: data.executives_female,
            assistants_male: data.assistants_male,
            assistants_female: data.assistants_female,
            specialists_male: data.specialists_male,
            specialists_female: data.specialists_female,
          })
        });
        
        const result = await response.json();
        
        if (!result.success) {
          throw new Error(result.message || 'Erro ao criar empresa');
        }
        
        console.log('✅ Empresa criada com sucesso:', result);
      }
      
      onClose();
    } catch (error) {
      console.error('❌ Erro ao salvar empresa:', error);
      // TODO: Mostrar erro na UI
      alert(`Erro ao salvar empresa: ${error instanceof Error ? error.message : 'Erro desconhecido'}`);
    }
  };

  const toggleLanguage = (language: string) => {
    const newLanguages = selectedLanguages.includes(language)
      ? selectedLanguages.filter(l => l !== language)
      : [...selectedLanguages, language];
    
    setSelectedLanguages(newLanguages);
    setValue('idiomas', newLanguages);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">
          {isEditing ? 'Editar Empresa' : 'Nova Empresa'}
        </h2>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-md"
        >
          <X size={20} />
        </button>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        {/* Basic Information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Nome da Empresa *</label>
            <input
              {...register('nome')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: TechVision Solutions"
            />
            {errors.nome && (
              <p className="text-red-500 text-sm mt-1">{errors.nome.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Código *</label>
            <input
              {...register('codigo')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: TECH001"
              disabled={isEditing} // Don't allow editing code
            />
            {errors.codigo && (
              <p className="text-red-500 text-sm mt-1">{errors.codigo.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Domínio da Empresa</label>
            <input
              {...register('dominio')}
              type="url"
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Ex: https://empresa.com"
            />
            {errors.dominio && (
              <p className="text-red-500 text-sm mt-1">{errors.dominio.message}</p>
            )}
          </div>
        </div>

        {/* Descrição da empresa */}
        <div>
          <label className="block text-sm font-medium mb-1">Descrição da Empresa *</label>
          <textarea
            {...register('descricao')}
            rows={3}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Descreva o negócio, missão e principais atividades da empresa..."
          />
          {errors.descricao && (
            <p className="text-red-500 text-sm mt-1">{errors.descricao.message}</p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Indústria *</label>
            <select
              {...register('industry')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {INDUSTRIES.map(industry => (
                <option key={industry} value={industry}>
                  {industry.charAt(0).toUpperCase() + industry.slice(1)}
                </option>
              ))}
            </select>
            {errors.industry && (
              <p className="text-red-500 text-sm mt-1">{errors.industry.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">País *</label>
            <select
              {...register('pais')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="BR">Brasil</option>
              <option value="US">Estados Unidos</option>
              <option value="CA">Canadá</option>
              <option value="MX">México</option>
              <option value="AR">Argentina</option>
              <option value="ES">Espanha</option>
              <option value="PT">Portugal</option>
            </select>
            {errors.pais && (
              <p className="text-red-500 text-sm mt-1">{errors.pais.message}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Status</label>
            <select
              {...register('status')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="ativa">Ativa</option>
              <option value="inativa">Inativa</option>
              <option value="processando">Processando</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Gênero do CEO</label>
            <select
              {...register('ceo_gender')}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="feminino">Feminino</option>
              <option value="masculino">Masculino</option>
            </select>
          </div>
        </div>

        {/* Team Distribution */}
        <div>
          <h3 className="text-lg font-medium mb-4">Distribuição da Equipe</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Executivos (H)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('executives_male', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Executivos (M)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('executives_female', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Assistentes (H)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('assistants_male', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Assistentes (M)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('assistants_female', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Especialistas (H)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('specialists_male', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Especialistas (M)</label>
              <input
                type="number"
                min="0"
                max="10"
                {...register('specialists_female', { valueAsNumber: true })}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            Total de personas: <span className="font-medium">{totalPersonas}</span> (incluindo CEO)
          </div>
        </div>

        {/* Languages */}
        <div>
          <label className="block text-sm font-medium mb-2">Idiomas Extras</label>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
            {LANGUAGES.map(language => (
              <label key={language} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={selectedLanguages.includes(language)}
                  onChange={() => toggleLanguage(language)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm">{language}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Buttons */}
        <div className="flex gap-3 pt-4 border-t">
          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 size={20} className="animate-spin" />
            ) : (
              <Save size={20} />
            )}
            {isLoading ? 'Salvando...' : 'Salvar'}
          </button>
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}