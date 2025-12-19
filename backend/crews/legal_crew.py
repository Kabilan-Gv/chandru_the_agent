from crewai import Crew, Process
from agents import LegalAgents
from tasks import LegalTasks
from typing import Dict, Any

class LegalCrew:
    """Main crew orchestrator for legal AI assistant"""

    def __init__(self):
        self.agents = LegalAgents()

    def analyze_document(self, document_content: str, document_type: str) -> str:
        """Analyze a legal document"""
        agent = self.agents.legal_analyst_agent()
        task = LegalTasks.analyze_document_task(agent, document_content, document_type)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def review_contract(self, contract_content: str, contract_type: str) -> str:
        """Review a contract comprehensively"""
        agent = self.agents.contract_reviewer_agent()
        task = LegalTasks.review_contract_task(agent, contract_content, contract_type)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def extract_clauses(self, contract_content: str) -> str:
        """Extract and categorize contract clauses"""
        agent = self.agents.contract_reviewer_agent()
        task = LegalTasks.extract_clauses_task(agent, contract_content)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def conduct_research(self, query: str, jurisdiction: str = "General") -> str:
        """Conduct legal research"""
        agent = self.agents.legal_researcher_agent()
        task = LegalTasks.legal_research_task(agent, query, jurisdiction)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def assess_compliance(self, business_context: str, industry: str) -> str:
        """Assess compliance requirements"""
        agent = self.agents.compliance_advisor_agent()
        task = LegalTasks.compliance_assessment_task(agent, business_context, industry)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def assess_risk(self, scenario: str, risk_type: str) -> str:
        """Assess legal risks"""
        agent = self.agents.risk_assessment_agent()
        task = LegalTasks.risk_assessment_task(agent, scenario, risk_type)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def general_consultation(self, question: str, context: str = "") -> str:
        """Provide general legal consultation"""
        agent = self.agents.legal_consultant_agent()
        task = LegalTasks.general_consultation_task(agent, question, context)

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)

    def comprehensive_contract_analysis(self, contract_content: str, contract_type: str) -> str:
        """Perform comprehensive contract analysis using multiple agents"""
        reviewer_agent = self.agents.contract_reviewer_agent()
        risk_agent = self.agents.risk_assessment_agent()

        review_task = LegalTasks.review_contract_task(reviewer_agent, contract_content, contract_type)
        risk_task = LegalTasks.risk_assessment_task(
            risk_agent,
            f"Contract review for {contract_type}",
            "Contractual Risk"
        )

        crew = Crew(
            agents=[reviewer_agent, risk_agent],
            tasks=[review_task, risk_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return str(result)
