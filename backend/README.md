# Legal AI Assistant - Backend

A comprehensive legal AI assistant powered by CrewAI and Groq's Llama 3.3 70B model.

## Features

- **General Legal Consultation**: Answer legal questions in plain English
- **Contract Review**: Comprehensive contract analysis with risk assessment
- **Clause Extraction**: Extract and categorize contract clauses
- **Legal Research**: Conduct research on legal topics and case law
- **Compliance Assessment**: Assess regulatory compliance requirements
- **Risk Assessment**: Evaluate legal risks and provide mitigation strategies
- **Document Processing**: Support for PDF, DOCX, and TXT files

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_groq_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
MODEL_NAME=groq/llama-3.3-70b-versatile
```

### 3. Set Up Database

Apply the database schema from `../database-schema.sql` to your Supabase instance.

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Chat
- `POST /api/chat` - General legal consultation

### Documents
- `POST /api/upload-document` - Upload a legal document
- `POST /api/analyze-document` - Analyze a document
- `GET /api/documents/{user_id}` - Get user's documents

### Research & Analysis
- `POST /api/legal-research` - Conduct legal research
- `POST /api/compliance-assessment` - Assess compliance requirements
- `POST /api/risk-assessment` - Assess legal risks

### Conversations
- `GET /api/conversations/{user_id}` - Get user's conversations
- `GET /api/messages/{conversation_id}` - Get conversation messages

## Architecture

### Agents
- **Legal Analyst**: Document and contract analysis
- **Contract Reviewer**: Contract review and clause extraction
- **Legal Researcher**: Legal research and case law
- **Compliance Advisor**: Compliance and regulatory guidance
- **Risk Assessor**: Legal risk assessment
- **Legal Consultant**: General legal consultation

### Tasks
Each agent has specialized tasks optimized for their role, powered by CrewAI's task orchestration.

### Tools
- **Document Processor**: Extract text from PDF, DOCX, and TXT files

## Model Configuration

This backend uses Groq's Llama 3.3 70B Versatile model:
- Model: `groq/llama-3.3-70b-versatile`
- Fast inference with Groq's LPU architecture
- Superior performance on legal reasoning and analysis
- Excellent tool use and instruction following

## Notes

- All responses are for informational purposes only
- Users should consult licensed attorneys for specific legal matters
- The system provides legal information, not legal advice
