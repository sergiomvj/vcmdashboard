'use client';

import { useHealthCheck } from '@/lib/hooks';
import { StatusPanel } from '@/components/status-panel';
import { BiografiaForm } from '@/components/biografia-form';
import { ScriptControls } from '@/components/script-controls';
import { OutputsPanel } from '@/components/outputs-panel';
import { RAGPanel } from '@/components/rag-panel';
import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';

export default function Dashboard() {
  const { data: healthData, isLoading: healthLoading } = useHealthCheck();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">VCM Dashboard</h1>
              <p className="text-gray-600">Virtual Company Manager - Interface Real</p>
            </div>
            
            <div className="flex items-center gap-3">
              {healthLoading ? (
                <div className="flex items-center gap-2 text-gray-500">
                  <Activity size={20} className="animate-pulse" />
                  <span>Verificando...</span>
                </div>
              ) : healthData ? (
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircle size={20} />
                  <span>API Conectada</span>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-red-600">
                  <AlertTriangle size={20} />
                  <span>API Desconectada</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Coluna Principal */}
          <div className="lg:col-span-2 space-y-8">
            {/* Formulário de Biografias */}
            <BiografiaForm />
            
            {/* Controles de Scripts */}
            <ScriptControls />
            
            {/* Sistema RAG */}
            <RAGPanel />
          </div>
          
          {/* Sidebar */}
          <div className="space-y-8">
            {/* Status Panel */}
            <StatusPanel />
            
            {/* Outputs Panel */}
            <OutputsPanel />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>VCM Dashboard - Interface Real para execução de scripts Python</p>
            <p className="mt-1">
              API Backend: <span className="font-mono">http://localhost:8000</span> | 
              Frontend: <span className="font-mono">http://localhost:3001</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}