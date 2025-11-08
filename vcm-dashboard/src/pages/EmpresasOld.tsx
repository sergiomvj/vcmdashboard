import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Plus, Building2 } from 'lucide-react';

function EmpresasOld() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Empresas Virtuais</h1>
          <p className="text-gray-600">Gerencie suas empresas virtuais e suas equipes</p>
        </div>
        <Button className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Nova Empresa
        </Button>
      </div>

      {/* Estado vazio */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building2 className="h-5 w-5" />
            Suas Empresas Virtuais
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-12">
            <Building2 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma empresa virtual criada ainda
            </h3>
            <p className="text-gray-600 mb-6 max-w-md mx-auto">
              Crie sua primeira empresa virtual para começar a usar o sistema VCM. 
              Cada empresa terá sua própria equipe de 20 personas geradas automaticamente.
            </p>
            <Button className="flex items-center gap-2 mx-auto">
              <Plus className="h-4 w-4" />
              Criar Primeira Empresa
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Informações sobre Scripts Python */}
      <Card>
        <CardHeader>
          <CardTitle>🐍 Integração com Scripts Python</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-gray-600">
              O sistema utiliza os scripts Python existentes para gerar as empresas virtuais:
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-medium text-blue-900 mb-2">Scripts de Geração</h4>
                <ul className="text-sm text-blue-700 space-y-1">
                  <li>• 01_virtual_company_generator.py</li>
                  <li>• 05_auto_biografia_generator.py</li>
                </ul>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-900 mb-2">Scripts de Processamento</h4>
                <ul className="text-sm text-green-700 space-y-1">
                  <li>• 01_generate_competencias.py</li>
                  <li>• 02_generate_tech_specs.py</li>
                  <li>• 03_generate_rag.py</li>
                  <li>• 04_generate_fluxos_analise.py</li>
                  <li>• 05_generate_workflows_n8n.py</li>
                </ul>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default EmpresasOld;