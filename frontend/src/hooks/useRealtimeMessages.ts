import { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';

export interface Message {
  id: string;
  telefone: string;
  mensagem: string;
  direcao: 'entrada' | 'saida';
  created_at: string;
}

export function useRealtimeMessages(telefoneFiltro?: string) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    // Initial fetch
    let query = supabase.from('mensagens_whatsapp').select('*').order('created_at', { ascending: true });
    if (telefoneFiltro) query = query.eq('telefone', telefoneFiltro);

    query.then(({ data, error }) => {
      if (!error && data) setMessages(data as Message[]);
    });

    // Subscribe to Realtime channel
    const channel = supabase.channel('mensagens_updates')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'mensagens_whatsapp' },
        (payload) => {
          const newMessage = payload.new as Message;
          if (!telefoneFiltro || newMessage.telefone === telefoneFiltro) {
            setMessages((prev) => [...prev, newMessage]);
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [telefoneFiltro]);

  return { messages };
}
