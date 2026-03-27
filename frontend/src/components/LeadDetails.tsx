import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabaseClient';

interface Lead {
  id: string;
  condominio_id: string | null;
  nome: string;
  telefone: string;
  origem: string;
  status: string;
  criado_em: string;
  email_encaminhamento: string | null;
}

export default function LeadDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [lead, setLead] = useState<Lead | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchLeadDetails() {
      if (!id) return;
      setLoading(true);
      setError(null);

      const { data, error } = await supabase
        .from('leads')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        console.error('Erro ao buscar detalhes do lead:', error);
        setError('Não foi possível carregar os detalhes do lead.');
      } else {
        setLead(data);
      }
      setLoading(false);
    }

    fetchLeadDetails();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#f8f9fa] p-8 flex justify-center items-center">
        <div className="text-xl text-[#525f73] font-['Inter']">Carregando detalhes do lead...</div>
      </div>
    );
  }

  if (error || !lead) {
    return (
      <div className="min-h-screen bg-[#f8f9fa] p-8 flex flex-col justify-center items-center">
        <div className="text-xl text-[#ba1a1a] font-['Inter'] mb-4">{error || 'Lead não encontrado.'}</div>
        <button
          onClick={() => navigate('/dashboard-tecnico')}
          className="bg-[#003f87] hover:bg-[#0056b3] text-white font-['Inter'] py-2 px-4 rounded-lg shadow-sm"
        >
          Voltar ao Dashboard
        </button>
      </div>
    );
  }

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'novo': return 'bg-[#ffc49b] text-[#713700]'; // tertiary_container / on_tertiary_fixed_variant
      case 'triagem': return 'bg-[#d6e3fb] text-[#586579]'; // secondary_container / on_secondary_container
      case 'roteado': return 'bg-[#d7e2ff] text-[#001a40]'; // primary_fixed / on_primary_fixed
      case 'proposta_gerada': return 'bg-[#acc7ff] text-[#004491]'; // primary_fixed_dim / on_primary_fixed_variant
      case 'rejeitada': return 'bg-[#ffdad6] text-[#93000a]'; // error_container / on_error_container
      default: return 'bg-[#d9dadb] text-[#424752]'; // surface_dim / on_surface_variant
    }
  };

  return (
    <div className="min-h-screen bg-[#f8f9fa] p-8 font-['Inter'] text-[#191c1d]">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold font-['Manrope'] text-[#191c1d]">Detalhes do Lead</h1>
            <p className="text-[#424752] mt-1">Informações completas e ações</p>
          </div>
          <button
            onClick={() => navigate('/dashboard-tecnico')}
            className="text-[#003f87] hover:text-[#0056b3] font-medium px-4 py-2 bg-transparent rounded hover:bg-[#f3f4f5] transition-colors"
          >
            &larr; Voltar
          </button>
        </header>

        <div className="bg-[#ffffff] rounded-2xl p-8 mb-8" style={{ boxShadow: '0px 12px 32px rgba(25, 28, 29, 0.04)' }}>
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold font-['Manrope'] text-[#191c1d]">{lead.nome || 'Nome não informado'}</h2>
            <span className={`px-3 py-1 text-sm font-semibold rounded-full uppercase tracking-wider ${getStatusBadgeClass(lead.status)}`}>
              {lead.status}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-6">
            <div className="bg-[#f3f4f5] p-6 rounded-xl">
              <h3 className="text-xs font-semibold text-[#727784] uppercase tracking-wider mb-4">Informações de Contato</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-[#525f73] mb-1">Telefone</p>
                  <p className="text-base font-medium">{lead.telefone || 'N/A'}</p>
                </div>
                <div>
                  <p className="text-sm text-[#525f73] mb-1">Email de Encaminhamento (IA)</p>
                  <p className="text-base font-medium">{lead.email_encaminhamento || 'Não roteado'}</p>
                </div>
              </div>
            </div>

            <div className="bg-[#f3f4f5] p-6 rounded-xl">
              <h3 className="text-xs font-semibold text-[#727784] uppercase tracking-wider mb-4">Metadados do Lead</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-[#525f73] mb-1">Data de Criação</p>
                  <p className="text-base font-medium">{new Date(lead.criado_em).toLocaleString('pt-BR')}</p>
                </div>
                <div>
                  <p className="text-sm text-[#525f73] mb-1">Origem</p>
                  <p className="text-base font-medium">{lead.origem || 'Não identificada'}</p>
                </div>
                <div>
                  <p className="text-sm text-[#525f73] mb-1">ID do Condomínio</p>
                  <p className="text-base font-medium font-mono text-sm">{lead.condominio_id || 'N/A'}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex gap-4">
          <button
            onClick={() => navigate(`/checklist/${lead.id}`)}
            className="flex-1 bg-gradient-to-br from-[#003f87] to-[#0056b3] hover:from-[#004491] hover:to-[#0056b3] text-white font-semibold py-4 px-6 rounded-xl shadow-md transition-all text-center text-lg"
          >
            Iniciar Avaliação Técnica
          </button>
        </div>
      </div>
    </div>
  );
}
