import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';
const supabaseServiceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';

// Lazy-init public client (avoids build-time crash when env vars are missing)
let _publicClient: SupabaseClient | null = null;
function getPublicClient(): SupabaseClient {
  if (!_publicClient) {
    if (!supabaseUrl || !supabaseAnonKey) {
      throw new Error('Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY');
    }
    _publicClient = createClient(supabaseUrl, supabaseAnonKey);
  }
  return _publicClient;
}

// Public client — safe for client-side, respects RLS
// Use getter so it doesn't explode at import time during build
export const supabase: SupabaseClient = new Proxy({} as SupabaseClient, {
  get(_, prop) {
    return (getPublicClient() as unknown as Record<string | symbol, unknown>)[prop];
  },
});

// Admin client — server-side only, bypasses RLS
let _adminClient: SupabaseClient | null = null;
export function getAdminClient(): SupabaseClient {
  if (!supabaseServiceRoleKey) {
    throw new Error('Missing SUPABASE_SERVICE_ROLE_KEY');
  }
  if (!_adminClient) {
    _adminClient = createClient(supabaseUrl, supabaseServiceRoleKey, {
      auth: { persistSession: false },
    });
  }
  return _adminClient;
}

// Backward compat
export const publicClient = supabase;
export const getSupabaseClient = (serviceRole = false) =>
  serviceRole ? getAdminClient() : supabase;
