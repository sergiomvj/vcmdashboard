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
      
      <div className="space-y-4">
        {/* Gerador de Biografias */}
        {execution_status.biografia && (
          <div className="bg-blue-50 rounded-lg p-3">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-sm">Gerador de Biografias</h4>
                <p className="text-xs text-gray-600">Script 0 - Criação das personas base</p>
              </div>
              <StatusBadge
                status={getStatus(execution_status.biografia)}
                label={execution_status.biografia.running ? 'Executando' : 
                       execution_status.biografia.last_result === 'success' ? 'Concluído' :
                       execution_status.biografia.last_result === 'error' ? 'Erro' : 'Aguardando'}
                lastRun={execution_status.biografia.last_run}
              />
            </div>
          </div>
        )}

        {/* Scripts de Processamento */}
        <div className="bg-gray-50 rounded-lg p-3">
          <h4 className="font-medium mb-3 text-sm text-gray-700">Pipeline de Processamento</h4>
          <div className="space-y-2">
            {[1, 2, 3, 4, 5].map((num) => {
              const scriptKey = `script_${num}` as keyof typeof execution_status;
              const scriptStatus = execution_status[scriptKey];
              const scriptInfo = {
                1: { name: 'Competências', desc: 'Análise de habilidades técnicas e comportamentais' },
                2: { name: 'Tech Specs', desc: 'Especificações técnicas e ferramentas' },
                3: { name: 'RAG Database', desc: 'Base de conhecimento estruturada' },
                4: { name: 'Fluxos de Análise', desc: 'Mapeamento de processos de negócio' },
                5: { name: 'Workflows N8N', desc: 'Automações para execução prática' }
              };

              if (!scriptStatus) return null;

              return (
                <div key={num} className="bg-white rounded-lg p-3 border">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono text-gray-500">Script {num}</span>
                        <span className="font-medium text-sm">{scriptInfo[num as keyof typeof scriptInfo].name}</span>
                      </div>
                      <p className="text-xs text-gray-600 mt-1">{scriptInfo[num as keyof typeof scriptInfo].desc}</p>
                    </div>
                    <StatusBadge
                      status={getStatus(scriptStatus)}
                      label={scriptStatus.running ? 'Executando' : 
                             scriptStatus.last_result === 'success' ? 'OK' :
                             scriptStatus.last_result === 'error' ? 'Erro' : 'Aguardando'}
                      lastRun={scriptStatus.last_run}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Status Geral */}
        {execution_status.cascade && (
          <div className="bg-green-50 rounded-lg p-3">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium text-sm">Status Geral do Sistema</h4>
                <p className="text-xs text-gray-600">Execução completa da cascata de scripts</p>
              </div>
              <StatusBadge
                status={getStatus(execution_status.cascade)}
                label={execution_status.cascade.running ? 'Executando' : 
                       execution_status.cascade.last_result === 'success' ? 'Completo' :
                       execution_status.cascade.last_result === 'error' ? 'Erro' : 'Pendente'}
                lastRun={execution_status.cascade.last_run}
              />
            </div>
          </div>
        )}
      </div>

      <div className="mt-4 text-xs text-gray-500 border-t pt-3">
        <div className="flex justify-between">
          <span>Última atualização:</span>
          <span>{(statusData as any).timestamp ? new Date((statusData as any).timestamp).toLocaleString() : 'Dados locais'}</span>
        </div>
      </div>
    </div>
  );
}