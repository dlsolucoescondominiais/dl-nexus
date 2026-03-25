import { createClient } from '@supabase/supabase-js';

// As variáveis de ambiente devem ser prefixadas com VITE_ ou NEXT_PUBLIC_ dependendo do framework.
// Vamos assumir React com Vite (padrão moderno para SPAs)
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://nejdtvkpiclagsnfljsz.supabase.co';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseAnonKey) {
  console.error("Supabase config is missing. Please set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in your .env file.");
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
