from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.retrieval_service import search_similar_chunks
from app.schemas.search import SearchResponse, SearchResult

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
@router.get("/{deal_id}" , response_model=SearchResponse)
def search_documents(
    deal_id: int,
    query: str,
    limit: int=5,
    db: Session = Depends(get_db),
):
    
    results = search_similar_chunks(
        db=db,
        deal_id=deal_id,
        query=query,
        limit=limit,
    )
    
    return SearchResponse(
        results=[
            SearchResult(
                id=row["id"],
                document_id=row["document_id"],
                chunk_index=row["chunk_index"],
                content=row["content"],
                page_number=row["page_number"],
                distance=float(row["distance"]),
            )
            for row in results
        ]
    )