import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';
import { LeadCard } from '../components/LeadCard';

export interface Lead {
  id: string;
  nome_contato: string;
  nome_condominio: string;
  telefone: string;
  status: 'novo' | 'triado' | 'em_contato' | 'proposta' | 'fechado' | 'perdido';
  tipo_servico: string;
  created_at: string;
}

export function Dashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => {
    // Busca inicial de Leads
    supabase.from('leads').select('*').order('created_at', { ascending: false }).then(({ data, error }) => {
      if (!error && data) setLeads(data as Lead[]);
    });

    // Supabase Realtime para Leads
    const leadsChannel = supabase.channel('leads_updates')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'leads' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setLeads((prev) => [payload.new as Lead, ...prev]);
          } else if (payload.eventType === 'UPDATE') {
            setLeads((prev) => prev.map((l) => (l.id === payload.new.id ? (payload.new as Lead) : l)));
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(leadsChannel);
    };
  }, []);

  return (
    <div className="p-8 font-inter">
      <h1 className="text-3xl font-manrope font-bold mb-6">DL Nexus - Dashboard do Técnico</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {leads.map((lead) => (
          <LeadCard key={lead.id} lead={lead} />
        ))}
      </div>
    </div>
  );
}
