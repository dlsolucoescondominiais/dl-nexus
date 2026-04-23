/**
 * DL Nexus - Camada de Comunicação Externa (Antigravity & Integrações B2B)
 */
import { supabase } from './supabaseClient';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.dlsolucoescondominiais.com.br';

export const apiClient = {
  async post(endpoint: string, payload: any) {
    const { data: { session } } = await supabase.auth.getSession();

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (session?.access_token) {
      headers['Authorization'] = `Bearer ${session.access_token}`;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erro HTTP: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Falha no apiClient.post(${endpoint}):`, error);
      throw error;
    }
  }
};
