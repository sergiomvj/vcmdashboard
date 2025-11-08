import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Building2, Users, RefreshCw, CheckCircle } from 'lucide-react'

function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard VCM</h1>
        <p className="text-gray-600">Visão geral do sistema Virtual Company Manager</p>
      </div>

      {/* Métricas Principais */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Empresas Virtuais</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">Nenhuma empresa criada ainda</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Personas</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">Aguardando criação de empresas</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Sincronizações</CardTitle>
            <RefreshCw className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">Nenhuma sincronização pendente</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Status Sistema</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">OK</div>
            <p className="text-xs text-muted-foreground">Sistema operacional</p>
          </CardContent>
        </Card>
      </div>

      {/* Área de Boas-vindas */}
      <Card>
        <CardHeader>
          <CardTitle>Bem-vindo ao VCM Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-gray-600">
              Este é o painel de controle do Virtual Company Manager. Aqui você pode:
            </p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• <strong>Criar empresas virtuais</strong> com equipes completas de personas</li>
              <li>• <strong>Executar scripts Python</strong> para gerar biografias e competências</li>
              <li>• <strong>Sincronizar dados</strong> entre o VCM Central e bancos das empresas</li>
              <li>• <strong>Gerenciar workflows N8N</strong> automatizados</li>
              <li>• <strong>Monitorar</strong> o status de todas as operações</li>
            </ul>
            <div className="pt-4">
              <p className="text-sm text-blue-600">
                💡 <strong>Próximo passo:</strong> Acesse a seção "Empresas" para criar sua primeira empresa virtual
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard