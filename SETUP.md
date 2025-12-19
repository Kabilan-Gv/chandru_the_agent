# Legal AI Assistant Setup Guide

A comprehensive legal AI assistant built with CrewAI, Groq's Llama 3.3 70B model, React, and Supabase.

## Features

### 2025 Modern Legal AI Capabilities
- **General Legal Consultation**: Answer legal questions in plain English
- **Contract Review & Analysis**: Comprehensive contract review with risk assessment
- **Clause Extraction**: Automatically extract and categorize contract clauses
- **Legal Research**: Research legal topics, case law, and precedents
- **Compliance Assessment**: Assess regulatory compliance requirements
- **Risk Assessment**: Evaluate legal risks with mitigation strategies
- **Document Processing**: Support for PDF, DOCX, and TXT files
- **Multi-Agent Orchestration**: Specialized AI agents for different legal tasks
- **Real-time Chat Interface**: Beautiful, responsive chat UI
- **Conversation History**: Track and manage all legal consultations
- **Secure Authentication**: Built-in Supabase authentication

## Architecture

### Backend (Python + CrewAI)
- **CrewAI Framework**: Multi-agent orchestration
- **Groq LLM**: Fast inference with Llama 3.3 70B Versatile model
- **FastAPI**: Modern Python web framework
- **Supabase**: PostgreSQL database with real-time capabilities
- **Document Processing**: PDF, DOCX, TXT support

### Frontend (React + TypeScript)
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Supabase Client**: Real-time database and auth
- **Lucide Icons**: Beautiful icon library

### Specialized AI Agents
1. **Legal Analyst**: Document and contract analysis
2. **Contract Reviewer**: Contract review and clause extraction
3. **Legal Researcher**: Legal research and case law
4. **Compliance Advisor**: Compliance and regulatory guidance
5. **Risk Assessor**: Legal risk assessment
6. **Legal Consultant**: General legal consultation

## Prerequisites

- Python 3.10+
- Node.js 18+
- Groq API Key (get from https://console.groq.com)
- Supabase Account (get from https://supabase.com)

## Setup Instructions

### 1. Database Setup

1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy the entire contents of `database-schema.sql`
4. Execute the SQL to create all tables, policies, and indexes

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

5. Configure environment variables in `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here
   MODEL_NAME=groq/llama-3.3-70b-versatile
   ```
VITE_SUPABASE_URL=https://vrlsvdxhxtzrkifhzxys.supabase.co
   **Where to find these values:**
   - **GROQ_API_KEY**: Get from https://console.groq.com/keys
   - **SUPABASE_URL**: Found in Supabase Project Settings > API
   - **SUPABASE_SERVICE_KEY**: Found in Supabase Project Settings > API > service_role key (keep secret!)

6. Start the backend server:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### 3. Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. The `.env` file already exists with Supabase credentials

3. Start the development server:
   ```bash
   npm run dev
   ```

   The app will be available at the URL shown in the terminal

## Usage Guide

### First Time Setup

1. Open the application in your browser
2. Sign up with your email and password
3. You'll be automatically signed in

### Creating Conversations

Click one of the conversation type buttons:
- **General Consultation**: Ask any legal questions
- **Contract Review**: Review and analyze contracts
- **Legal Research**: Research legal topics and case law
- **Compliance Check**: Assess compliance requirements
- **Risk Assessment**: Evaluate legal risks

### Uploading Documents

Currently, document upload is available via API:
```bash
curl -X POST http://localhost:8000/api/upload-document \
  -F "user_id=YOUR_USER_ID" \
  -F "file=@contract.pdf"
```

### Analyzing Documents

After uploading, analyze via API:
```bash
curl -X POST http://localhost:8000/api/analyze-document \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "YOUR_USER_ID",
    "document_id": "DOCUMENT_ID",
    "analysis_type": "contract_review"
  }'
```

## API Endpoints

### Chat
- `POST /api/chat` - General legal consultation

### Documents
- `POST /api/upload-document` - Upload a legal document
- `POST /api/analyze-document` - Analyze a document
- `GET /api/documents/{user_id}` - Get user's documents

### Research & Analysis
- `POST /api/legal-research` - Conduct legal research
- `POST /api/compliance-assessment` - Assess compliance
- `POST /api/risk-assessment` - Assess risks

### Conversations
- `GET /api/conversations/{user_id}` - Get conversations
- `GET /api/messages/{conversation_id}` - Get messages

## Model Information

This application uses **Groq's Llama 3.3 70B Versatile** model:

- **Model ID**: `groq/llama-3.3-70b-versatile`
- **Context Window**: 8K tokens
- **Speed**: Extremely fast inference with Groq's LPU
- **Capabilities**: Superior performance on legal reasoning, coding, math, and instruction following
- **Cost**: Significantly lower cost than alternatives

## Important Legal Disclaimer

**This AI assistant provides legal information, NOT legal advice.**

- The information provided is for educational purposes only
- It does not create an attorney-client relationship
- Always consult with a licensed attorney for specific legal matters
- The AI may make mistakes or provide incomplete information
- Do not rely solely on AI-generated content for legal decisions

## Troubleshooting

### Backend Issues

**Error: "Missing Groq API Key"**
- Ensure `GROQ_API_KEY` is set in `backend/.env`
- Get your key from https://console.groq.com/keys

**Error: "Model has been decommissioned"**
- Ensure you're using `groq/llama-3.3-70b-versatile` (not 3.1)
- Update the `MODEL_NAME` in `.env`

**Database Connection Error**
- Verify `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in `.env`
- Ensure the database schema has been applied

### Frontend Issues

**Authentication Not Working**
- Check that Supabase credentials are correct in `.env`
- Verify email confirmation is disabled in Supabase Auth settings

**Messages Not Sending**
- Ensure backend is running at `http://localhost:8000`
- Check browser console for errors
- Verify CORS is enabled in backend

## Development

### Adding New Agents

1. Add agent definition in `backend/agents/legal_agents.py`
2. Create corresponding task in `backend/tasks/legal_tasks.py`
3. Add crew method in `backend/crews/legal_crew.py`
4. Create API endpoint in `backend/main.py`

### Adding New Features

Frontend features should be added as new components in `src/components/`

Backend features should be added as new endpoints in `backend/main.py`

## Production Deployment

### Backend Deployment
- Deploy to a service that supports Python (Railway, Render, Fly.io)
- Set environment variables in the hosting platform
- Update CORS settings to allow your frontend domain

### Frontend Deployment
- Update `BACKEND_URL` in `Dashboard.tsx` to your backend URL
- Deploy to Vercel, Netlify, or similar
- Set environment variables in the hosting platform

## Credits

Built with:
- CrewAI for multi-agent orchestration
- Groq for fast LLM inference
- Supabase for database and authentication
- React for the frontend
- FastAPI for the backend API

## License

This project is for educational purposes only.
