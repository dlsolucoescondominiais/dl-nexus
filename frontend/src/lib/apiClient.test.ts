import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { apiClient } from './apiClient';
import { supabase } from './supabaseClient';

vi.mock('./supabaseClient', () => ({
  supabase: {
    auth: {
      getSession: vi.fn(),
    },
  },
}));

describe('apiClient.post', () => {
  const originalFetch = global.fetch;
  const originalConsoleError = console.error;

  beforeEach(() => {
    global.fetch = vi.fn();
    console.error = vi.fn(); // Suppress expected console.error in tests
  });

  afterEach(() => {
    global.fetch = originalFetch;
    console.error = originalConsoleError;
    vi.clearAllMocks();
  });

  it('should make a POST request with correct payload and Content-Type header when no session exists', async () => {
    (supabase.auth.getSession as any).mockResolvedValue({ data: { session: null } });
    const mockResponse = { success: true };

    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(mockResponse),
    });

    const endpoint = '/test-endpoint';
    const payload = { foo: 'bar' };
    const result = await apiClient.post(endpoint, payload);

    expect(supabase.auth.getSession).toHaveBeenCalled();
    expect(global.fetch).toHaveBeenCalledWith(`https://api.dlsolucoescondominiais.com.br${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    expect(result).toEqual(mockResponse);
  });

  it('should include Authorization header when a valid session exists', async () => {
    (supabase.auth.getSession as any).mockResolvedValue({
      data: {
        session: { access_token: 'fake-token-123' }
      }
    });
    const mockResponse = { success: true };

    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: vi.fn().mockResolvedValue(mockResponse),
    });

    await apiClient.post('/auth-endpoint', { data: 'test' });

    expect(global.fetch).toHaveBeenCalledWith(expect.any(String), expect.objectContaining({
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer fake-token-123',
      },
    }));
  });

  it('should throw an error with the detail from the API if response is not ok', async () => {
    (supabase.auth.getSession as any).mockResolvedValue({ data: { session: null } });

    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 400,
      json: vi.fn().mockResolvedValue({ detail: 'Invalid request data' }),
    });

    await expect(apiClient.post('/error-endpoint', {})).rejects.toThrow('Invalid request data');
    expect(console.error).toHaveBeenCalled();
  });

  it('should throw a fallback HTTP error if response is not ok and no detail is provided', async () => {
    (supabase.auth.getSession as any).mockResolvedValue({ data: { session: null } });

    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500,
      json: vi.fn().mockRejectedValue(new Error('Failed to parse JSON')), // JSON parse fails
    });

    await expect(apiClient.post('/server-error', {})).rejects.toThrow('Erro HTTP: 500');
    expect(console.error).toHaveBeenCalled();
  });

  it('should throw an error if fetch fails completely (e.g. network error)', async () => {
    (supabase.auth.getSession as any).mockResolvedValue({ data: { session: null } });

    const networkError = new Error('Network Error');
    (global.fetch as any).mockRejectedValue(networkError);

    await expect(apiClient.post('/network-error', {})).rejects.toThrow('Network Error');
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Falha no apiClient.post'), networkError);
  });
});
