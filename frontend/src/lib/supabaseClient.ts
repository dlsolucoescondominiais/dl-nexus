// Import the Supabase client library
import { createClient } from '@supabase/supabase-js';

// Retrieve Supabase URL and anonymous key from environment variables
// Note: In React, environment variables must be prefixed with REACT_APP_
const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

// Basic error handling: Check if environment variables are defined
if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing required Supabase environment variables: REACT_APP_SUPABASE_URL and REACT_APP_SUPABASE_ANON_KEY');
}

// Create a singleton Supabase client instance
const supabaseClient = createClient(supabaseUrl, supabaseAnonKey);

// Export the client as default for use in other parts of the application
export default supabaseClient;
