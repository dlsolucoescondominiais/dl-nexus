import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabaseClient';

interface Lead {
  id: string;
  nome: string;
  telefone: string;
  empresa_condominio: string;
  tipo_cliente: string;
  servico_desejado: string;
  pipeline_stage: string;
  score_comercial: number;
  ultima_interacao: string;
}

export default function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [kpis, setKpis] = useState({
    total_leads: 0,
    em_negociacao: 0,
    fechado_ganho: 0,
    contratos_ativos: 0
  });

  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();

    // Subscribing ao Supabase Realtime V6
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

    // 1. Fetch Leads V6 (Enterprise)
    const { data: leadsData, error: leadsError } = await supabase
      .from('leads')
      .select('id, nome, telefone, empresa_condominio, tipo_cliente, servico_desejado, pipeline_stage, score_comercial, ultima_interacao')
      .order('ultima_interacao', { ascending: false });

    if (leadsError) console.error('Erro ao buscar leads:', leadsError);

    setLeads(leadsData || []);

    // Calcula KPIs do Funil
    const total = leadsData?.length || 0;
    const negociando = leadsData?.filter(l => l.pipeline_stage === 'negociacao').length || 0;
    const ganhos = leadsData?.filter(l => l.pipeline_stage === 'fechado_ganho').length || 0;
    const recorrentes = leadsData?.filter(l => l.pipeline_stage === 'contrato_recorrente').length || 0;

    setKpis({
      total_leads: total,
      em_negociacao: negociando,
      fechado_ganho: ganhos,
      contratos_ativos: recorrentes
    });

    setLoading(false);
  };

  if (loading && leads.length === 0) {
    return <div className="p-8 text-center text-slate-500">Inicializando DL Commander...</div>;
  }

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">DL Commander (Visão Executiva)</h1>
        <p className="text-slate-500 mt-1">Pipeline B2B, Conversão e Gestão OPEX (Zonas Sul, Norte, Oeste, Sudoeste)</p>
      </header>

      {/* KPIs da Operação (Pipeline de Vendas) */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-slate-200">
          <div className="px-5 py-5">
            <dt className="text-sm font-medium text-slate-500 truncate">Total no Funil</dt>
            <dd className="mt-1 text-3xl font-semibold text-slate-900">{kpis.total_leads}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-slate-200">
          <div className="px-5 py-5">
            <dt className="text-sm font-medium text-slate-500 truncate">Em Negociação</dt>
            <dd className="mt-1 text-3xl font-semibold text-yellow-600">{kpis.em_negociacao}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-slate-200">
          <div className="px-5 py-5">
            <dt className="text-sm font-medium text-slate-500 truncate">Fechado (Ganho)</dt>
            <dd className="mt-1 text-3xl font-semibold text-green-600">{kpis.fechado_ganho}</dd>
          </div>
        </div>
        <div className="bg-white overflow-hidden shadow-sm rounded-xl border border-slate-200 bg-slate-800">
          <div className="px-5 py-5">
            <dt className="text-sm font-medium text-slate-300 truncate">Contratos OPEX (Recorrente)</dt>
            <dd className="mt-1 text-3xl font-semibold text-white">{kpis.contratos_ativos}</dd>
          </div>
        </div>
      </div>

      {/* Tabela de Pipeline Enterprise Real-Time */}
      <div className="bg-white shadow-sm rounded-xl border border-slate-200">
        <div className="px-6 py-5 border-b border-slate-100 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-slate-800">Esteira de Negócios (Pipeline IA)</h3>
          <button onClick={fetchDashboardData} className="text-sm font-medium text-blue-600 hover:text-blue-500">Sincronizar</button>
        </div>
        <ul className="divide-y divide-slate-100 overflow-y-auto max-h-[600px]">
          {leads.map((lead) => (
            <li key={lead.id} className="px-6 py-5 hover:bg-slate-50 cursor-pointer transition-colors" onClick={() => navigate(`/lead/${lead.id}`)}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <p className="text-base font-bold text-slate-900 truncate">
                    {lead.empresa_condominio || lead.nome || 'Condomínio Não Informado'}
                  </p>
                  {lead.score_comercial > 80 && (
                     <span className="bg-orange-100 text-orange-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">Hot Lead</span>
                  )}
                </div>
                <div className="ml-2 flex-shrink-0 flex">
                  <p className={`px-3 py-1 inline-flex text-xs font-bold uppercase tracking-wider rounded-full
                    ${lead.pipeline_stage === 'novo_lead' ? 'bg-blue-50 text-blue-700' :
                      lead.pipeline_stage === 'triagem_ia' ? 'bg-indigo-50 text-indigo-700' :
                      lead.pipeline_stage.includes('fechado_ganho') ? 'bg-green-100 text-green-800' :
                      lead.pipeline_stage.includes('contrato') ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-700'}`}>
                    {lead.pipeline_stage.replace('_', ' ')}
                  </p>
                </div>
              </div>
              <div className="mt-2 flex justify-between items-center">
                <div className="flex items-center space-x-4">
                  <p className="text-sm text-slate-500 font-medium">📱 {lead.telefone}</p>
                  <p className="text-sm text-slate-500 capitalize">
                    🔧 {lead.servico_desejado ? lead.servico_desejado.replace('_', ' ') : 'Pendente'}
                  </p>
                  <p className="text-sm text-slate-500 capitalize">
                    🏢 {lead.tipo_cliente ? lead.tipo_cliente.replace('_', ' ') : 'Pendente'}
                  </p>
                </div>
                <div className="text-xs text-slate-400 font-medium">
                  Última interação: {new Date(lead.ultima_interacao).toLocaleDateString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </li>
          ))}
          {leads.length === 0 && (
            <li className="px-6 py-12 text-center text-slate-500 font-medium">O Funil está vazio. Nenhuma oportunidade encontrada na V6.</li>
          )}
        </ul>
      </div>
    </div>
  );
}
