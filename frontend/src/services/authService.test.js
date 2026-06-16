import { vi, describe, it, expect, beforeEach } from 'vitest';
import { register } from './authService';
import { supabase } from '../lib/supabaseClient';

vi.mock('../lib/supabaseClient', () => ({
  supabase: {
    auth: {
      signUp: vi.fn(),
    }
  }
}));

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('register', () => {
    it('should return success and user data on successful registration', async () => {
      const mockUser = { id: '123', email: 'test@example.com' };
      supabase.auth.signUp.mockResolvedValueOnce({
        data: { user: mockUser },
        error: null,
      });

      const result = await register('test@example.com', 'password123', 'Test User');

      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
        options: {
          data: { name: 'Test User' },
        },
      });
      expect(result).toEqual({ success: true, data: mockUser, error: null });
    });

    it('should return an error when supabase returns an error', async () => {
      supabase.auth.signUp.mockResolvedValueOnce({
        data: { user: null },
        error: { message: 'Registration failed' },
      });

      const result = await register('test@example.com', 'password123', 'Test User');

      expect(result).toEqual({ success: false, data: null, error: 'Registration failed' });
    });

    it('should handle thrown exceptions gracefully', async () => {
      supabase.auth.signUp.mockRejectedValueOnce(new Error('Network error'));

      const result = await register('test@example.com', 'password123', 'Test User');

      expect(result).toEqual({ success: false, data: null, error: 'Network error' });
    });
  });
});
