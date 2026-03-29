import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Checklist from './components/Checklist';
import LeadDetails from './components/LeadDetails';
import Marketing from './components/Marketing';

function ChecklistWrapper() {
  const { leadId } = useParams();
  return <Checklist leadId={leadId || "demo-id"} tecnicoNome="Especialista DL" />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />

        {/* Painel do Tecnólogo/Admin */}
                        <Route path="/dashboard-tecnico" element={<Dashboard />} />

        {/* Motor de Atracao B2B (Redes Sociais) */}
        <Route path="/marketing" element={<Marketing />} />

        {/* Raio-X B2B do Sindico */}
        <Route path="/lead/:id" element={<LeadDetails />} />

        {/* Portal do Síndico (Placeholder para V2) */}
        <Route path="/portal-sindico" element={
          <div className="p-8 text-center text-xl text-gray-700">
            Portal do Síndico (Em Construção) - DL Nexus
          </div>
        } />

        {/* Módulo Mobile para a Rua */}
        <Route path="/checklist/:leadId" element={<ChecklistWrapper />} />

        {/* Demo local */}
        <Route path="/checklist" element={
          <Checklist leadId="demo-id" tecnicoNome="Especialista DL" />
        } />

      </Routes>
    </Router>
  );
}

export default App;
