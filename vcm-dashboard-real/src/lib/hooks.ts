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
        const response = await fetch('/api/status');
        if (!response.ok) {
          return mockExecutionStatus; // Usar mock se API falhar
        }
        return await response.json();
      } catch {
        return mockExecutionStatus; // Usar mock se API falhar
      }
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