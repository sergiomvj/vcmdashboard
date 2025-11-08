import { Routes, Route } from 'react-router-dom'
import { Layout } from '../components/layout/Layout'
import Dashboard from '../pages/Dashboard'
import Empresas from '../pages/Empresas'
import Personas from '../pages/Personas'
import Workflows from '../pages/Workflows'
import RAG from '../pages/RAG'
import Settings from '../pages/Settings'
import EmpresaDetails from '../pages/EmpresaDetails'
import PersonaDetails from '../pages/PersonaDetails'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="/empresas" element={<Empresas />} />
        <Route path="/empresas/:id" element={<EmpresaDetails />} />
        <Route path="/personas" element={<Personas />} />
        <Route path="/personas/:id" element={<PersonaDetails />} />
        <Route path="/workflows" element={<Workflows />} />
        <Route path="/rag" element={<RAG />} />
        <Route path="/settings" element={<Settings />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes