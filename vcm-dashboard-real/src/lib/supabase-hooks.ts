import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase, Empresa, SystemConfiguration, Persona, TABLES } from './supabase';

// =====================
// EMPRESAS HOOKS (using existing table)
// =====================

export const useEmpresas = () => {
  return useQuery({
    queryKey: ['empresas'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from(TABLES.EMPRESAS)
        .select('*')
        .order('created_at', { ascending: false });
      
      if (error) throw error;
      return data as Empresa[];
    },
  });
};

export const useEmpresa = (id: string) => {
  return useQuery({
    queryKey: ['empresa', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from(TABLES.EMPRESAS)
        .select('*')
        .eq('id', id)
        .single();
      
      if (error) throw error;
      return data as Empresa;
    },
    enabled: !!id,
  });
};

export const useCreateEmpresa = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (empresa: Partial<Empresa>) => {
      // Generate codigo if not provided
      const codigo = empresa.codigo || `EMP_${Date.now()}`;
      
      const { data, error } = await supabase
        .from(TABLES.EMPRESAS)
        .insert([{
          ...empresa,
          codigo,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }])
        .select()
        .single();
      
      if (error) throw error;
      return data as Empresa;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['empresas'] });
    },
  });
};

export const useUpdateEmpresa = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, ...updates }: Partial<Empresa> & { id: string }) => {
      const { data, error } = await supabase
        .from(TABLES.EMPRESAS)
        .update({
          ...updates,
          updated_at: new Date().toISOString(),
        })
        .eq('id', id)
        .select()
        .single();
      
      if (error) throw error;
      return data as Empresa;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['empresas'] });
      queryClient.invalidateQueries({ queryKey: ['empresa', data.id] });
    },
  });
};

export const useDeleteEmpresa = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase
        .from(TABLES.EMPRESAS)
        .delete()
        .eq('id', id);
      
      if (error) throw error;
      return id;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['empresas'] });
    },
  });
};

// =====================
// CONFIGURATIONS HOOKS
// =====================

export const useConfigurations = (category?: string) => {
  return useQuery({
    queryKey: ['configurations', category],
    queryFn: async () => {
      let query = supabase
        .from(TABLES.CONFIGURATIONS)
        .select('*')
        .order('category', { ascending: true })
        .order('key', { ascending: true });
      
      if (category) {
        query = query.eq('category', category);
      }
      
      const { data, error } = await query;
      
      if (error) throw error;
      return data as SystemConfiguration[];
    },
  });
};

export const useConfiguration = (id: string) => {
  return useQuery({
    queryKey: ['configuration', id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from(TABLES.CONFIGURATIONS)
        .select('*')
        .eq('id', id)
        .single();
      
      if (error) throw error;
      return data as SystemConfiguration;
    },
    enabled: !!id,
  });
};

export const useCreateConfiguration = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (config: Omit<SystemConfiguration, 'id' | 'created_at' | 'updated_at'>) => {
      const { data, error } = await supabase
        .from(TABLES.CONFIGURATIONS)
        .insert([{
          ...config,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }])
        .select()
        .single();
      
      if (error) throw error;
      return data as SystemConfiguration;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['configurations'] });
    },
  });
};

export const useUpdateConfiguration = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, ...updates }: Partial<SystemConfiguration> & { id: string }) => {
      const { data, error } = await supabase
        .from(TABLES.CONFIGURATIONS)
        .update({
          ...updates,
          updated_at: new Date().toISOString(),
        })
        .eq('id', id)
        .select()
        .single();
      
      if (error) throw error;
      return data as SystemConfiguration;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['configurations'] });
      queryClient.invalidateQueries({ queryKey: ['configuration', data.id] });
    },
  });
};

export const useDeleteConfiguration = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase
        .from(TABLES.CONFIGURATIONS)
        .delete()
        .eq('id', id);
      
      if (error) throw error;
      return id;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['configurations'] });
    },
  });
};

// =====================
// PERSONAS HOOKS (for empresa management)
// =====================

export const useEmpresaPersonas = (empresaId: string) => {
  return useQuery({
    queryKey: ['personas', empresaId],
    queryFn: async () => {
      const { data, error } = await supabase
        .from(TABLES.PERSONAS)
        .select('*')
        .eq('empresa_id', empresaId)
        .order('full_name', { ascending: true });
      
      if (error) throw error;
      return data as Persona[];
    },
    enabled: !!empresaId,
  });
};

export const usePersonasByEmpresa = (empresaId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: ['personas', empresaId],
    queryFn: async () => {
      if (!empresaId) return [];
      
      const { data, error } = await supabase
        .from(TABLES.PERSONAS)
        .select('*')
        .eq('empresa_id', empresaId)
        .order('full_name', { ascending: true });
      
      if (error) throw error;
      return data as Persona[];
    },
    enabled: enabled && !!empresaId,
  });
};

// Legacy hooks for backward compatibility (mapping to new names)
export const useCompanies = useEmpresas;
export const useCompany = useEmpresa;
export const useCreateCompany = useCreateEmpresa;
export const useUpdateCompany = useUpdateEmpresa;
export const useDeleteCompany = useDeleteEmpresa;
export const useCompanyPersonas = useEmpresaPersonas;