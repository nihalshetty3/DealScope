from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.retrieval_service import search_similar_chunks
from app.services.llm_service import generate_answer

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
@router.post("/{deal_id}")
def ask_question(
    deal_id: int,
    question: str,
    db:Session = Depends(get_db)
):
    
    chunks = search_similar_chunks(
        db=db,
        deal_id=deal_id,
        query=question,
        limit=5,
    )
    
    answer = generate_answer(
        questions=question,
        chunks=chunks,
    )
    
    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "document_id": chunk["document_id"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    }