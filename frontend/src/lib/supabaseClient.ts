import { createClient } from '@supabase/supabase-js';

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://mock.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'mock-anon-key';

// Validar se as variáveis de ambiente existem
if (!import.meta.env.VITE_SUPABASE_URL || !import.meta.env.VITE_SUPABASE_ANON_KEY) {
  console.warn('Variáveis de ambiente do Supabase não configuradas. Usando mock url para o ambiente não quebrar na inicialização.');
}

// Criar cliente Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
