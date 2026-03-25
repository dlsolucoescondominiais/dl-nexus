// src/services/authService.js
// This module provides authentication services using Supabase (v2 syntax).
// It includes functions for login, registration, logout, password reset, profile update, and getting the current user.
// All functions return a structured object: { success: boolean, data: any, error: string | null }

// Import Supabase client (assuming it's configured elsewhere)
import { supabase } from '../lib/supabaseClient'; // Ajustado para o nome do export default que criamos

export const login = async (email, password) => {
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) {
      return { success: false, data: null, error: error.message };
    }
    return { success: true, data: data.user, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred during login.' };
  }
};

export const register = async (email, password, name) => {
  try {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { name }, // Store name in user metadata
      }
    });
    if (error) {
      return { success: false, data: null, error: error.message };
    }
    return { success: true, data: data.user, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred during registration.' };
  }
};

export const logout = async () => {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) {
      return { success: false, data: null, error: error.message };
    }
    return { success: true, data: null, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred during logout.' };
  }
};

export const resetPassword = async (email) => {
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email);
    if (error) {
      return { success: false, data: null, error: error.message };
    }
    return { success: true, data: null, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred during password reset.' };
  }
};

export const updateProfile = async (updates) => {
  try {
    const { data, error } = await supabase.auth.updateUser({
      data: updates, // Update user metadata
    });
    if (error) {
      return { success: false, data: null, error: error.message };
    }
    return { success: true, data: data.user, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred during profile update.' };
  }
};

export const getCurrentUser = async () => {
  try {
    const { data: { session }, error } = await supabase.auth.getSession();
    if (error || !session) {
      return { success: false, data: null, error: error ? error.message : 'No user is currently authenticated.' };
    }
    return { success: true, data: session.user, error: null };
  } catch (err) {
    return { success: false, data: null, error: err.message || 'An unexpected error occurred while getting the current user.' };
  }
};
