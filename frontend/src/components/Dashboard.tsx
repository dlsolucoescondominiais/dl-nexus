import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabaseClient';

interface Lead {
  id: string;
  condominio_id: string | null;
  nome: string;
  telefone: string;
  origem: string;
  status: string;
  criado_em: string;
}

export default function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const [kpis, setKpis] = useState({ novos: 0, avaliacoes_concluidas: 0, propostas_ativas: 0 });

  useEffect(() => {
    fetchDashboardData();

    // Subscribing ao Supabase Realtime para não precisar de F5 quando n8n injeta dados
    const subscription = supabase
      .channel('public:leads')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'leads' }, payload => {
        fetchDashboardData();
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);

    // 1. Fetch Leads V3
    const { data: leadsData, error: leadsError } = await supabase
      .from('leads')
      .select('id, condominio_id, nome, telefone, origem, status, criado_em')
      .order('criado_em', { ascending: false });

    // 2. Fetch Avaliações Técnicas (Contagem)
    const { count: avaliacoesCount, error: avaliacoesError } = await supabase
      .from('avaliacoes_tecnicas')
      .select('*', { count: 'exact', head: true });

    // 3. Fetch Propostas (Contagem Ativas)
    const { count: propostasCount, error: propostasError } = await supabase
      .from('propostas')
      .select('*', { count: 'exact', head: true })
      .neq('status', 'rejeitada'); // V3 status_proposta

    if (leadsError) console.error('Erro ao buscar leads:', leadsError);

    setLeads(leadsData || []);

    const novos = leadsData?.filter(l => l.status === 'novo').length || 0;

    setKpis({
      novos,
      avaliacoes_concluidas: avaliacoesCount || 0,
      propostas_ativas: propostasCount || 0
    });

    setLoading(false);
  };

  if (loading && leads.length === 0) {
    return <div className="p-8 text-center">Carregando Cérebro DL Nexus...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard Tático B2B</h1>
        <p className="text-gray-500">Gestão Automática de Leads e Automação OPEX</p>
      </header>

      {/* KPIs da Operação (Pipeline de Vendas) */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3 lg:grid-cols-3 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg border-l-4 border-blue-500">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Novos Leads (IA Triando)</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{kpis.novos}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow rounded-lg border-l-4 border-yellow-500">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Avaliações Técnicas Realizadas</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{kpis.avaliacoes_concluidas}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow rounded-lg border-l-4 border-green-500">
          <div className="px-4 py-5 sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">Propostas OPEX (Ativas)</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{kpis.propostas_ativas}</dd>
          </div>
        </div>
      </div>

      {/* Tabela de Leads Real-Time */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 border-b border-gray-200 sm:px-6 flex justify-between">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Pipeline de Síndicos</h3>
          <button onClick={fetchDashboardData} className="text-sm text-blue-600 hover:text-blue-500">Atualizar</button>
        </div>
        <ul className="divide-y divide-gray-200 overflow-y-auto max-h-96">
          {leads.map((lead) => (
            <li key={lead.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50 cursor-pointer" onClick={() => navigate(`/lead/${lead.id}`)}>
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-blue-600 truncate">{lead.nome || 'Nome não informado'}</p>
                <div className="ml-2 flex-shrink-0 flex">
                  <p className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                    ${lead.status === 'novo' ? 'bg-blue-100 text-blue-800' :
                      lead.status === 'triagem' ? 'bg-yellow-100 text-yellow-800' :
                      lead.status === 'roteado' ? 'bg-indigo-100 text-indigo-800' :
                      lead.status === 'proposta_gerada' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                    {lead.status.toUpperCase()}
                  </p>
                </div>
              </div>
              <div className="mt-2 sm:flex sm:justify-between">
                <div className="sm:flex">
                  <p className="flex items-center text-sm text-gray-500 mr-4">
                    📱 {lead.telefone}
                  </p>
                  <p className="flex items-center text-sm text-gray-500 mr-4 font-semibold">
                    Origem: {lead.origem || 'Não identificada'}
                  </p>
                </div>
                <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                  <p>{new Date(lead.criado_em).toLocaleDateString('pt-BR')}</p>
                </div>
              </div>
            </li>
          ))}
          {leads.length === 0 && (
            <li className="px-4 py-8 text-center text-gray-500">Nenhum lead encontrado no banco.</li>
          )}
        </ul>
      </div>
    </div>
  );
}
