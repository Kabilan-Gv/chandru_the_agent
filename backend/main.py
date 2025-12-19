from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
from datetime import datetime
from supabase import create_client, Client

from config import config
from crews import LegalCrew
from tools import DocumentProcessor

app = FastAPI(title="Legal AI Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_SERVICE_KEY)
legal_crew = LegalCrew()

class ChatRequest(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    message: str
    conversation_type: str = "general"
    context: Optional[str] = None

class DocumentAnalysisRequest(BaseModel):
    user_id: str
    document_id: str
    analysis_type: str

class ResearchRequest(BaseModel):
    user_id: str
    conversation_id: Optional[str] = None
    query: str
    jurisdiction: Optional[str] = "General"

class ComplianceRequest(BaseModel):
    user_id: str
    business_context: str
    industry: str

class RiskAssessmentRequest(BaseModel):
    user_id: str
    scenario: str
    risk_type: str

@app.get("/")
async def root():
    return {
        "message": "Legal AI Assistant API",
        "version": "1.0.0",
        "model": config.MODEL_NAME
    }

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle general legal consultation chat"""
    try:
        conversation_id = request.conversation_id

        if not conversation_id:
            conversation_data = {
                "user_id": request.user_id,
                "title": request.message[:100],
                "conversation_type": request.conversation_type,
                "created_at": datetime.utcnow().isoformat()
            }
            result = supabase.table("conversations").insert(conversation_data).execute()
            conversation_id = result.data[0]["id"]

        user_message_data = {
            "conversation_id": conversation_id,
            "role": "user",
            "content": request.message,
            "created_at": datetime.utcnow().isoformat()
        }
        supabase.table("messages").insert(user_message_data).execute()

        response = legal_crew.general_consultation(request.message, request.context or "")

        assistant_message_data = {
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": response,
            "created_at": datetime.utcnow().isoformat()
        }
        supabase.table("messages").insert(assistant_message_data).execute()

        return {
            "conversation_id": conversation_id,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-document")
async def upload_document(
    user_id: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """Upload and process a legal document"""
    try:
        file_bytes = await file.read()
        file_type = file.content_type

        processed = DocumentProcessor.process_document(file_bytes, file_type)

        document_data = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "file_name": file.filename,
            "file_type": file_type,
            "file_size": len(file_bytes),
            "storage_path": f"documents/{user_id}/{file.filename}",
            "processed": True,
            "metadata": {
                "word_count": processed["word_count"],
                "char_count": processed["char_count"]
            },
            "created_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("documents").insert(document_data).execute()
        document_id = result.data[0]["id"]

        return {
            "document_id": document_id,
            "file_name": file.filename,
            "text": processed["text"],
            "metadata": document_data["metadata"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-document")
async def analyze_document(request: DocumentAnalysisRequest):
    """Analyze a document using AI agents"""
    try:
        doc_result = supabase.table("documents").select("*").eq("id", request.document_id).execute()

        if not doc_result.data:
            raise HTTPException(status_code=404, detail="Document not found")

        document = doc_result.data[0]

        analysis_type = request.analysis_type

        if analysis_type == "contract_review":
            response = legal_crew.review_contract(
                document.get("text", ""),
                document.get("file_type", "contract")
            )
        elif analysis_type == "clause_extraction":
            response = legal_crew.extract_clauses(document.get("text", ""))
        elif analysis_type == "document_analysis":
            response = legal_crew.analyze_document(
                document.get("text", ""),
                document.get("file_type", "document")
            )
        else:
            response = legal_crew.analyze_document(
                document.get("text", ""),
                document.get("file_type", "document")
            )

        analysis_data = {
            "document_id": request.document_id,
            "analysis_type": analysis_type,
            "results": {"analysis": response},
            "created_at": datetime.utcnow().isoformat()
        }

        supabase.table("document_analysis").insert(analysis_data).execute()

        return {
            "document_id": request.document_id,
            "analysis_type": analysis_type,
            "analysis": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/legal-research")
async def legal_research(request: ResearchRequest):
    """Conduct legal research"""
    try:
        response = legal_crew.conduct_research(request.query, request.jurisdiction)

        research_data = {
            "user_id": request.user_id,
            "conversation_id": request.conversation_id,
            "query": request.query,
            "jurisdiction": request.jurisdiction,
            "results": {"research": response},
            "summary": response[:500],
            "created_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("legal_research").insert(research_data).execute()

        return {
            "research_id": result.data[0]["id"],
            "query": request.query,
            "jurisdiction": request.jurisdiction,
            "research": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compliance-assessment")
async def compliance_assessment(request: ComplianceRequest):
    """Assess compliance requirements"""
    try:
        response = legal_crew.assess_compliance(request.business_context, request.industry)

        return {
            "business_context": request.business_context,
            "industry": request.industry,
            "assessment": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/risk-assessment")
async def risk_assessment(request: RiskAssessmentRequest):
    """Assess legal risks"""
    try:
        response = legal_crew.assess_risk(request.scenario, request.risk_type)

        task_data = {
            "user_id": request.user_id,
            "agent_type": "risk_assessment",
            "task_type": request.risk_type,
            "input_data": {
                "scenario": request.scenario,
                "risk_type": request.risk_type
            },
            "output_data": {"assessment": response},
            "status": "completed",
            "created_at": datetime.utcnow().isoformat()
        }

        supabase.table("agent_tasks").insert(task_data).execute()

        return {
            "scenario": request.scenario,
            "risk_type": request.risk_type,
            "assessment": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{user_id}")
async def get_conversations(user_id: str):
    """Get all conversations for a user"""
    try:
        result = supabase.table("conversations").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

        return {
            "conversations": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages/{conversation_id}")
async def get_messages(conversation_id: str):
    """Get all messages in a conversation"""
    try:
        result = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()

        return {
            "messages": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{user_id}")
async def get_documents(user_id: str):
    """Get all documents for a user"""
    try:
        result = supabase.table("documents").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

        return {
            "documents": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
