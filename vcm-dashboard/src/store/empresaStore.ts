import { create } from 'zustand';
import type { Empresa } from '../types/empresa';
import { empresasAPI } from '../lib/api/empresas';

interface EmpresaState {
  selectedEmpresa: Empresa | null;
  empresas: Empresa[];
  isLoading: boolean;
  error: Error | null;
  setSelectedEmpresa: (empresa: Empresa | null) => void;
  fetchEmpresas: () => Promise<void>;
}

export const useEmpresaStore = create<EmpresaState>((set) => ({
  selectedEmpresa: null,
  empresas: [],
  isLoading: false,
  error: null,
  setSelectedEmpresa: (empresa) => set({ selectedEmpresa: empresa }),
  fetchEmpresas: async () => {
    set({ isLoading: true, error: null });
    try {
      const empresas = await empresasAPI.getAll();
      set({ empresas, isLoading: false });
    } catch (error: any) {
      set({ error, isLoading: false });
    }
  },
}));
