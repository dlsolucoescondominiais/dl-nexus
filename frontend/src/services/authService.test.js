import { describe, it, expect, vi, beforeEach } from 'vitest';
import { register } from './authService';
import { supabase } from '../lib/supabaseClient';

// Mock the supabase client
vi.mock('../lib/supabaseClient', () => {
  return {
    supabase: {
      auth: {
        signUp: vi.fn(),
      },
    },
  };
});

describe('authService', () => {
  describe('register', () => {
    beforeEach(() => {
      // Clear all mocks before each test
      vi.clearAllMocks();
    });

    it('should successfully register a new user', async () => {
      // Arrange
      const mockUser = { id: '123', email: 'test@example.com' };
      supabase.auth.signUp.mockResolvedValueOnce({
        data: { user: mockUser },
        error: null,
      });

      // Act
      const result = await register('test@example.com', 'password123', 'Test User');

      // Assert
      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
        options: {
          data: { name: 'Test User' },
        },
      });
      expect(result).toEqual({
        success: true,
        data: mockUser,
        error: null,
      });
    });

    it('should handle registration failure (Supabase error)', async () => {
      // Arrange
      const errorMessage = 'User already exists';
      supabase.auth.signUp.mockResolvedValueOnce({
        data: null,
        error: { message: errorMessage },
      });

      // Act
      const result = await register('existing@example.com', 'password123', 'Existing User');

      // Assert
      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: 'existing@example.com',
        password: 'password123',
        options: {
          data: { name: 'Existing User' },
        },
      });
      expect(result).toEqual({
        success: false,
        data: null,
        error: errorMessage,
      });
    });

    it('should handle unexpected errors during registration', async () => {
      // Arrange
      const errorMessage = 'Network error';
      supabase.auth.signUp.mockRejectedValueOnce(new Error(errorMessage));

      // Act
      const result = await register('test@example.com', 'password123', 'Test User');

      // Assert
      expect(result).toEqual({
        success: false,
        data: null,
        error: errorMessage,
      });
    });

    it('should handle unexpected errors without a specific message', async () => {
      // Arrange
      supabase.auth.signUp.mockRejectedValueOnce('Some strange error string');

      // Act
      const result = await register('test@example.com', 'password123', 'Test User');

      // Assert
      expect(result).toEqual({
        success: false,
        data: null,
        error: 'An unexpected error occurred during registration.',
      });
    });
  });
});
