'use client';

import { useExecutionStatus } from '@/lib/hooks';
import { CheckCircle, XCircle, Clock, AlertTriangle, Loader2, Activity } from 'lucide-react';

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
      <span style={{color: 'inherit'}}>{label}</span>
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
  const { data: statusData, isLoading, error } = useExecutionStatus();

  // Show loading state
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border p-4">
        <div className="flex items-center gap-2 text-gray-600 mb-3">
          <Activity size={20} />
          <h3 className="font-medium">Status dos Scripts</h3>
        </div>
        <div className="flex items-center justify-center py-8">
          <Loader2 className="animate-spin text-gray-400" size={32} />
          <span className="ml-2 text-gray-500">Carregando status...</span>
        </div>
      </div>
    );
  }

  // Use mock data if no real data available
  const mockData = {
    biografia: { running: false, last_run: null, last_result: 'success' },
    script_1: { running: false, last_run: null, last_result: 'idle' },
    script_2: { running: false, last_run: null, last_result: 'idle' },
    script_3: { running: false, last_run: null, last_result: 'idle' },
    script_4: { running: false, last_run: null, last_result: 'idle' },
    script_5: { running: false, last_run: null, last_result: 'idle' },
    cascade: { running: false, last_run: null, last_result: 'idle' },
  };

  const status = statusData || mockData;

  const getScriptStatus = (script: ScriptStatus): 'running' | 'success' | 'error' | 'idle' | 'pending' => {
    if (script.running) return 'running';
    if (script.last_result === 'success') return 'success';
    if (script.last_result === 'error') return 'error';
    return 'idle';
  };

  return (
    <div className="bg-white rounded-lg border p-4">
      <div className="flex items-center gap-2 text-gray-600 mb-3">
        <Activity size={20} />
        <h3 className="font-medium" style={{color: '#374151'}}>Status dos Scripts</h3>
      </div>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        <StatusBadge
          status={getScriptStatus(status.biografia)}
          label="Biografia"
          lastRun={status.biografia.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.script_1)}
          label="Script 1"
          lastRun={status.script_1.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.script_2)}
          label="Script 2"
          lastRun={status.script_2.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.script_3)}
          label="Script 3"
          lastRun={status.script_3.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.script_4)}
          label="Script 4"
          lastRun={status.script_4.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.script_5)}
          label="Script 5"
          lastRun={status.script_5.last_run}
        />
        <StatusBadge
          status={getScriptStatus(status.cascade)}
          label="Cascata"
          lastRun={status.cascade.last_run}
        />
      </div>

      {error && (
        <div className="mt-3 text-xs text-amber-600 bg-amber-50 p-2 rounded">
          <strong>Modo Desenvolvimento:</strong> Usando dados simulados (API não conectada)
        </div>
      )}

      <div className="mt-3 text-xs text-gray-400">
        Atualização automática a cada 2 segundos
      </div>
    </div>
  );
}