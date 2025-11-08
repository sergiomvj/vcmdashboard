export const empresasAPI = {
  // Buscar todas as empresas
  getAll: async (): Promise<Empresa[]> => {
    const { data, error } = await supabase
      .from('empresas')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  // Buscar empresa por ID
  getById: async (id: string): Promise<Empresa> => {
    const { data, error } = await supabase
      .from('empresas')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data
  },

  // Buscar empresa por código
  getByCodigo: async (codigo: string): Promise<Empresa> => {
    const { data, error } = await supabase
      .from('empresas')
      .select('*')
      .eq('codigo', codigo)
      .single()

    if (error) throw error
    return data
  },

  // Criar nova empresa
  create: async (empresa: CreateEmpresa): Promise<Empresa> => {
    const { data, error } = await supabase
      .from('empresas')
      .insert({
        ...empresa,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Atualizar empresa
  update: async (id: string, empresa: UpdateEmpresa): Promise<Empresa> => {
    const { data, error } = await supabase
      .from('empresas')
      .update({
        ...empresa,
        updated_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Deletar empresa
  delete: async (id: string): Promise<void> => {
    const { error } = await supabase
      .from('empresas')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Atualizar status dos scripts
  updateScriptsStatus: async (id: string, scriptsStatus: Partial<Empresa['scripts_status']>): Promise<Empresa> => {
    const { data: currentEmpresa } = await supabase
      .from('empresas')
      .select('scripts_status')
      .eq('id', id)
      .single()

    const updatedScriptsStatus = {
      ...currentEmpresa?.scripts_status,
      ...scriptsStatus
    }

    const { data, error } = await supabase
      .from('empresas')
      .update({
        scripts_status: updatedScriptsStatus,
        updated_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Buscar empresas com estatísticas
  getWithStats: async (): Promise<(Empresa & { 
    personas_count: number
    active_workflows: number
    last_sync?: string 
  })[]> => {
    const { data, error } = await supabase
      .from('empresas')
      .select(`
        *,
        personas(count),
        workflows(count)
      `)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  }
}