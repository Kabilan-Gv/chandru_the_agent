from crewai import Task
from typing import Dict, Any

class LegalTasks:
    @staticmethod
    def analyze_document_task(agent, document_content: str, document_type: str) -> Task:
        """Task for analyzing legal documents"""
        return Task(
            description=f"""Analyze the following {document_type} document and provide a comprehensive analysis:

Document Content:
{document_content}

Your analysis should include:
1. Document Overview: Brief summary of the document type and purpose
2. Key Parties: Identify all parties involved
3. Main Terms: Extract and explain key terms and conditions
4. Important Dates: List all critical dates, deadlines, and time periods
5. Key Obligations: Outline primary obligations of each party
6. Notable Clauses: Highlight any unusual or important clauses
7. Plain English Summary: Provide a clear, non-technical summary

Format your response in a structured, easy-to-read manner.""",
            agent=agent,
            expected_output="A detailed analysis of the document including overview, parties, terms, dates, obligations, notable clauses, and plain English summary"
        )

    @staticmethod
    def review_contract_task(agent, contract_content: str, contract_type: str) -> Task:
        """Task for contract review and risk assessment"""
        return Task(
            description=f"""Review the following {contract_type} contract and provide a detailed assessment:

Contract Content:
{contract_content}

Your review should include:
1. Contract Type & Purpose: Identify the contract type and its purpose
2. Parties & Roles: List all parties and their roles
3. Key Terms Analysis:
   - Payment terms
   - Duration and termination conditions
   - Deliverables or performance obligations
   - Warranties and representations
4. Risk Assessment:
   - HIGH RISK clauses (could cause significant problems)
   - MEDIUM RISK clauses (require attention)
   - LOW RISK clauses (standard terms)
5. Missing Protections: Identify any important protections that should be included
6. Unfavorable Terms: Flag terms that may be one-sided or unfair
7. Recommendations: Provide specific recommendations for improvement

Rate the overall contract risk as: LOW, MEDIUM, or HIGH.""",
            agent=agent,
            expected_output="A comprehensive contract review including risk assessment, problematic clauses, missing protections, and specific recommendations"
        )

    @staticmethod
    def extract_clauses_task(agent, contract_content: str) -> Task:
        """Task for extracting and categorizing contract clauses"""
        return Task(
            description=f"""Extract and categorize all important clauses from the following contract:

Contract Content:
{contract_content}

Identify and extract the following clause types:
1. Payment & Financial Clauses
2. Term & Termination Clauses
3. Liability & Indemnification Clauses
4. Confidentiality & Non-Disclosure Clauses
5. Intellectual Property Clauses
6. Dispute Resolution Clauses
7. Warranty & Representation Clauses
8. Force Majeure Clauses
9. Non-Compete & Non-Solicitation Clauses
10. Governing Law & Jurisdiction Clauses

For each clause found:
- Quote the actual clause text
- Explain what it means in plain English
- Assess its fairness (Favorable/Neutral/Unfavorable)
- Note any concerns or recommendations""",
            agent=agent,
            expected_output="A categorized list of all important clauses with explanations, fairness assessments, and recommendations"
        )

    @staticmethod
    def legal_research_task(agent, query: str, jurisdiction: str = "General") -> Task:
        """Task for conducting legal research"""
        return Task(
            description=f"""Conduct comprehensive legal research on the following query:

Query: {query}
Jurisdiction: {jurisdiction}

Your research should include:
1. Legal Framework: Explain the relevant legal framework and applicable laws
2. Key Legal Principles: Identify and explain key legal principles
3. Relevant Case Law: Reference important cases and precedents (if applicable)
4. Statutory Provisions: Cite relevant statutes and regulations
5. Current Trends: Discuss any recent developments or trends in this area
6. Practical Implications: Explain practical implications and considerations
7. Recommendations: Provide guidance based on the research

Note: While this research is comprehensive, it is for informational purposes only
and should not be considered legal advice. Consult with a licensed attorney for
specific legal matters.""",
            agent=agent,
            expected_output="A thorough legal research report with legal framework, principles, case law, statutes, trends, and practical guidance"
        )

    @staticmethod
    def compliance_assessment_task(agent, business_context: str, industry: str) -> Task:
        """Task for assessing compliance requirements"""
        return Task(
            description=f"""Assess compliance requirements for the following business context:

Business Context: {business_context}
Industry: {industry}

Your compliance assessment should cover:
1. Regulatory Framework: Identify applicable regulations and standards
2. Key Compliance Requirements: List main compliance obligations
3. Industry-Specific Requirements: Highlight industry-specific regulations
4. Data Privacy & Security: Address data protection requirements (GDPR, CCPA, etc.)
5. Employment & Labor Laws: Cover relevant employment compliance
6. Financial & Tax Compliance: Note financial reporting and tax obligations
7. Compliance Gaps: Identify potential compliance gaps or risks
8. Recommended Actions: Provide a prioritized action plan

Rate compliance complexity as: LOW, MEDIUM, or HIGH.""",
            agent=agent,
            expected_output="A comprehensive compliance assessment with regulatory requirements, gaps, risks, and prioritized action plan"
        )

    @staticmethod
    def risk_assessment_task(agent, scenario: str, risk_type: str) -> Task:
        """Task for assessing legal risks"""
        return Task(
            description=f"""Assess legal risks for the following scenario:

Scenario: {scenario}
Risk Type: {risk_type}

Your risk assessment should include:
1. Risk Identification: Identify all potential legal risks
2. Risk Analysis:
   - Likelihood (Low/Medium/High)
   - Impact (Low/Medium/High)
   - Overall Risk Rating (Low/Medium/High/Critical)
3. Detailed Risk Breakdown: Analyze each identified risk
4. Potential Consequences: Describe possible outcomes if risks materialize
5. Mitigation Strategies: Provide specific risk mitigation recommendations
6. Best Practices: Suggest industry best practices to minimize risks
7. Action Plan: Create a prioritized action plan

Prioritize risks by severity and provide clear, actionable recommendations.""",
            agent=agent,
            expected_output="A detailed risk assessment with identified risks, ratings, consequences, mitigation strategies, and prioritized action plan"
        )

    @staticmethod
    def general_consultation_task(agent, question: str, context: str = "") -> Task:
        """Task for general legal consultation"""
        additional_context = f"\n\nAdditional Context: {context}" if context else ""

        return Task(
            description=f"""Provide clear, helpful guidance on the following legal question:

Question: {question}{additional_context}

Your response should:
1. Address the Question: Provide a direct answer to the question
2. Explain the Law: Explain relevant legal principles and concepts
3. Consider Different Scenarios: Discuss various situations or interpretations
4. Practical Guidance: Offer practical advice and considerations
5. Next Steps: Suggest appropriate next steps
6. Important Disclaimers: Clarify limitations and when to seek legal counsel

Remember to:
- Explain legal concepts in plain, accessible language
- Avoid excessive legal jargon
- Be clear this is information, not legal advice
- Recommend consulting a licensed attorney for specific legal matters
- Be thorough but concise""",
            agent=agent,
            expected_output="A clear, comprehensive response addressing the legal question with explanations, practical guidance, and appropriate disclaimers"
        )
