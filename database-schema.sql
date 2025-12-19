/*
  # Legal AI Assistant Database Schema - 2025

  ## Overview
  Comprehensive database schema for a modern legal AI assistant with CrewAI backend integration.

  ## Tables Created

  ### 1. users_profile
  Extended user profile information beyond Supabase auth
  - user_id (references auth.users)
  - full_name, organization, role
  - subscription_tier, preferences
  - usage statistics

  ### 2. conversations
  Tracks all AI assistant conversations
  - conversation_id, user_id, title
  - conversation type (general, contract_review, legal_research, etc.)
  - status, timestamps

  ### 3. messages
  Individual messages within conversations
  - message_id, conversation_id
  - role (user, assistant, system)
  - content, tokens_used
  - timestamps

  ### 4. documents
  Legal documents uploaded by users
  - document_id, user_id
  - file_name, file_type, file_size
  - storage_path, processed status
  - document metadata (parties, dates, clauses)

  ### 5. document_analysis
  AI analysis results for documents
  - analysis_id, document_id
  - analysis_type (contract_review, clause_extraction, risk_assessment)
  - results (JSON with findings)
  - confidence scores

  ### 6. legal_research
  Legal research queries and results
  - research_id, user_id, conversation_id
  - query, jurisdiction
  - results (case law, statutes, precedents)
  - citations

  ### 7. clauses_library
  Extracted and categorized legal clauses
  - clause_id, document_id
  - clause_type, clause_text
  - risk_level, recommendations

  ### 8. agent_tasks
  CrewAI task tracking and results
  - task_id, user_id, conversation_id
  - agent_type, task_type
  - input_data, output_data
  - status, execution time

  ### 9. usage_analytics
  Track API usage and costs
  - analytics_id, user_id
  - tokens_used, cost
  - model_used, timestamp

  ## Security
  - RLS enabled on all tables
  - Users can only access their own data
  - Authenticated access required
*/

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Profile Table
CREATE TABLE IF NOT EXISTS users_profile (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  full_name text,
  organization text,
  role text,
  subscription_tier text DEFAULT 'free',
  preferences jsonb DEFAULT '{}',
  total_conversations integer DEFAULT 0,
  total_documents integer DEFAULT 0,
  total_tokens_used bigint DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE users_profile ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON users_profile FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile"
  ON users_profile FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile"
  ON users_profile FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Conversations Table
CREATE TABLE IF NOT EXISTS conversations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  title text NOT NULL,
  conversation_type text DEFAULT 'general',
  status text DEFAULT 'active',
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own conversations"
  ON conversations FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own conversations"
  ON conversations FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own conversations"
  ON conversations FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own conversations"
  ON conversations FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Messages Table
CREATE TABLE IF NOT EXISTS messages (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id uuid REFERENCES conversations(id) ON DELETE CASCADE NOT NULL,
  role text NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content text NOT NULL,
  tokens_used integer DEFAULT 0,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view messages from own conversations"
  ON messages FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = messages.conversation_id
      AND conversations.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert messages to own conversations"
  ON messages FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM conversations
      WHERE conversations.id = messages.conversation_id
      AND conversations.user_id = auth.uid()
    )
  );

-- Documents Table
CREATE TABLE IF NOT EXISTS documents (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  conversation_id uuid REFERENCES conversations(id) ON DELETE SET NULL,
  file_name text NOT NULL,
  file_type text NOT NULL,
  file_size bigint NOT NULL,
  storage_path text NOT NULL,
  processed boolean DEFAULT false,
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own documents"
  ON documents FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own documents"
  ON documents FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own documents"
  ON documents FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own documents"
  ON documents FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- Document Analysis Table
CREATE TABLE IF NOT EXISTS document_analysis (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id uuid REFERENCES documents(id) ON DELETE CASCADE NOT NULL,
  analysis_type text NOT NULL,
  results jsonb NOT NULL DEFAULT '{}',
  confidence_scores jsonb DEFAULT '{}',
  risk_assessment jsonb DEFAULT '{}',
  recommendations jsonb DEFAULT '[]',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE document_analysis ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view analysis of own documents"
  ON document_analysis FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM documents
      WHERE documents.id = document_analysis.document_id
      AND documents.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert analysis for own documents"
  ON document_analysis FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM documents
      WHERE documents.id = document_analysis.document_id
      AND documents.user_id = auth.uid()
    )
  );

-- Legal Research Table
CREATE TABLE IF NOT EXISTS legal_research (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  conversation_id uuid REFERENCES conversations(id) ON DELETE SET NULL,
  query text NOT NULL,
  jurisdiction text,
  research_type text,
  results jsonb DEFAULT '[]',
  citations jsonb DEFAULT '[]',
  summary text,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE legal_research ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own legal research"
  ON legal_research FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own legal research"
  ON legal_research FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Clauses Library Table
CREATE TABLE IF NOT EXISTS clauses_library (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id uuid REFERENCES documents(id) ON DELETE CASCADE,
  clause_type text NOT NULL,
  clause_text text NOT NULL,
  risk_level text DEFAULT 'low',
  recommendations text[],
  metadata jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now()
);

ALTER TABLE clauses_library ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view clauses from own documents"
  ON clauses_library FOR SELECT
  TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM documents
      WHERE documents.id = clauses_library.document_id
      AND documents.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can insert clauses for own documents"
  ON clauses_library FOR INSERT
  TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM documents
      WHERE documents.id = clauses_library.document_id
      AND documents.user_id = auth.uid()
    )
  );

-- Agent Tasks Table
CREATE TABLE IF NOT EXISTS agent_tasks (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  conversation_id uuid REFERENCES conversations(id) ON DELETE SET NULL,
  agent_type text NOT NULL,
  task_type text NOT NULL,
  input_data jsonb NOT NULL,
  output_data jsonb,
  status text DEFAULT 'pending',
  execution_time_ms integer,
  error_message text,
  created_at timestamptz DEFAULT now(),
  completed_at timestamptz
);

ALTER TABLE agent_tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own agent tasks"
  ON agent_tasks FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own agent tasks"
  ON agent_tasks FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own agent tasks"
  ON agent_tasks FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Usage Analytics Table
CREATE TABLE IF NOT EXISTS usage_analytics (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  tokens_used integer NOT NULL,
  cost decimal(10, 6),
  model_used text NOT NULL,
  operation_type text NOT NULL,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE usage_analytics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own usage analytics"
  ON usage_analytics FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own usage analytics"
  ON usage_analytics FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_documents_user_id ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_document_analysis_document_id ON document_analysis(document_id);
CREATE INDEX IF NOT EXISTS idx_legal_research_user_id ON legal_research(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_tasks_user_id ON agent_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_analytics_user_id ON usage_analytics(user_id);
CREATE INDEX IF NOT EXISTS idx_clauses_library_document_id ON clauses_library(document_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_users_profile_updated_at BEFORE UPDATE ON users_profile
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON conversations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_documents_updated_at BEFORE UPDATE ON documents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
