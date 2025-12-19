import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Message } from '../../types';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  loading: boolean;
  conversationType: string;
  activeConversationId: string | null;
  user: any;
}

export function ChatInterface({
  messages,
  onSendMessage,
  loading,
  conversationType,
  activeConversationId,
  user
}: ChatInterfaceProps) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const messageContent = input;
    setInput('');
    await onSendMessage(messageContent);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-6">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md">
              <h3 className="text-2xl font-semibold text-slate-300 mb-4">
                How can I assist you today?
              </h3>
              <p className="text-slate-400">
                Ask me about contracts, legal documents, compliance, or any legal questions you have.
              </p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-3xl rounded-2xl px-6 py-4 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-700 text-slate-100'
                  }`}
                >
                  <div className="whitespace-pre-wrap break-words">{message.content}</div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-700 text-slate-100 rounded-2xl px-6 py-4">
                  <Loader2 className="w-5 h-5 animate-spin" />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {conversationType === 'contract_review' && (
  <div className="p-4 border-b border-slate-700 bg-slate-800">
    <h3 className="text-sm font-medium text-white mb-2">Upload Contract Document (PDF or DOCX)</h3>
    <input
      type="file"
      accept=".pdf,.doc,.docx"
      onChange={async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);
        formData.append("user_id", user?.id || "");
        formData.append("conversation_id", activeConversationId || "");

        try {
          const res = await fetch("http://localhost:8000/api/upload-document", {
            method: "POST",
            body: formData,
          });

          const data = await res.json();
          if (res.ok) {
            alert(`File uploaded successfully: ${data.file_name}`);
          } else {
            alert(`Upload failed: ${data.detail || "Unknown error"}`);
          }
        } catch (err) {
          console.error("Upload error:", err);
          alert("Upload failed. Check console for details.");
        }
      }}
      className="block w-full text-sm text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-700"
    />
  </div>
)}


      <div className="border-t border-slate-700 px-4 py-4 bg-slate-800">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="flex gap-4">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a legal question..."
              className="flex-1 px-4 py-3 bg-slate-900 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
