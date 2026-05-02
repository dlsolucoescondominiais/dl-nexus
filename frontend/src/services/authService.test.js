import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  login,
  register,
  logout,
  resetPassword,
  updateProfile,
  getCurrentUser,
} from './authService';
import { supabase } from '../lib/supabaseClient';

// Mock the Supabase client
vi.mock('../lib/supabaseClient', () => {
  return {
    supabase: {
      auth: {
        signInWithPassword: vi.fn(),
        signUp: vi.fn(),
        signOut: vi.fn(),
        resetPasswordForEmail: vi.fn(),
        updateUser: vi.fn(),
        getSession: vi.fn(),
      },
    },
  };
});

describe('authService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('login', () => {
    it('should return user data on successful login', async () => {
      const mockUser = { id: 1, email: 'test@example.com' };
      supabase.auth.signInWithPassword.mockResolvedValueOnce({
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

    it('should return error on failed login', async () => {
      supabase.auth.signInWithPassword.mockResolvedValueOnce({
        data: null,
        error: { message: 'Invalid credentials' },
      });

      const result = await login('test@example.com', 'wrongpassword');

      expect(result).toEqual({ success: false, data: null, error: 'Invalid credentials' });
    });

    it('should catch unexpected errors during login', async () => {
      supabase.auth.signInWithPassword.mockRejectedValueOnce(new Error('Network Error'));

      const result = await login('test@example.com', 'password123');

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });

  describe('register', () => {
    it('should return user data on successful registration', async () => {
      const mockUser = { id: 1, email: 'test@example.com', user_metadata: { name: 'John Doe' } };
      supabase.auth.signUp.mockResolvedValueOnce({
        data: { user: mockUser },
        error: null,
      });

      const result = await register('test@example.com', 'password123', 'John Doe');

      expect(supabase.auth.signUp).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
        options: {
          data: { name: 'John Doe' },
        },
      });
      expect(result).toEqual({ success: true, data: mockUser, error: null });
    });

    it('should return error on failed registration', async () => {
      supabase.auth.signUp.mockResolvedValueOnce({
        data: null,
        error: { message: 'Email already exists' },
      });

      const result = await register('test@example.com', 'password123', 'John Doe');

      expect(result).toEqual({ success: false, data: null, error: 'Email already exists' });
    });

    it('should catch unexpected errors during registration', async () => {
      supabase.auth.signUp.mockRejectedValueOnce(new Error('Network Error'));

      const result = await register('test@example.com', 'password123', 'John Doe');

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });

  describe('logout', () => {
    it('should return success on successful logout', async () => {
      supabase.auth.signOut.mockResolvedValueOnce({ error: null });

      const result = await logout();

      expect(supabase.auth.signOut).toHaveBeenCalled();
      expect(result).toEqual({ success: true, data: null, error: null });
    });

    it('should return error on failed logout', async () => {
      supabase.auth.signOut.mockResolvedValueOnce({
        error: { message: 'Logout failed' },
      });

      const result = await logout();

      expect(result).toEqual({ success: false, data: null, error: 'Logout failed' });
    });

    it('should catch unexpected errors during logout', async () => {
      supabase.auth.signOut.mockRejectedValueOnce(new Error('Network Error'));

      const result = await logout();

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });

  describe('resetPassword', () => {
    it('should return success on successful password reset', async () => {
      supabase.auth.resetPasswordForEmail.mockResolvedValueOnce({ error: null });

      const result = await resetPassword('test@example.com');

      expect(supabase.auth.resetPasswordForEmail).toHaveBeenCalledWith('test@example.com');
      expect(result).toEqual({ success: true, data: null, error: null });
    });

    it('should return error on failed password reset', async () => {
      supabase.auth.resetPasswordForEmail.mockResolvedValueOnce({
        error: { message: 'User not found' },
      });

      const result = await resetPassword('test@example.com');

      expect(result).toEqual({ success: false, data: null, error: 'User not found' });
    });

    it('should catch unexpected errors during password reset', async () => {
      supabase.auth.resetPasswordForEmail.mockRejectedValueOnce(new Error('Network Error'));

      const result = await resetPassword('test@example.com');

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });

  describe('updateProfile', () => {
    it('should return user data on successful profile update', async () => {
      const mockUser = { id: 1, email: 'test@example.com', user_metadata: { name: 'Jane Doe' } };
      supabase.auth.updateUser.mockResolvedValueOnce({
        data: { user: mockUser },
        error: null,
      });

      const result = await updateProfile({ name: 'Jane Doe' });

      expect(supabase.auth.updateUser).toHaveBeenCalledWith({
        data: { name: 'Jane Doe' },
      });
      expect(result).toEqual({ success: true, data: mockUser, error: null });
    });

    it('should return error on failed profile update', async () => {
      supabase.auth.updateUser.mockResolvedValueOnce({
        data: null,
        error: { message: 'Update failed' },
      });

      const result = await updateProfile({ name: 'Jane Doe' });

      expect(result).toEqual({ success: false, data: null, error: 'Update failed' });
    });

    it('should catch unexpected errors during profile update', async () => {
      supabase.auth.updateUser.mockRejectedValueOnce(new Error('Network Error'));

      const result = await updateProfile({ name: 'Jane Doe' });

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });

  describe('getCurrentUser', () => {
    it('should return user data when session exists', async () => {
      const mockUser = { id: 1, email: 'test@example.com' };
      supabase.auth.getSession.mockResolvedValueOnce({
        data: { session: { user: mockUser } },
        error: null,
      });

      const result = await getCurrentUser();

      expect(supabase.auth.getSession).toHaveBeenCalled();
      expect(result).toEqual({ success: true, data: mockUser, error: null });
    });

    it('should return error when no session exists', async () => {
      supabase.auth.getSession.mockResolvedValueOnce({
        data: { session: null },
        error: null,
      });

      const result = await getCurrentUser();

      expect(result).toEqual({ success: false, data: null, error: 'No user is currently authenticated.' });
    });

    it('should return error when getSession fails', async () => {
      supabase.auth.getSession.mockResolvedValueOnce({
        data: { session: null },
        error: { message: 'Session error' },
      });

      const result = await getCurrentUser();

      expect(result).toEqual({ success: false, data: null, error: 'Session error' });
    });

    it('should catch unexpected errors during getSession', async () => {
      supabase.auth.getSession.mockRejectedValueOnce(new Error('Network Error'));

      const result = await getCurrentUser();

      expect(result).toEqual({ success: false, data: null, error: 'Network Error' });
    });
  });
});
