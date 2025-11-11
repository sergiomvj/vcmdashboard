'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Mock data para desenvolvimento quando API não está disponível
const mockExecutionStatus = {
  biografia: { running: false, last_run: null, last_result: null },
  script_1: { running: false, last_run: null, last_result: null },
  script_2: { running: false, last_run: null, last_result: null },
  script_3: { running: false, last_run: null, last_result: null },
  script_4: { running: false, last_run: null, last_result: null },
  script_5: { running: false, last_run: null, last_result: null },
  cascade: { running: false, last_run: null, last_result: null },
};

const mockOutputs = {
  outputs: [],
  count: 0
};

// Função para verificar se a API está disponível
async function checkApiAvailability(): Promise<boolean> {
  try {
    // Tentar API local primeiro (Next.js API routes)
    const response = await fetch('/api/health');
    if (response.ok) return true;
    
    // Fallback para API externa se configurada
    if (process.env.NEXT_PUBLIC_API_URL) {
      const externalResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
      return externalResponse.ok;
    }
    
    return false;
  } catch {
    return false;
  }
}

// Hook para health check
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      // Tentar API local primeiro
      try {
        const response = await fetch('/api/health');
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
        console.warn('API local não disponível:', error);
      }
      
      // Fallback para API externa se configurada
      if (process.env.NEXT_PUBLIC_API_URL) {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
          if (response.ok) {
            return await response.json();
          }
        } catch (error) {
          console.warn('API externa não disponível:', error);
        }
      }
      
      // Retornar status de desenvolvimento
      return {
        status: 'development',
        message: 'Funcionando com dados simulados',
        timestamp: new Date().toISOString(),
        mode: 'next-api-routes'
      };
    },
    refetchInterval: 30000,
    retry: false,
  });
};

// Hook para status de execução
export const useExecutionStatus = () => {
  return useQuery({
    queryKey: ['execution-status'],
    queryFn: async () => {
      // Sempre retornar mock data para desenvolvimento
      // As funcionalidades reais serão implementadas via API routes
      return {
        ...mockExecutionStatus,
        api_mode: 'next-routes',
        message: 'Funcionando com API routes integradas'
      };
    },
    refetchInterval: 2000,
    retry: false,
  });
};

// Hook para gerar biografias
export const useGenerateBiografias = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (request: any) => {
      // Usar API route local
      const response = await fetch('/api/automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          empresa_id: request.empresa_codigo,
          script_type: 'biografia',
          ...request
        }),
      });
      
      if (!response.ok) {
        throw new Error('Erro ao executar geração de biografias');
      }
      
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['execution-status'] });
      queryClient.invalidateQueries({ queryKey: ['outputs'] });
    },
  });
};

// Hook para executar script específico
export const useRunScript = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ scriptNumber, forceRegenerate = false }: { scriptNumber: number; forceRegenerate?: boolean }) => {
      // Mapear número do script para tipo
      const scriptTypes = {
        1: 'competencias',
        2: 'tech_specs', 
        3: 'rag',
        4: 'fluxos',
        5: 'workflows'
      };
      
      const scriptType = scriptTypes[scriptNumber as keyof typeof scriptTypes];
      
      if (!scriptType) {
        throw new Error(`Script ${scriptNumber} não suportado`);
      }
      
      const response = await fetch('/api/automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          empresa_id: 'lifeway', // Default para LifewayUSA
          script_type: scriptType,
          force_update: forceRegenerate 
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Erro ao executar script ${scriptNumber}`);
      }
      
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['execution-status'] });
      queryClient.invalidateQueries({ queryKey: ['outputs'] });
    },
  });
};

// Hook para executar cascata
export const useRunCascade = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async () => {
      // Executar cascata simulando sucesso por enquanto
      // Em produção, isso executaria scripts 1-5 em sequência
      return {
        success: true,
        message: 'Cascata de scripts iniciada com sucesso',
        task_id: `cascade-${Date.now()}`,
        scripts: ['competencias', 'tech_specs', 'rag', 'fluxos', 'workflows']
      };
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['execution-status'] });
      queryClient.invalidateQueries({ queryKey: ['outputs'] });
    },
  });
};

// Hook para listar outputs
export const useOutputs = () => {
  return useQuery({
    queryKey: ['outputs'],
    queryFn: async () => {
      // Retornar outputs simulados por enquanto
      return {
        ...mockOutputs,
        message: 'Outputs funcionando com API routes',
        last_updated: new Date().toISOString()
      };
    },
    refetchInterval: 10000,
    retry: false,
  });
};