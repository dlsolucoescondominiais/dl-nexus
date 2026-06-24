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
  describe('login', () => {
    beforeEach(() => {
      vi.clearAllMocks();
    });

    it('should return success and user data on successful login', async () => {
      // Arrange
      const mockUser = { id: '123', email: 'test@example.com' };
      supabase.auth.signInWithPassword.mockResolvedValueOnce({
        data: { user: mockUser },
        error: null,
      });

      // Act
      const result = await login('test@example.com', 'password123');

      // Assert
      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual({
        success: true,
        data: mockUser,
        error: null,
      });
    });

    it('should return error message when supabase returns an error', async () => {
      // Arrange
      const mockError = { message: 'Invalid login credentials' };
      supabase.auth.signInWithPassword.mockResolvedValueOnce({
        data: null,
        error: mockError,
      });

      // Act
      const result = await login('test@example.com', 'wrongpassword');

      // Assert
      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'wrongpassword',
      });
      expect(result).toEqual({
        success: false,
        data: null,
        error: 'Invalid login credentials',
      });
    });

    it('should handle unexpected exceptions and return a generic error message', async () => {
      // Arrange
      supabase.auth.signInWithPassword.mockRejectedValueOnce(new Error('Network error'));

      // Act
      const result = await login('test@example.com', 'password123');

      // Assert
      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual({
        success: false,
        data: null,
        error: 'Network error',
      });
    });

    it('should handle unexpected exceptions without message and return a default error message', async () => {
      // Arrange
      supabase.auth.signInWithPassword.mockRejectedValueOnce({});

      // Act
      const result = await login('test@example.com', 'password123');

      // Assert
      expect(supabase.auth.signInWithPassword).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
      expect(result).toEqual({
        success: false,
        data: null,
        error: 'An unexpected error occurred during login.',
      });
    });
  });
});
