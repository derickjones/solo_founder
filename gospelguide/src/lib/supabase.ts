import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Server-side client with service role for admin operations
export const supabaseAdmin = createClient(
  supabaseUrl,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
)

// Types for our database
export interface Document {
  id: string
  content: string
  source_type: 'scripture' | 'conference' | 'manual' | 'saints'
  book?: string
  chapter?: number
  verse_start?: number
  verse_end?: number
  scripture_ref?: string
  speaker?: string
  title?: string
  session?: string
  conference_date?: string
  speaker_calling?: string
  conference_year?: number
  conference_month?: string
  volume?: number
  section_title?: string
  embedding?: number[]
  word_count?: number
  chunk_index?: number
  created_at?: string
  updated_at?: string
}

export interface User {
  id: string
  clerk_user_id: string
  email?: string
  subscription_tier: 'free' | 'monthly' | 'yearly' | 'lifetime'
  queries_used_today: number
  total_queries: number
  last_query_date: string
  stripe_customer_id?: string
  subscription_id?: string
  subscription_status?: string
  subscription_current_period_end?: string
  created_at?: string
  updated_at?: string
}

export interface Conversation {
  id: string
  user_id: string
  title: string
  mode: string
  created_at?: string
  updated_at?: string
}

export interface Message {
  id: string
  conversation_id: string
  role: 'user' | 'assistant'
  content: string
  sources?: any[]
  mode?: string
  tokens_used?: number
  created_at?: string
}

// Helper functions for common operations
export async function createUser(clerkUserId: string, email?: string) {
  const { data, error } = await supabase
    .from('users')
    .insert({
      clerk_user_id: clerkUserId,
      email,
      subscription_tier: 'free'
    })
    .select()
    .single()

  if (error) throw error
  return data as User
}

export async function getUserByClerkId(clerkUserId: string) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('clerk_user_id', clerkUserId)
    .single()

  if (error && error.code !== 'PGRST116') throw error
  return data as User | null
}

export async function checkUsageLimit(clerkUserId: string): Promise<boolean> {
  const { data, error } = await supabase
    .rpc('check_usage_limit', { user_clerk_id: clerkUserId })

  if (error) throw error
  return data as boolean
}

export async function incrementUsage(clerkUserId: string) {
  const { error } = await supabase
    .from('users')
    .update({
      queries_used_today: supabase.raw('queries_used_today + 1'),
      total_queries: supabase.raw('total_queries + 1'),
      last_query_date: new Date().toISOString().split('T')[0]
    })
    .eq('clerk_user_id', clerkUserId)

  if (error) throw error
}

export async function searchDocuments(
  queryEmbedding: number[],
  sourceType?: string,
  threshold = 0.78,
  limit = 10
) {
  const { data, error } = await supabase
    .rpc('match_documents', {
      query_embedding: queryEmbedding,
      match_threshold: threshold,
      match_count: limit,
      filter_source_type: sourceType
    })

  if (error) throw error
  return data as Document[]
}