export const personasAPI = {
  // Buscar todas as personas
  getAll: async (): Promise<Persona[]> => {
    const { data, error } = await supabase
      .from('personas')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  // Buscar personas por empresa
  getByEmpresa: async (empresaId: string): Promise<Persona[]> => {
    const { data, error } = await supabase
      .from('personas')
      .select('*')
      .eq('empresa_id', empresaId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  // Buscar persona por ID
  getById: async (id: string): Promise<Persona> => {
    const { data, error } = await supabase
      .from('personas')
      .select('*')
      .eq('id', id)
      .single()

    if (error) throw error
    return data
  },

  // Buscar persona por código
  getByCode: async (personaCode: string): Promise<Persona> => {
    const { data, error } = await supabase
      .from('personas')
      .select('*')
      .eq('persona_code', personaCode)
      .single()

    if (error) throw error
    return data
  },

  // Criar nova persona
  create: async (persona: CreatePersona): Promise<Persona> => {
    const { data, error } = await supabase
      .from('personas')
      .insert({
        ...persona,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        last_sync: new Date().toISOString()
      })
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Atualizar persona
  update: async (id: string, persona: UpdatePersona): Promise<Persona> => {
    const { data, error } = await supabase
      .from('personas')
      .update({
        ...persona,
        updated_at: new Date().toISOString()
      })
      .eq('id', id)
      .select()
      .single()

    if (error) throw error
    return data
  },

  // Deletar persona
  delete: async (id: string): Promise<void> => {
    const { error } = await supabase
      .from('personas')
      .delete()
      .eq('id', id)

    if (error) throw error
  },

  // Buscar personas com competências e workflows
  getWithDetails: async (empresaId?: string): Promise<(Persona & {
    competencias_count: number
    workflows_count: number
    rag_knowledge_count: number
  })[]> => {
    let query = supabase
      .from('personas')
      .select(`
        *,
        competencias(count),
        workflows(count),
        rag_knowledge(count)
      `)

    if (empresaId) {
      query = query.eq('empresa_id', empresaId)
    }

    const { data, error } = await query.order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  },

  // Filtrar personas por status, role, department
  filter: async (filters: {
    empresaId?: string
    status?: Persona['status']
    role?: string
    department?: string
    specialty?: string
  }): Promise<Persona[]> => {
    let query = supabase
      .from('personas')
      .select('*')

    if (filters.empresaId) query = query.eq('empresa_id', filters.empresaId)
    if (filters.status) query = query.eq('status', filters.status)
    if (filters.role) query = query.ilike('role', `%${filters.role}%`)
    if (filters.department) query = query.ilike('department', `%${filters.department}%`)
    if (filters.specialty) query = query.ilike('specialty', `%${filters.specialty}%`)

    const { data, error } = await query.order('created_at', { ascending: false })

    if (error) throw error
    return data || []
  }
}