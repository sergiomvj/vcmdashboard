'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  Zap, 
  PlayCircle, 
  CheckCircle, 
  AlertCircle,
  Clock,
  ArrowRight 
} from 'lucide-react';

interface CascadeStep {
  id: string;
  name: string;
  script: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  duration?: number;
  output?: string;
}

export function QuickCascadePanel() {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);
  const [steps, setSteps] = useState<CascadeStep[]>([
    { id: '1', name: 'Competências', script: '01_generate_competencias.js', status: 'pending' },
    { id: '2', name: 'Tech Specs', script: '02_generate_tech_specs.js', status: 'pending' },
    { id: '3', name: 'RAG Database', script: '03_generate_rag.js', status: 'pending' },
    { id: '4', name: 'Fluxos', script: '04_generate_fluxos_analise.js', status: 'pending' },
    { id: '5', name: 'Workflows N8N', script: '05_generate_workflows_n8n.js', status: 'pending' }
  ]);

  const runCascade = async () => {
    setIsRunning(true);
    setProgress(0);
    setCurrentStep(0);

    try {
      const response = await fetch('/api/cascade-nodejs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: 'full' })
      });

      if (!response.ok) {
        throw new Error('Erro na execução da cascata');
      }

      // Simula progresso em tempo real
      for (let i = 0; i < steps.length; i++) {
        setCurrentStep(i);
        setProgress(((i + 1) / steps.length) * 100);
        
        // Atualiza status do step atual
        setSteps(prev => prev.map((step, index) => ({
          ...step,
          status: index === i ? 'running' : index < i ? 'completed' : 'pending'
        })));

        // Simula tempo de execução (em produção, seria real)
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Marca como completo
        setSteps(prev => prev.map((step, index) => ({
          ...step,
          status: index <= i ? 'completed' : 'pending'
        })));
      }

      setProgress(100);
    } catch (error) {
      console.error('Erro na cascata:', error);
      setSteps(prev => prev.map((step, index) => ({
        ...step,
        status: index === currentStep ? 'error' : step.status
      })));
    } finally {
      setIsRunning(false);
    }
  };

  const resetCascade = () => {
    setSteps(prev => prev.map(step => ({ ...step, status: 'pending' })));
    setProgress(0);
    setCurrentStep(0);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Clock className="h-4 w-4 animate-pulse text-yellow-500" />;
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <PlayCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  return (
    <Card className="bg-gradient-to-br from-blue-50 to-indigo-100 border-blue-200">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Zap className="h-5 w-5 text-blue-600" />
          <span className="text-blue-900">Execução Rápida - Cascata Completa</span>
        </CardTitle>
        <p className="text-blue-700 text-sm">
          Execute toda a sequência de scripts Node.js (1-5) automaticamente
        </p>
      </CardHeader>
      
      <CardContent>
        {/* Botões de Controle */}
        <div className="flex space-x-3 mb-6">
          <Button
            onClick={runCascade}
            disabled={isRunning}
            className="bg-blue-600 hover:bg-blue-700 text-white flex items-center space-x-2"
          >
            <Zap className="h-4 w-4" />
            <span>{isRunning ? 'Executando...' : 'Executar Cascata'}</span>
          </Button>
          
          {!isRunning && (
            <Button
              variant="outline"
              onClick={resetCascade}
              className="border-blue-300 text-blue-700 hover:bg-blue-50"
            >
              Resetar
            </Button>
          )}
        </div>

        {/* Progress Bar */}
        {isRunning && (
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-900">Progresso Geral</span>
              <span className="text-sm text-blue-600">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2 bg-blue-100" />
          </div>
        )}

        {/* Steps */}
        <div className="space-y-3">
          {steps.map((step, index) => (
            <div
              key={step.id}
              className={`flex items-center justify-between p-3 rounded-lg border transition-all ${
                step.status === 'running' 
                  ? 'bg-yellow-50 border-yellow-200 shadow-md' 
                  : step.status === 'completed'
                  ? 'bg-green-50 border-green-200'
                  : step.status === 'error'
                  ? 'bg-red-50 border-red-200'
                  : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-center space-x-3">
                {getStatusIcon(step.status)}
                <div>
                  <p className="font-medium text-sm">
                    Script {step.id}: {step.name}
                  </p>
                  <p className="text-xs text-gray-500">{step.script}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <Badge 
                  variant="outline" 
                  className={
                    step.status === 'running' ? 'border-yellow-400 text-yellow-700' :
                    step.status === 'completed' ? 'border-green-400 text-green-700' :
                    step.status === 'error' ? 'border-red-400 text-red-700' :
                    'border-gray-400 text-gray-700'
                  }
                >
                  {step.status === 'pending' && 'Aguardando'}
                  {step.status === 'running' && 'Executando'}
                  {step.status === 'completed' && 'Concluído'}
                  {step.status === 'error' && 'Erro'}
                </Badge>
                
                {index < steps.length - 1 && (
                  <ArrowRight className="h-4 w-4 text-gray-400" />
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Status Footer */}
        <div className="mt-6 pt-4 border-t border-blue-200">
          <p className="text-sm text-blue-700 text-center">
            {isRunning ? (
              `Executando Script ${currentStep + 1} de ${steps.length}...`
            ) : progress === 100 ? (
              'Cascata concluída com sucesso! ✨'
            ) : (
              'Pronto para execução da cascata completa'
            )}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}