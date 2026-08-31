from google import genai
from app.core.config import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)

def generate_answer(questions: str , chunks: list[dict]) -> str:
    
    context_parts = []
    for chunk in chunks:
        context_parts.append(
            f"""
Document ID: {chunk["document_id"]}
Page: {chunk["page_number"]}
Chunk: {chunk["chunk_index"]}

Content:
{chunk["content"]}
"""
        )
    context = "\n".join(context_parts)
    prompt = f"""
You are DealScope, an M&A due-diligence assistant.

Answer the user's question using ONLY the provided document context.

If the answer cannot be found in the context, say:
"I could not find sufficient information in the provided documents."

Do not invent facts or numbers.

Always mention the relevant document page when possible.

Question:
{questions}

Document Context:
{context}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text