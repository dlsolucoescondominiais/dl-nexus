import { describe, it, expect, vi, beforeEach } from 'vitest';
import { login } from './authService';
import { supabase } from '../lib/supabaseClient';

// Mock the supabase client
vi.mock('../lib/supabaseClient', () => ({
  supabase: {
    auth: {
      signInWithPassword: vi.fn(),
    },
  },
}));

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should return success true when login is successful', async () => {
      const mockUser = { id: '1', email: 'test@example.com' };
      supabase.auth.signInWithPassword.mockResolvedValue({
        data: { user: mockUser },
        error: null,
      });

      const result = await login('test@example.com', 'password123');

      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual({ success: true, data: mockUser, error: null });
    });

    it('should return error when supabase returns an error object', async () => {
      supabase.auth.signInWithPassword.mockResolvedValue({
        data: null,
        error: { message: 'Invalid credentials' },
      });

      const result = await login('test@example.com', 'wrongpassword');

      expect(result).toEqual({ success: false, data: null, error: 'Invalid credentials' });
    });

    it('should return error when an exception is thrown during login (with err.message)', async () => {
      supabase.auth.signInWithPassword.mockRejectedValue(new Error('Network error'));

      const result = await login('test@example.com', 'password123');

      expect(result).toEqual({ success: false, data: null, error: 'Network error' });
    });

    it('should return default error when an exception is thrown without err.message', async () => {
      supabase.auth.signInWithPassword.mockRejectedValue('Something bad happened'); // Not an Error object

      const result = await login('test@example.com', 'password123');

      expect(result).toEqual({ success: false, data: null, error: 'An unexpected error occurred during login.' });
    });
  });
});
