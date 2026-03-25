import React, { useState } from 'react';
import { supabase } from '../lib/supabaseClient';

interface ChecklistProps {
  leadId: string; // Vem via rota ou props (qual condomínio está sendo avaliado)
  tecnicoNome: string; // Ex: Diogo
}

// Representação de um módulo (Ex: Módulo Commander para CFTV/Incêndio)
export default function ChecklistMobile({ leadId = 'a1b2c3d4-e5f6-7890-1234-567890abcdef', tecnicoNome = 'Especialista DL' }: ChecklistProps) {
  const [loading, setLoading] = useState(false);
  const [mensagem, setMensagem] = useState('');

  const [checklist, setChecklist] = useState({
    quadroEletrico: false,
    cabeamentoEstruturado: false,
    bombaDagua: false,
    cameraIntelbras: false,
    painelSolar: false,
    observacoes: '',
    viabilidade: 'media',
    score: 50
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as any;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setChecklist(prev => ({ ...prev, [name]: checked }));
    } else {
      setChecklist(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSalvarAvaliacao = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMensagem('Sincronizando com o DL Nexus...');

    try {
      // 1. Grava na tabela de avaliações técnicas no formato V3 do Supabase
      const { data, error } = await supabase
        .from('avaliacoes_tecnicas')
        .insert([
          {
            lead_id: leadId,
            agente: tecnicoNome, // Equivalente a Tecnico / Especialidade
            score: parseInt(checklist.score as any),
            recomendacoes: checklist.observacoes,
            viabilidade: checklist.viabilidade, // 'alta', 'media', 'baixa'
          }
        ])
        .select();

      if (error) throw error;

      // 2. Atualiza o status do Lead no Pipeline (Gatilho para n8n)
      const { error: updateError } = await supabase
        .from('leads')
        .update({ status: 'proposta_gerada' }) // V3 Status enum
        .eq('id', leadId);

      if (updateError) throw updateError;

      setMensagem('Avaliação Técnica salva! O DL Nexus já vai processar a Proposta.');
    } catch (err: any) {
      console.error('Erro ao salvar Avaliação:', err);
      setMensagem(`Falha: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white min-h-screen p-4 sm:p-6 lg:p-8 font-sans">
      <div className="max-w-3xl mx-auto">
        <header className="mb-6 pb-4 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 leading-tight">
            Módulo de Avaliação Técnica
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Formulário Dinâmico de Integração (Diogo | Responsável: {tecnicoNome})
          </p>
        </header>

        <form onSubmit={handleSalvarAvaliacao} className="space-y-6">

          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 shadow-sm">
            <h3 className="text-lg font-medium text-gray-900 mb-4 border-b pb-2">Itens Inspecionados</h3>

            <div className="space-y-4">
              <label className="flex items-center space-x-3 cursor-pointer p-2 hover:bg-gray-100 rounded">
                <input type="checkbox" name="quadroEletrico" className="h-5 w-5 text-blue-600 rounded" checked={checklist.quadroEletrico} onChange={handleChange} />
                <span className="text-gray-700 font-medium">Quadro Elétrico (Fiação exposta / Norma)</span>
              </label>

              <label className="flex items-center space-x-3 cursor-pointer p-2 hover:bg-gray-100 rounded">
                <input type="checkbox" name="cabeamentoEstruturado" className="h-5 w-5 text-blue-600 rounded" checked={checklist.cabeamentoEstruturado} onChange={handleChange} />
                <span className="text-gray-700 font-medium">Cabeamento Estruturado (Racks e Switch)</span>
              </label>

              <label className="flex items-center space-x-3 cursor-pointer p-2 hover:bg-gray-100 rounded">
                <input type="checkbox" name="cameraIntelbras" className="h-5 w-5 text-blue-600 rounded" checked={checklist.cameraIntelbras} onChange={handleChange} />
                <span className="text-gray-700 font-medium">Segurança CFTV (Infra Inteligente)</span>
              </label>

              <label className="flex items-center space-x-3 cursor-pointer p-2 hover:bg-gray-100 rounded">
                <input type="checkbox" name="painelSolar" className="h-5 w-5 text-blue-600 rounded" checked={checklist.painelSolar} onChange={handleChange} />
                <span className="text-gray-700 font-medium">Viabilidade Energia Solar Híbrida</span>
              </label>
            </div>
          </div>

          <div className="space-y-4">
            <div>
               <label htmlFor="score" className="block text-sm font-medium text-gray-700">Score da Vistoria (0 a 100)</label>
               <input type="number" name="score" min="0" max="100" value={checklist.score} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-3 border"/>
            </div>

            <div>
               <label htmlFor="viabilidade" className="block text-sm font-medium text-gray-700">Viabilidade</label>
               <select name="viabilidade" value={checklist.viabilidade} onChange={handleChange} className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-3 border">
                  <option value="alta">Alta</option>
                  <option value="media">Média</option>
                  <option value="baixa">Baixa</option>
               </select>
            </div>

            <div>
              <label htmlFor="observacoes" className="block text-sm font-medium text-gray-700">Recomendações</label>
              <textarea
                id="observacoes"
                name="observacoes"
                rows={4}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-3 border"
                placeholder="Descreva problemas críticos de segurança ou infraestrutura para justificar a proposta OPEX."
                value={checklist.observacoes}
                onChange={handleChange}
              ></textarea>
            </div>
          </div>

          {mensagem && (
            <div className={`p-4 rounded-md ${mensagem.includes('Falha') ? 'bg-red-50 text-red-800' : 'bg-green-50 text-green-800'}`}>
              <p className="text-sm font-medium">{mensagem}</p>
            </div>
          )}

          <div className="pt-4 flex justify-end">
            <button
              type="submit"
              disabled={loading}
              className="inline-flex justify-center py-3 px-6 border border-transparent shadow-sm text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 w-full sm:w-auto"
            >
              {loading ? 'Transmitindo...' : 'Salvar Avaliação Técnica'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
