import React from 'react';
import {
  MessageSquare,
  FileText,
  Search,
  ShieldCheck,
  AlertTriangle,
  Plus,
  Scale,
  LogOut,
  Menu,
  X
} from 'lucide-react';
import { Conversation, ConversationType } from '../../types';
import { useAuth } from '../../contexts/AuthContext';

interface SidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewConversation: (type: ConversationType) => void;
  isMobileMenuOpen: boolean;
  onToggleMobileMenu: () => void;
}

const conversationTypeIcons: Record<ConversationType, React.ReactNode> = {
  general: <MessageSquare className="w-4 h-4" />,
  contract_review: <FileText className="w-4 h-4" />,
  legal_research: <Search className="w-4 h-4" />,
  document_drafting: <FileText className="w-4 h-4" />,
  compliance: <ShieldCheck className="w-4 h-4" />,
  risk_assessment: <AlertTriangle className="w-4 h-4" />
};

export function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewConversation,
  isMobileMenuOpen,
  onToggleMobileMenu
}: SidebarProps) {
  const { signOut, user } = useAuth();

  const conversationTypes: { type: ConversationType; label: string }[] = [
    { type: 'general', label: 'General Consultation' },
    { type: 'contract_review', label: 'Contract Review' },
    { type: 'legal_research', label: 'Legal Research' },
    { type: 'compliance', label: 'Compliance Check' },
    { type: 'risk_assessment', label: 'Risk Assessment' }
  ];

  const handleNewConversation = (type: ConversationType) => {
    onNewConversation(type);
    if (window.innerWidth < 768) {
      onToggleMobileMenu();
    }
  };

  const handleSelectConversation = (id: string) => {
    onSelectConversation(id);
    if (window.innerWidth < 768) {
      onToggleMobileMenu();
    }
  };

  const sidebarContent = (
    <>
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Scale className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <h1 className="text-xl font-bold text-white">Legal AI</h1>
            <p className="text-xs text-slate-400 truncate">{user?.email}</p>
          </div>
        </div>

        <div className="space-y-2">
          {conversationTypes.map(({ type, label }) => (
            <button
              key={type}
              onClick={() => handleNewConversation(type)}
              className="w-full flex items-center gap-3 px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span className="text-sm font-medium">{label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 px-2">
          Recent Conversations
        </h2>
        <div className="space-y-1">
          {conversations.map((conversation) => (
            <button
              key={conversation.id}
              onClick={() => handleSelectConversation(conversation.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                activeConversationId === conversation.id
                  ? 'bg-slate-700 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              {conversationTypeIcons[conversation.conversation_type as ConversationType]}
              <span className="flex-1 text-left text-sm truncate">{conversation.title}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-slate-700">
        <button
          onClick={signOut}
          className="w-full flex items-center gap-3 px-4 py-3 text-slate-400 hover:bg-slate-800 hover:text-white rounded-lg transition-colors"
        >
          <LogOut className="w-4 h-4" />
          <span className="text-sm font-medium">Sign Out</span>
        </button>
      </div>
    </>
  );

  return (
    <>
      <button
        onClick={onToggleMobileMenu}
        className="md:hidden fixed top-4 left-4 z-50 bg-slate-800 p-2 rounded-lg text-white"
      >
        {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      <aside
        className={`
          fixed md:static inset-y-0 left-0 z-40
          w-80 bg-slate-800 border-r border-slate-700
          flex flex-col transform transition-transform duration-200 ease-in-out
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}
      >
        {sidebarContent}
      </aside>

      {isMobileMenuOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={onToggleMobileMenu}
        />
      )}
    </>
  );
}
