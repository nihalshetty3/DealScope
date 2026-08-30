from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends , File , HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.deal import Deal
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.document_service import (
    chunk_text,
    extract_text_from_pdf,
)

router = APIRouter(
    prefix="/deals",
    tags=["Documents"],
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
@router.post("/{deal_id}/documents")
async def upload_document(
    deal_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    
    deal = (
        db.query(Deal)
        .filter(Deal.id == deal_id)
        .first()
    )
    
    if deal is None:
        raise HTTPException(
            status_code=404,
            detail = "Deal not found",
        )
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )
    storage_dir = Path("storage/documents")
    storage_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    
    file_id = uuid4().hex
    filename = f"{file_id}_{file.filename}"

    file_path = storage_dir / filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    pages = extract_text_from_pdf(str(file_path))

    if not pages:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF",
        )

    document = Document(
        deal_id=deal_id,
        filename=file.filename,
        document_type="unknown",
        file_path=str(file_path),
    )

    db.add(document)
    db.flush()

    chunks = chunk_text(pages)

    for chunk in chunks:
        db_chunk = DocumentChunk(
            document_id=document.id,
            deal_id=deal_id,
            chunk_index=chunk["chunk_index"],
            content=chunk["content"],
            page_number=chunk["page_number"],
        )

        db.add(db_chunk)

    db.commit()
    db.refresh(document)

    return {
        "document_id": document.id,
        "filename": document.filename,
        "pages": len(pages),
        "chunks": len(chunks),
        "status": "processed",
    }