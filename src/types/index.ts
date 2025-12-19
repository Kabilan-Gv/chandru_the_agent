export interface User {
  id: string;
  email: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  tokens_used?: number;
  created_at: string;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  conversation_type: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  user_id: string;
  file_name: string;
  file_type: string;
  file_size: number;
  processed: boolean;
  created_at: string;
}

export interface DocumentAnalysis {
  id: string;
  document_id: string;
  analysis_type: string;
  results: any;
  created_at: string;
}

export type ConversationType =
  | 'general'
  | 'contract_review'
  | 'legal_research'
  | 'document_drafting'
  | 'compliance'
  | 'risk_assessment';

export type AnalysisType =
  | 'contract_review'
  | 'clause_extraction'
  | 'risk_assessment'
  | 'compliance_check'
  | 'document_analysis';
