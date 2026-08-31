from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.embedding_service import generate_embedding


def search_similar_chunks(
    db: Session,
    query: str,
    deal_id: int,
    limit: int = 5,
):
    query_embedding = generate_embedding(query)

    sql = text("""
        SELECT
            id,
            document_id,
            chunk_index,
            content,
            page_number,
            embedding <=> CAST(:embedding AS vector) AS distance
        FROM document_chunks
        WHERE deal_id = :deal_id
          AND embedding IS NOT NULL
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """)

    result = db.execute(
        sql,
        {
            "embedding": str(query_embedding),
            "deal_id": deal_id,
            "limit": limit,
        },
    )

    return result.mappings().all()