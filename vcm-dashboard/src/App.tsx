import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import LoginPage from './pages/Login'

// Importar páginas reais
import Dashboard from './pages/Dashboard'
import Empresas from './pages/Empresas'
import EmpresaDetails from './pages/EmpresaDetails'
import Personas from './pages/Personas'
import PersonaDetails from './pages/PersonaDetails'
import Workflows from './pages/Workflows'
import RAG from './pages/RAG'
import Settings from './pages/Settings'

// Protected route component - acesso direto para desenvolvimento
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <>{children}</>
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        
        {/* Protected routes - acesso direto para desenvolvimento */}
        <Route path="/" element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="empresas" element={<Empresas />} />
          <Route path="empresas/:id" element={<EmpresaDetails />} />
          <Route path="personas" element={<Personas />} />
          <Route path="personas/:id" element={<PersonaDetails />} />
          <Route path="workflows" element={<Workflows />} />
          <Route path="rag" element={<RAG />} />
          <Route path="settings" element={<Settings />} />
        </Route>
        
        {/* Redirecionamento da raiz para dashboard */}
        <Route path="/" element={<Navigate to="/" replace />} />
        
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App