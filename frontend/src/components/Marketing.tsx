import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';
import { apiClient } from '../lib/apiClient';

interface Conteudo {
  id: string;
  tipo: string;
  problema: string;
  copy_gerada: string;
  status: string;
  imagem_url?: string;
  criado_em: string;
  erro_meta_api?: string;
}

export default function Marketing() {
  const [conteudos, setConteudos] = useState<Conteudo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConteudos();

    const subscription = supabase
      .channel('public:conteudos_marketing')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'conteudos_marketing' }, () => {
        fetchConteudos();
      })
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);

  const fetchConteudos = async () => {
    setLoading(true);
    const { data, error } = await supabase
      .from('conteudos_marketing')
      .select('*')
      .order('criado_em', { ascending: false });

    if (error) console.error('Erro ao buscar conteúdos:', error);
    setConteudos(data || []);
    setLoading(false);
  };

  const handleAprovar = async (id: string, copy_gerada: string) => {
    if (!confirm('Aprovar e disparar post para a Meta (Facebook/Instagram)?')) return;

    try {
      // 1. Atualizar banco para 'agendado' para dar feedback visual
      await supabase.from('conteudos_marketing').update({ status: 'agendado' }).eq('id', id);

      // 2. Acionar a Rota Antigravity para chamar o Webhook 013 do n8n
      await apiClient.post('/api/marketing/aprovar', {
        post_id: id,
        copy_aprovada: copy_gerada,
        imagem_url: 'https://cdn.dlsolucoescondominiais.com.br/assets/imagem_padrao_marketing.jpg'
      });

      alert('Post enviado ao orquestrador!');
    } catch (err: any) {
      alert(`Falha ao disparar automação: ${err.message}`);
      // Reverte status visual se a API falhar
      await supabase.from('conteudos_marketing').update({ status: 'pendente_aprovacao' }).eq('id', id);
    }
  };

  if (loading && conteudos.length === 0) return <div className="p-8 text-slate-500">Buscando cópias geradas pela IA...</div>;

  return (
    <div className="min-h-screen bg-slate-50 p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Atração de Síndicos (Marketing AI)</h1>
        <p className="text-slate-500 mt-1">Aprovação Semi-Automática de Redes Sociais</p>
      </header>

      <div className="grid grid-cols-1 gap-6">
        {conteudos.map(post => (
          <div key={post.id} className="bg-white shadow-sm rounded-xl border border-slate-200 p-6 flex flex-col md:flex-row gap-6">
            <div className="flex-1">
              <div className="flex justify-between mb-4">
                <div className="flex space-x-2">
                  <span className="px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-bold rounded-full uppercase">Tema: {post.problema}</span>
                  <span className="px-3 py-1 bg-slate-100 text-slate-800 text-xs font-bold rounded-full uppercase">{post.tipo}</span>
                </div>
                <div>
                  {post.status === 'pendente_aprovacao' && <span className="text-yellow-600 font-semibold text-sm">⏳ Pendente Diogo</span>}
                  {post.status === 'publicado' && <span className="text-green-600 font-semibold text-sm">✅ Publicado na Meta</span>}
                  {post.status === 'erro' && <span className="text-red-600 font-semibold text-sm">❌ Erro API</span>}
                  {post.status === 'agendado' && <span className="text-blue-600 font-semibold text-sm">🚀 Disparando...</span>}
                </div>
              </div>

              <textarea
                className="w-full h-40 p-4 bg-slate-50 border border-slate-200 rounded-lg text-slate-700 font-mono text-sm"
                defaultValue={post.copy_gerada}
                onChange={(e) => {
                  // Mutação local se o Diogo quiser editar o texto da IA antes de enviar
                  post.copy_gerada = e.target.value;
                }}
              />

              {post.erro_meta_api && (
                <p className="text-xs text-red-500 mt-2 font-mono">Log Meta: {post.erro_meta_api}</p>
              )}
            </div>

            <div className="md:w-48 flex flex-col justify-center gap-3 border-l border-slate-100 md:pl-6">
              <p className="text-xs text-slate-400 mb-2">Gerado em: {new Date(post.criado_em).toLocaleDateString()}</p>
              <button
                disabled={post.status === 'publicado' || post.status === 'agendado'}
                onClick={() => handleAprovar(post.id, post.copy_gerada)}
                className="w-full px-4 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors shadow-sm"
              >
                Aprovar & Postar
              </button>
            </div>
          </div>
        ))}
        {conteudos.length === 0 && (
          <div className="text-center py-12 bg-white rounded-xl border border-slate-200 text-slate-500">
            A IA (Cron do n8n) ainda não gerou cópias nesta semana.
          </div>
        )}
      </div>
    </div>
  );
}
