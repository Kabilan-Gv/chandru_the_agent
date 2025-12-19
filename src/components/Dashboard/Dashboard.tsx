import React, { useState, useEffect } from 'react';
import { Sidebar } from '../Sidebar/Sidebar';
import { ChatInterface } from '../Chat/ChatInterface';
import { useAuth } from '../../contexts/AuthContext';
import { Conversation, Message, ConversationType } from '../../types';
import { supabase } from '../../lib/supabase';

const BACKEND_URL = 'http://localhost:8000';

export function Dashboard() {
  const { user } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (user) {
      loadConversations();
    }
  }, [user]);

  useEffect(() => {
    if (activeConversationId) {
      loadMessages(activeConversationId);
    }
  }, [activeConversationId]);

  const loadConversations = async () => {
    try {
      const { data, error } = await supabase
        .from('conversations')
        .select('*')
        .eq('user_id', user!.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setConversations(data || []);
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadMessages = async (conversationId: string) => {
    try {
      const { data, error } = await supabase
        .from('messages')
        .select('*')
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: true });

      if (error) throw error;
      setMessages(data || []);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const handleNewConversation = async (type: ConversationType) => {
    try {
      const { data, error } = await supabase
        .from('conversations')
        .insert({
          user_id: user!.id,
          title: `New ${type.replace('_', ' ')}`,
          conversation_type: type,
          status: 'active'
        })
        .select()
        .single();

      if (error) throw error;

      setConversations([data, ...conversations]);
      setActiveConversationId(data.id);
      setMessages([]);
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const handleSelectConversation = (id: string) => {
    setActiveConversationId(id);
  };

  const handleSendMessage = async (content: string) => {
    if (!activeConversationId || !user) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      conversation_id: activeConversationId,
      role: 'user',
      content,
      created_at: new Date().toISOString()
    };

    setMessages([...messages, userMessage]);
    setLoading(true);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: user.id,
          conversation_id: activeConversationId,
          message: content,
          conversation_type: conversations.find((c) => c.id === activeConversationId)
            ?.conversation_type || 'general'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        conversation_id: activeConversationId,
        role: 'assistant',
        content: data.response,
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev, assistantMessage]);

      const conversation = conversations.find((c) => c.id === activeConversationId);
      if (conversation && conversation.title.startsWith('New ')) {
        const { error } = await supabase
          .from('conversations')
          .update({ title: content.slice(0, 100) })
          .eq('id', activeConversationId);

        if (!error) {
          loadConversations();
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: crypto.randomUUID(),
        conversation_id: activeConversationId,
        role: 'assistant',
        content:
          'Sorry, I encountered an error. Please make sure the backend server is running at http://localhost:8000',
        created_at: new Date().toISOString()
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-900">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewConversation={handleNewConversation}
        isMobileMenuOpen={isMobileMenuOpen}
        onToggleMobileMenu={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      />

      <main className="flex-1 flex flex-col overflow-hidden">
        {activeConversationId ? (
          <ChatInterface
           messages={messages}
           onSendMessage={handleSendMessage}
           loading={loading}
           conversationType={
             conversations.find((c) => c.id === activeConversationId)?.conversation_type || 'general'
           }
           activeConversationId={activeConversationId}
           user={user}
           />
        ) : (
          <div className="flex-1 flex items-center justify-center px-4">
            <div className="text-center max-w-2xl">
              <h2 className="text-3xl font-bold text-white mb-4">Welcome to Legal AI Assistant</h2>
              <p className="text-slate-400 text-lg mb-8">
                Start a new conversation to get legal information, review contracts, conduct
                research, or assess compliance and risks.
              </p>
              <p className="text-slate-500 text-sm">
                This AI assistant provides legal information, not legal advice. Always consult with
                a licensed attorney for specific legal matters.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
