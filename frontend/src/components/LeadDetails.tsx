import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabaseClient';

interface Mensagem {
  id: string;
  mensagem: string;
  direcao: string;
  created_at: string;
}

const LeadDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lead, setLead] = useState<any>(null);
  const [mensagens, setMensagens] = useState<Mensagem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeadDetails = async () => {
      try {
        // Busca os dados do lead juntamente com os dados do condomínio (FK)
        const { data: leadData, error: leadError } = await supabase
          .from('leads')
          .select('*, condominio:condominios(nome, endereco, cnpj)')
          .eq('id', id)
          .single();

        if (leadError) throw leadError;
        setLead(leadData);

        // Se o lead tiver telefone, busca as conversas da Aninha no WhatsApp
        if (leadData?.telefone) {
          const { data: msgData, error: msgError } = await supabase
            .from('mensagens_whatsapp')
            .select('*')
            .eq('telefone', leadData.telefone)
            .order('created_at', { ascending: true });

          if (msgError) console.error("Erro ao buscar mensagens:", msgError);
          setMensagens(msgData || []);
        }

      } catch (error) {
        console.error('Erro ao procurar os detalhes do lead:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchLeadDetails();

    let subscription: any;
    if (leadData?.telefone) {
      // Inscreve no canal de mensagens filtrando EXATAMENTE pelo telefone deste lead
      subscription = supabase
        .channel(`chat_lead_${leadData.telefone}`)
        .on('postgres_changes', {
            event: 'INSERT',
            schema: 'public',
            table: 'mensagens_whatsapp',
            filter: `telefone=eq.${leadData.telefone}`
          },
          (payload) => {
            setMensagens((current) => [...current, payload.new as Mensagem]);
          }
        )
        .subscribe();
    }

    return () => {
      if (subscription) supabase.removeChannel(subscription);
    };
  }, [id]);

  if (loading) return <div className="p-8 text-center text-slate-500">A carregar detalhes do lead...</div>;
  if (!lead) return <div className="p-8 text-center text-red-500">Lead não encontrado na base de dados.</div>;

  return (
    <div className="max-w-5xl mx-auto p-6 bg-white rounded-lg shadow-md mt-8">
      <div className="flex justify-between items-center border-b pb-4 mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Painel de Controlo: Detalhes do Lead</h1>
        <Link to="/dashboard-tecnico" className="px-4 py-2 bg-slate-800 text-white rounded-md hover:bg-slate-700 transition-colors">
          Voltar ao Dashboard
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-slate-50 p-5 rounded-md border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-700 mb-3 border-b pb-2">Informação do Cliente</h2>
          <p className="mb-2"><strong>Nome do Contato:</strong> {lead.nome}</p>
          <p className="mb-2"><strong>Condomínio/Colégio:</strong> {lead.condominio?.nome || 'Não vinculado (B2B Pendente)'}</p>
          <p className="mb-2"><strong>Telefone:</strong> {lead.telefone}</p>
          <p className="mb-2"><strong>E-mail:</strong> {lead.email || 'Não informado'}</p>
        </div>

        <div className="bg-slate-50 p-5 rounded-md border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-700 mb-3 border-b pb-2">Detalhes da Oportunidade</h2>
          <p className="mb-2"><strong>Origem de Captação:</strong> <span className="capitalize">{lead.origem || 'Desconhecida'}</span></p>
          <p className="mb-2"><strong>Data de Entrada:</strong> {new Date(lead.criado_em).toLocaleString('pt-BR')}</p>

          <div className="mt-4 flex items-center justify-between">
            <p className="flex items-center">
              <strong>Status:</strong>
              <span className={`ml-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider
                ${lead.status === 'novo' ? 'bg-blue-100 text-blue-800' :
                  lead.status === 'triagem' ? 'bg-yellow-100 text-yellow-800' :
                  lead.status === 'roteado' ? 'bg-indigo-100 text-indigo-800' :
                  lead.status === 'proposta_gerada' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                {lead.status}
              </span>
            </p>
            <button
              onClick={() => navigate(`/checklist/${lead.id}`)}
              className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-500 shadow-sm"
            >
              Fazer Vistoria
            </button>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-slate-50 p-5 rounded-md border border-slate-200">
        <h2 className="text-lg font-semibold text-slate-700 mb-3 border-b pb-2">Mensagem Original (Primeiro Contato)</h2>
        <p className="text-slate-600 whitespace-pre-wrap italic">"{lead.mensagem || 'Sem mensagem de escopo.'}"</p>
      </div>

      {/* Injeção da Tabela de Mensagens do WhatsApp */}
      <div className="mt-8 border-t pt-6">
        <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold text-slate-800">Histórico de Conversa (WhatsApp)</h2>
            <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-1 rounded-full animate-pulse">
                Sincronizado com Meta API
            </span>
        </div>

        <div className="bg-[#efeae2] border border-slate-300 rounded-lg h-96 flex flex-col p-4 overflow-y-auto">
          {mensagens.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-slate-500">
              <svg className="w-8 h-8 mb-2 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              <span>A Aninha ainda não registrou interações para este número ({lead.telefone}).</span>
            </div>
          ) : (
            <div className="space-y-4">
              {mensagens.map((msg) => (
                <div key={msg.id} className={`flex ${msg.direcao === 'saida' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[75%] rounded-lg px-4 py-2 shadow-sm relative ${
                    msg.direcao === 'saida'
                      ? 'bg-[#d9fdd3] text-slate-800 rounded-tr-none'
                      : 'bg-white text-slate-800 rounded-tl-none border border-slate-200'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap break-words">{msg.mensagem}</p>
                    <p className="text-[10px] text-slate-400 text-right mt-1 font-medium">
                      {new Date(msg.created_at).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LeadDetails;
