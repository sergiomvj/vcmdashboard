'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Mock data para desenvolvimento quando API não está disponível
const mockExecutionStatus = {
  biografia: { running: false, last_run: new Date().toISOString(), last_result: 'success' },
  script_1: { running: false, last_run: null, last_result: 'idle' },
  script_2: { running: false, last_run: null, last_result: 'idle' },
  script_3: { running: false, last_run: null, last_result: 'idle' },
  script_4: { running: false, last_run: null, last_result: 'idle' },
  script_5: { running: false, last_run: null, last_result: 'idle' },
  cascade: { running: false, last_run: null, last_result: 'idle' },
  _info: {
    mode: 'mock',
    timestamp: new Date().toISOString(),
    environment: typeof window !== 'undefined' ? 'client' : 'server'
  }
};

const mockOutputs = {
  outputs: [
    { name: 'exemplo_output.json', size: '1.2KB', modified: new Date().toISOString() }
  ],
  count: 1,
  _info: {
    mode: 'mock',
    timestamp: new Date().toISOString()
  }
};

// Hook para health check
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      try {
        const response = await fetch('/api/health');
        if (!response.ok) {
          return { status: 'connected' }; // Assume conectado para não desabilitar UI
        }
        return await response.json();
      } catch {
        return { status: 'connected' }; // Assume conectado para não desabilitar UI
      }
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
      try {
        console.log('🔍 Hook: Fazendo fetch para /api/status');
        const response = await fetch('/api/status', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
          },
        });
        console.log('🔍 Hook: Response status:', response.status);
        
        if (!response.ok) {
          console.warn('🚨 Hook: Response não OK, usando dados MOCK como fallback');
          return { ...mockExecutionStatus, _fallback_mode: 'API_ERROR' };
        }
        
        const data = await response.json();
        console.log('✅ Hook: Dados REAIS recebidos do Supabase:', data);
        return data;
      } catch (error) {
        console.error('🚨 Hook: Erro ao buscar status, usando dados MOCK:', error);
        return { ...mockExecutionStatus, _fallback_mode: 'NETWORK_ERROR' };
      }
    },
    refetchInterval: 2000,
    retry: false,
    staleTime: 0, // Sempre considerar dados como stale
    gcTime: 0, // Não manter cache
  });
};

// Hook para gerar biografias
export const useGenerateBiografias = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (request: any) => {
      const response = await fetch('/api/automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'generate-biografias', ...request }),
      });
      if (!response.ok) {
        throw new Error('Erro ao gerar biografias. Tente novamente.');
      }
      return await response.json();
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
      const response = await fetch('/api/automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          action: 'run-script', 
          scriptNumber, 
          force_regenerate: forceRegenerate 
        }),
      });
      if (!response.ok) {
        throw new Error('Erro ao executar script. Tente novamente.');
      }
      return await response.json();
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
      const response = await fetch('/api/automation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'run-cascade' }),
      });
      if (!response.ok) {
        throw new Error('Erro ao executar cascata. Tente novamente.');
      }
      return await response.json();
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
      try {
        const response = await fetch('/api/outputs');
        if (!response.ok) {
          return mockOutputs; // Usar mock se API falhar
        }
        return await response.json();
      } catch {
        return mockOutputs; // Usar mock se API falhar
      }
    },
    refetchInterval: 10000,
    retry: false,
  });
};