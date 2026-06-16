import { describe, it, expect, vi, beforeEach } from 'vitest';
import { register } from './authService';
import { supabase } from '../lib/supabaseClient';

// Mock the Supabase client
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

  it('should return success response when registration is successful', async () => {
    const mockUser = { id: '123', email: 'test@example.com', user_metadata: { name: 'Test User' } };
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

  it('should return error response when supabase returns an error', async () => {
    const mockError = { message: 'User already exists' };
    supabase.auth.signUp.mockResolvedValueOnce({
      data: null,
      error: mockError,
    });

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(supabase.auth.signUp).toHaveBeenCalledTimes(1);
    expect(result).toEqual({
      success: false,
      data: null,
      error: 'User already exists',
    });
  });

  it('should return caught exception error message when an exception is thrown', async () => {
    supabase.auth.signUp.mockRejectedValueOnce(new Error('Network failure'));

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(supabase.auth.signUp).toHaveBeenCalledTimes(1);
    expect(result).toEqual({
      success: false,
      data: null,
      error: 'Network failure',
    });
  });

  it('should return generic error message when exception is thrown without message', async () => {
    supabase.auth.signUp.mockRejectedValueOnce('Unknown error');

    const result = await register('test@example.com', 'password123', 'Test User');

    expect(result).toEqual({
      success: false,
      data: null,
      error: 'An unexpected error occurred during registration.',
    });
  });
});
