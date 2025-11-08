import { useState } from 'react';
import { supabase } from '../lib/supabase';
import { createCompanyClient } from '@/lib/api/multi-db';
import { empresasAPI } from '../lib/api/empresas';
import type { Empresa } from '../types/empresa';

const Diagnostico = () => {
  const [vcmStatus, setVcmStatus] = useState({ status: 'pending', message: '' });
  const [companyStatus, setCompanyStatus] = useState<Record<string, { status: string; message: string }>>({});

  const runDiagnostics = async () => {
    // Test VCM Central Connection
    try {
      const { error } = await supabase.from('empresas_virtuais').select('id').limit(1);
      if (error) throw error;
      setVcmStatus({ status: 'success', message: 'Conexão com VCM Central bem-sucedida!' });

      // Test Company Connections
      const empresas: Empresa[] = await empresasAPI.getAll();
      const companyChecks: Record<string, { status: string; message: string }> = {};

      for (const empresa of empresas) {
        try {
          const companyClient = createCompanyClient(empresa);
          const { error: companyError } = await companyClient.from('personas').select('id').limit(1);
          if (companyError) throw companyError;
          companyChecks[empresa.id] = { status: 'success', message: 'Conexão bem-sucedida.' };
        } catch (e: any) {
          companyChecks[empresa.id] = { status: 'error', message: `Falha: ${e.message}` };
        }
      }
      setCompanyStatus(companyChecks);

    } catch (e: any) {
      setVcmStatus({ status: 'error', message: `Falha ao conectar com VCM Central: ${e.message}` });
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Página de Diagnóstico de Conexão</h1>
      <button onClick={runDiagnostics} className="bg-blue-500 text-white p-2 rounded mb-4">
        Rodar Diagnósticos
      </button>

      <div>
        <h2 className="text-xl font-semibold">VCM Central</h2>
        <p>Status: {vcmStatus.status} - {vcmStatus.message}</p>
      </div>

      <div className="mt-4">
        <h2 className="text-xl font-semibold">Bancos de Dados das Empresas</h2>
        {Object.entries(companyStatus).map(([id, status]) => (
          <div key={id}>
            <p>Empresa ID {id}: {status.status} - {status.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Diagnostico;
