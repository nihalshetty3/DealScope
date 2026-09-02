import json
from google import genai 

from app.score.config import settings
from app.services.retrieval_service import search_similar_chunks
from app.services.rerank_service import rerank_chunks
from app.schemas.risk import RiskAnalysisResponse

client =  genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def analyze_deal_risk(
    db,
    deal_id: int,
) -> RiskAnalysisResponse:

    chunks = search_similar_chunks(
        db=db,
        deal_id=deal_id,
        query=(
            "Identify financial, legal, operational, market, "
            "customer, technology, and regulatory risks, "
            "red flags, weaknesses, liabilities, dependencies, "
            "and potential issues in this M&A deal."
        ),
        limit=0,
    )
    
    if not chunks:
        return RiskAnalysisResponse(
            deal_id=deal_id,
            risks=[],
        )
    
    chunks = rerank_chunks(
        query=(
           "M&A due diligence risks, financial risks, "
            "legal risks, operational risks, liabilities, "
            "customer concentration, regulatory issues, "
            "market risks and red flags" 
        ),
        chunks=chunks,
        top_k=10,
    )
    
    context_parts=[]
    for chunk in chunks:
        context_parts.append(
            f"""
Document ID: {chunk["document_id"]}
Page Number: {chunk["page_number"]}
Chunk Index: {chunk["chunk_index"]}

Context:
{chunk["content"]}
"""
        )
    context = "\n".join(context_parts)
    
    prompt = f"""

You are DealScope, an M&A due-diligence analysis assistant.

Analyze the provided document evidence and identify meaningful
risks and red flags that could affect an acquisition decision.

IMPORTANT RULES:

1. Use ONLY the provided document evidence.
2. Do not invent facts, numbers, risks, or sources.
3. Every risk must be supported by evidence from the provided chunks.
4. Include the document_id, page_number, and chunk_index that support
   each risk.
5. If there is no meaningful evidence for a potential risk, do not
   report it.
6. Avoid duplicate risks.
7. Focus on actionable M&A due-diligence risks.
8. Severity must be one of:
   LOW, MEDIUM, HIGH, CRITICAL.
9. Category must be one of:
   Financial, Legal, Operational, Market, Customer, Technology,
   Regulatory, Other.

Look for things such as:

- declining revenue or profitability
- high debt or leverage
- negative cash flow
- customer concentration
- supplier concentration
- pending litigation
- regulatory problems
- intellectual property issues
- operational dependencies
- employee/key-person dependencies
- market contraction
- competitive threats
- technology risks
- unusual financial trends
- material liabilities
- contract risks
- other acquisition-related red flags

Return ONLY valid JSON.

The JSON must have exactly this structure:

{{
    "risks": [
        {{
            "category": "Financial",
            "severity": "HIGH",
            "title": "Short risk title",
            "description": "Explain why this is a risk.",
            "evidence": "Quote or summarize the supporting evidence.",
            "document_id": 1,
            "page_number": 42,
            "chunk_index": 7
        }}
    ]
}}

If no meaningful risks are found, return:

{{
    "risks": []
}}

DOCUMENT EVIDENCE:

{context}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON: {response.text}"
        ) from exc 
    return RiskAnalysisResponse(
        deal_id=deal_id,
        risks=data.get("risks", []),
    )