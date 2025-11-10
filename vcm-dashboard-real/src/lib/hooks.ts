'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient, BiografiaRequest } from './api';

// Hook para health check
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => apiClient.healthCheck(),
    refetchInterval: 30000, // 30 segundos
  });
};

// Hook para status de execução
export const useExecutionStatus = () => {
  return useQuery({
    queryKey: ['execution-status'],
    queryFn: () => apiClient.getStatus(),
    refetchInterval: 2000, // 2 segundos para monitoramento em tempo real
  });
};

// Hook para gerar biografias
export const useGenerateBiografias = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (request: BiografiaRequest) => apiClient.generateBiografias(request),
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
    mutationFn: ({ scriptNumber, forceRegenerate = false }: { scriptNumber: number; forceRegenerate?: boolean }) =>
      apiClient.runScript(scriptNumber, forceRegenerate),
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
    mutationFn: () => apiClient.runCascade(),
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
    queryFn: () => apiClient.listOutputs(),
    refetchInterval: 10000, // 10 segundos
  });
};