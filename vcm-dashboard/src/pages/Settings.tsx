import React from 'react'
import { Settings as SettingsIcon, User, Bell, Shield } from 'lucide-react'
import { Card } from '../components/ui/card'

const Settings: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Configurações</h1>
      
      <div className="space-y-6">
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <User className="w-5 h-5 mr-2 text-gray-600" />
            <h2 className="text-lg font-medium text-gray-900">Perfil do Usuário</h2>
          </div>
          <p className="text-gray-600">Gerencie suas informações de perfil e preferências</p>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <Bell className="w-5 h-5 mr-2 text-gray-600" />
            <h2 className="text-lg font-medium text-gray-900">Notificações</h2>
          </div>
          <p className="text-gray-600">Configure suas preferências de notificação</p>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <Shield className="w-5 h-5 mr-2 text-gray-600" />
            <h2 className="text-lg font-medium text-gray-900">Segurança</h2>
          </div>
          <p className="text-gray-600">Gerencie configurações de segurança e privacidade</p>
        </Card>
        
        <Card className="p-6">
          <div className="flex items-center mb-4">
            <SettingsIcon className="w-5 h-5 mr-2 text-gray-600" />
            <h2 className="text-lg font-medium text-gray-900">Sistema</h2>
          </div>
          <p className="text-gray-600">Configurações gerais do sistema</p>
        </Card>
      </div>
    </div>
  )
}

export default Settings