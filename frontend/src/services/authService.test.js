import { vi, describe, it, expect, beforeEach } from 'vitest';
import { register } from './authService';
import { supabase } from '../lib/supabaseClient';

vi.mock('../lib/supabaseClient', () => {
  return {
    supabase: {
      auth: {
        signUp: vi.fn(),
      },
    },
  };
});

describe('authService - register', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should register successfully and return user data', async () => {
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
    expect(result).toEqual({
      success: true,
      data: mockUser,
      error: null,
    });
  });

  it('should handle registration errors from supabase', async () => {
    const mockError = { message: 'Email already registered' };
    supabase.auth.signUp.mockResolvedValueOnce({
      data: { user: null },
      error: mockError,
    });

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(result).toEqual({
      success: false,
      data: null,
      error: 'Email already registered',
    });
  });

  it('should handle unexpected exceptions during registration', async () => {
    const mockError = new Error('Network error');
    supabase.auth.signUp.mockRejectedValueOnce(mockError);

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(result).toEqual({
      success: false,
      data: null,
      error: 'Network error',
    });
  });

  it('should handle exceptions without a message during registration', async () => {
    supabase.auth.signUp.mockRejectedValueOnce({});

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(result).toEqual({
      success: false,
      data: null,
      error: 'An unexpected error occurred during registration.',
    });
  });
});
