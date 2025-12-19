import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "groq/llama-3.3-70b-versatile")

    MAX_TOKENS = 8000
    TEMPERATURE = 0.7

    CONVERSATION_TYPES = {
        "general": "General Legal Consultation",
        "contract_review": "Contract Review & Analysis",
        "legal_research": "Legal Research & Case Law",
        "document_drafting": "Document Drafting Assistance",
        "compliance": "Compliance & Regulatory Guidance",
        "risk_assessment": "Risk Assessment"
    }

    ANALYSIS_TYPES = {
        "contract_review": "Contract Review",
        "clause_extraction": "Clause Extraction",
        "risk_assessment": "Risk Assessment",
        "compliance_check": "Compliance Check",
        "legal_summary": "Legal Summary"
    }

config = Config()
