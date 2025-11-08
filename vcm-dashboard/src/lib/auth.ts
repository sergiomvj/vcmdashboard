import { supabase } from './supabase'
import React, { useState, useEffect } from 'react'

interface AuthState {
  user: any | null
  session: any | null
  isLoading: boolean
}

export const auth = {
  // Login
  signIn: async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    return { error }
  },

  // Registro
  signUp: async (email: string, password: string, metadata?: Record<string, any>) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata
      }
    })
    return { error }
  },

  // Logout
  signOut: async () => {
    await supabase.auth.signOut()
  },

  // Reset de senha
  resetPassword: async (email: string) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/reset-password`
    })
    return { error }
  },

  // Atualizar senha
  updatePassword: async (newPassword: string) => {
    const { error } = await supabase.auth.updateUser({
      password: newPassword
    })
    return { error }
  },

  // Obter usuário atual
  getCurrentUser: async () => {
    const { data: { user }, error } = await supabase.auth.getUser()
    return { user, error }
  },

  // Obter sessão atual
  getCurrentSession: async () => {
    const { data: { session }, error } = await supabase.auth.getSession()
    return { session, error }
  },

  // Refresh session
  refreshSession: async () => {
    const { error } = await supabase.auth.refreshSession()
    return { error }
  },

  // Listener para mudanças de auth
  onAuthStateChange: (callback: (event: string, session: any | null) => void) => {
    return supabase.auth.onAuthStateChange(callback)
  }
}

// Hook customizado para autenticação
export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    session: null,
    isLoading: true
  })

  useEffect(() => {
    // Obter sessão inicial
    const getInitialSession = async () => {
      const { session } = await auth.getCurrentSession()
      setAuthState({
        user: session?.user || null,
        session: session,
        isLoading: false
      })
    }

    getInitialSession()

    // Configurar listener para mudanças de auth
    const { data: { subscription } } = auth.onAuthStateChange((event, session) => {
      setAuthState({
        user: session?.user || null,
        session: session,
        isLoading: false
      })
    })

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  return authState
}