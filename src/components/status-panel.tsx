'use client';

import { useExecutionStatus } from '@/lib/hooks';
import { CheckCircle, XCircle, Clock, AlertTriangle, Loader2 } from 'lucide-react';

interface StatusBadgeProps {
  status: 'running' | 'success' | 'error' | 'idle' | 'pending';
  label: string;
  lastRun?: string | null;
}

function StatusBadge({ status, label, lastRun }: StatusBadgeProps) {
  const getStatusInfo = () => {
    switch (status) {
      case 'running':
        return { icon: Loader2, color: 'text-blue-600 bg-blue-100', spin: true };
      case 'success':
        return { icon: CheckCircle, color: 'text-green-600 bg-green-100', spin: false };
      case 'error':
        return { icon: XCircle, color: 'text-red-600 bg-red-100', spin: false };
      case 'pending':
        return { icon: Clock, color: 'text-yellow-600 bg-yellow-100', spin: false };
      default:
        return { icon: AlertTriangle, color: 'text-gray-600 bg-gray-100', spin: false };
    }
  };

  const { icon: Icon, color, spin } = getStatusInfo();

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${color}`}>
      <Icon size={16} className={spin ? 'animate-spin' : ''} />
      <span>{label}</span>
      {lastRun && (
        <span className="text-xs opacity-75">
          {new Date(lastRun).toLocaleTimeString()}
        </span>
      )}
    </div>
  );
}

interface ScriptStatus {
  running: boolean;
  last_result?: string | null;
  last_run?: string | null;
}

export function StatusPanel() {
  const { data: statusData, isLoading } = useExecutionStatus();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-lg font-semibold mb-4">Status dos Scripts</h3>
        <div className="flex items-center gap-2">
          <Loader2 size={20} className="animate-spin" />
          <span>Carregando status...</span>
        </div>
      </div>
    );
  }

  if (!statusData) {
    return (
      <div className="bg-white rounded-lg border p-6">
        <h3 className="text-lg font-semibold mb-4">Status dos Scripts</h3>
        <div className="text-red-600">Erro ao carregar status</div>
      </div>
    );
  }

  // Compatibilidade: se os dados vêm diretamente ou aninhados em execution_status
  const execution_status = statusData.execution_status || statusData;

  const getStatus = (scriptStatus: ScriptStatus) => {
    if (scriptStatus.running) return 'running';
    if (scriptStatus.last_result === 'success') return 'success';
    if (scriptStatus.last_result === 'error') return 'error';
    return 'idle';
  };

  return (
    <div className="bg-white rounded-lg border p-6">
      <h3 className="text-lg font-semibold mb-4">Status dos Scripts</h3>
      
      <div className="space-y-3">
        {execution_status.biografia && (
          <div className="flex items-center justify-between">
            <span className="font-medium">Gerador de Biografias</span>
            <StatusBadge
              status={getStatus(execution_status.biografia)}
              label={execution_status.biografia.running ? 'Executando' : 
                     execution_status.biografia.last_result === 'success' ? 'Concluído' :
                     execution_status.biografia.last_result === 'error' ? 'Erro' : 'Aguardando'}
              lastRun={execution_status.biografia.last_run}
            />
          </div>
        )}

        <div className="border-t pt-3">
          <h4 className="font-medium mb-2">Scripts de Processamento</h4>
          {[1, 2, 3, 4, 5].map((num) => {
            const scriptKey = `script_${num}` as keyof typeof execution_status;
            const scriptStatus = execution_status[scriptKey];
            const scriptNames = {
              1: 'Competências',
              2: 'Tech Specs',
              3: 'RAG Database',
              4: 'Fluxos de Análise',
              5: 'Workflows N8N'
            };

            if (!scriptStatus) return null;

            return (
              <div key={num} className="flex items-center justify-between py-1">
                <span className="text-sm">Script {num}: {scriptNames[num as keyof typeof scriptNames]}</span>
                <StatusBadge
                  status={getStatus(scriptStatus)}
                  label={scriptStatus.running ? 'Executando' : 
                         scriptStatus.last_result === 'success' ? 'OK' :
                         scriptStatus.last_result === 'error' ? 'Erro' : 'Aguardando'}
                  lastRun={scriptStatus.last_run}
                />
              </div>
            );
          })}
        </div>

        {execution_status.cascade && (
          <div className="border-t pt-3">
            <div className="flex items-center justify-between">
              <span className="font-medium">Cascata Completa</span>
              <StatusBadge
                status={getStatus(execution_status.cascade)}
                label={execution_status.cascade.running ? 'Executando' : 
                       execution_status.cascade.last_result === 'success' ? 'Concluída' :
                       execution_status.cascade.last_result === 'error' ? 'Erro' : 'Aguardando'}
                lastRun={execution_status.cascade.last_run}
              />
            </div>
          </div>
        )}
      </div>

      <div className="mt-4 text-xs text-gray-500">
        Última atualização: {statusData.timestamp ? new Date(statusData.timestamp).toLocaleString() : 'Dados locais'}
      </div>
    </div>
  );
}