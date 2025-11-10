'use client';

import { Building2, Settings, LayoutDashboard, Target, Shield } from 'lucide-react';

export type TabType = 'dashboard' | 'empresas' | 'objetivos-metas' | 'auditoria' | 'configuracoes';

interface TabNavigationProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export function TabNavigation({ activeTab, onTabChange }: TabNavigationProps) {
  const tabs = [
    {
      id: 'dashboard' as TabType,
      label: 'Dashboard',
      icon: LayoutDashboard,
      description: 'Visão geral e execução de scripts'
    },
    {
      id: 'empresas' as TabType,
      label: 'Empresas',
      icon: Building2,
      description: 'Gerenciar empresas virtuais'
    },
    {
      id: 'objetivos-metas' as TabType,
      label: 'Objetivos & Metas',
      icon: Target,
      description: 'Gerenciar metas globais e por persona'
    },
    {
      id: 'auditoria' as TabType,
      label: 'Auditoria',
      icon: Shield,
      description: 'Sistema de auditoria e compatibilidade'
    },
    {
      id: 'configuracoes' as TabType,
      label: 'Configurações',
      icon: Settings,
      description: 'Configurações do sistema'
    }
  ];

  return (
    <div className="border-b border-gray-200 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            
            return (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={`
                  group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm
                  ${isActive
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon 
                  size={20} 
                  className={`
                    mr-2 
                    ${isActive 
                      ? 'text-blue-500' 
                      : 'text-gray-400 group-hover:text-gray-500'
                    }
                  `} 
                />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}