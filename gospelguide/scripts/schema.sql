-- GospelGuide Database Schema
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table with vector embeddings
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text NOT NULL,
  source_type text NOT NULL CHECK (source_type IN ('scripture', 'conference', 'manual', 'saints')),
  
  -- Scripture-specific fields
  book text,
  chapter integer,
  verse_start integer,
  verse_end integer,
  scripture_ref text, -- "1 Nephi 3:7"
  
  -- Conference-specific fields
  speaker text,
  title text,
  session text, -- "Saturday Morning Session"
  conference_date date,
  speaker_calling text, -- "President", "Elder", etc.
  conference_year integer,
  conference_month text, -- "April", "October"
  
  -- Manual/Saints specific
  volume integer,
  section_title text,
  
  -- Vector and metadata
  embedding vector(3072), -- OpenAI text-embedding-3-large
  word_count integer,
  chunk_index integer DEFAULT 0, -- for multi-chunk documents
  
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Users table for authentication and usage tracking
CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  clerk_user_id text UNIQUE NOT NULL,
  email text,
  subscription_tier text NOT NULL DEFAULT 'free' CHECK (subscription_tier IN ('free', 'monthly', 'yearly', 'lifetime')),
  
  -- Usage tracking
  queries_used_today integer DEFAULT 0,
  total_queries integer DEFAULT 0,
  last_query_date date DEFAULT CURRENT_DATE,
  
  -- Billing
  stripe_customer_id text,
  subscription_id text,
  subscription_status text,
  subscription_current_period_end timestamptz,
  
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Conversations for chat history
CREATE TABLE conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title text NOT NULL,
  mode text NOT NULL DEFAULT 'default',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Messages within conversations
CREATE TABLE messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id uuid NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role text NOT NULL CHECK (role IN ('user', 'assistant')),
  content text NOT NULL,
  
  -- AI response metadata
  sources jsonb, -- Array of document IDs used for response
  mode text, -- Mode used for this response
  tokens_used integer,
  
  created_at timestamptz DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_documents_source_type ON documents(source_type);
CREATE INDEX idx_documents_embedding ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_documents_scripture_ref ON documents(scripture_ref) WHERE source_type = 'scripture';
CREATE INDEX idx_documents_conference_date ON documents(conference_date) WHERE source_type = 'conference';
CREATE INDEX idx_users_clerk_id ON users(clerk_user_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_users_last_query_date ON users(last_query_date);

-- Functions for vector similarity search
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(3072),
  match_threshold float DEFAULT 0.78,
  match_count int DEFAULT 10,
  filter_source_type text DEFAULT NULL
)
RETURNS TABLE (
  id uuid,
  content text,
  source_type text,
  book text,
  chapter integer,
  verse_start integer,
  verse_end integer,
  scripture_ref text,
  speaker text,
  title text,
  session text,
  conference_date date,
  speaker_calling text,
  conference_year integer,
  conference_month text,
  similarity float
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    d.id,
    d.content,
    d.source_type,
    d.book,
    d.chapter,
    d.verse_start,
    d.verse_end,
    d.scripture_ref,
    d.speaker,
    d.title,
    d.session,
    d.conference_date,
    d.speaker_calling,
    d.conference_year,
    d.conference_month,
    1 - (d.embedding <=> query_embedding) as similarity
  FROM documents d
  WHERE (filter_source_type IS NULL OR d.source_type = filter_source_type)
    AND 1 - (d.embedding <=> query_embedding) > match_threshold
  ORDER BY d.embedding <=> query_embedding
  LIMIT match_count;
$$;

-- Function to reset daily usage
CREATE OR REPLACE FUNCTION reset_daily_usage()
RETURNS void
LANGUAGE SQL
AS $$
  UPDATE users 
  SET queries_used_today = 0 
  WHERE last_query_date < CURRENT_DATE;
$$;

-- Usage limits by tier
CREATE OR REPLACE FUNCTION check_usage_limit(user_clerk_id text)
RETURNS boolean
LANGUAGE plpgsql
AS $$
DECLARE
  user_record users%ROWTYPE;
  daily_limit integer;
BEGIN
  SELECT * INTO user_record FROM users WHERE clerk_user_id = user_clerk_id;
  
  IF NOT FOUND THEN
    RETURN FALSE;
  END IF;
  
  -- Set limits by tier
  CASE user_record.subscription_tier
    WHEN 'free' THEN daily_limit := 5;
    WHEN 'monthly' THEN daily_limit := 1000; -- Effectively unlimited
    WHEN 'yearly' THEN daily_limit := 1000;
    WHEN 'lifetime' THEN daily_limit := 1000;
    ELSE daily_limit := 5;
  END CASE;
  
  -- Reset usage if new day
  IF user_record.last_query_date < CURRENT_DATE THEN
    UPDATE users 
    SET queries_used_today = 0, last_query_date = CURRENT_DATE
    WHERE clerk_user_id = user_clerk_id;
    user_record.queries_used_today := 0;
  END IF;
  
  RETURN user_record.queries_used_today < daily_limit;
END;
$$;