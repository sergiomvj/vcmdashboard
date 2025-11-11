'use client';

import { useState } from 'react';
import { useHealthCheck } from '@/lib/hooks';
import { StatusPanel } from '@/components/status-panel';
import { BiografiaForm } from '@/components/biografia-form';
import { ScriptControls } from '@/components/script-controls';
import { OutputsPanel } from '@/components/outputs-panel';
import { RAGPanel } from '@/components/rag-panel';
import { TabNavigation, TabType } from '@/components/tab-navigation';
import { EmpresasPage } from '@/components/empresas-page';
import { ConfiguracoesPage } from '@/components/configuracoes-page';
import { ObjetivosMetas } from '@/components/ObjetivosMetas';
import { AuditoriaSystem } from '@/components/AuditoriaSystem';
import { Activity, AlertTriangle, CheckCircle, Target, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');
  const [selectedEmpresaId, setSelectedEmpresaId] = useState<string>('');
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
              ) : healthData && healthData.status === 'healthy' ? (
                <div className="flex items-center gap-2 text-green-600">
                  <CheckCircle size={20} />
                  <span>API Conectada</span>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-blue-600">
                  <AlertTriangle size={20} />
                  <span>Modo Desenvolvimento</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* API Status Banner */}
      {!healthLoading && (!healthData || healthData.status !== 'healthy') && (
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <AlertTriangle className="h-5 w-5 text-blue-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-blue-800">
                    <strong>Modo Desenvolvimento:</strong> Dashboard funcionando com dados simulados. 
                    Para ativar funcionalidades completas de automação, execute: 
                    <code className="bg-blue-100 px-2 py-1 rounded ml-1 text-blue-900">python api_bridge_real.py</code>
                  </p>
                </div>
              </div>
              <Button 
                variant="outline" 
                size="sm" 
                className="text-blue-700 border-blue-300 hover:bg-blue-100"
                onClick={() => window.location.reload()}
              >
                Tentar Reconectar
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'dashboard' && (
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
        )}

        {activeTab === 'empresas' && (
          <EmpresasPage 
            onEmpresaSelect={setSelectedEmpresaId}
            selectedEmpresaId={selectedEmpresaId}
          />
        )}

        {activeTab === 'objetivos-metas' && (
          <ObjetivosMetas />
        )}

        {activeTab === 'auditoria' && (
          <AuditoriaSystem />
        )}
        
        {activeTab === 'configuracoes' && <ConfiguracoesPage />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="text-center text-gray-500 text-sm">
            <p>VCM Dashboard - Interface Real para execução de scripts Python</p>
            <p className="mt-1">
              Integrated API | 
              Frontend: <span className="font-mono">http://localhost:3001</span>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}