import React, { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useRealtimeMessages } from '../hooks/useRealtimeMessages';
import { supabase } from '../lib/supabaseClient';

export function Chat() {
  const { leadId } = useParams();
  const [telefoneFiltro, setTelefoneFiltro] = useState<string | undefined>();

  const { messages } = useRealtimeMessages(telefoneFiltro);
  const [newMessage, setNewMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchLead() {
        if (!leadId) return;
        const { data, error } = await supabase.from('leads').select('telefone').eq('id', leadId).single();
        if (data && !error) {
            setTelefoneFiltro(data.telefone);
        }
    }
    fetchLead();
  }, [leadId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !telefoneFiltro) return;

    const tempMessage = {
      telefone: telefoneFiltro,
      mensagem: newMessage,
      direcao: 'saida',
      tipo: 'text',
      lead_id: leadId,
    };

    const { error } = await supabase.from('mensagens_whatsapp').insert([tempMessage]);

    if (error) {
      console.error("Erro ao enviar mensagem:", error);
      alert("Falha ao gravar mensagem.");
      return;
    }

    try {
      await fetch('https://n8n.dlsolucoescondominiais.com.br/webhook/send-whatsapp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tempMessage)
      });
    } catch (err) {
      console.error("Erro ao acionar n8n:", err);
    }

    setNewMessage('');
  };

  if (!telefoneFiltro) {
      return <div className="p-4">Carregando dados do Lead...</div>;
  }

  return (
    <div className="flex flex-col h-[calc(100vh-64px)] bg-gray-50 font-inter">
      <div className="bg-white p-4 shadow-sm z-10">
        <h2 className="text-xl font-manrope font-bold">Chat com Lead: {telefoneFiltro}</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.direcao === 'saida' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] rounded-lg p-3 ${
              msg.direcao === 'saida'
                ? 'bg-blue-600 text-white rounded-br-none'
                : 'bg-white text-gray-800 rounded-bl-none shadow-sm'
            }`}>
              <p className="text-sm">{msg.mensagem}</p>
              <span className={`text-[10px] block mt-1 ${msg.direcao === 'saida' ? 'text-blue-200' : 'text-gray-400'}`}>
                {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="bg-white p-4 shadow-[0_-2px_10px_rgba(0,0,0,0.05)]">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            placeholder="Digite uma mensagem..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6 py-2 font-medium transition-colors"
          >
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}
