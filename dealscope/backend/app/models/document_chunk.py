from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer,Text
from sqlalchemy.orm import Mapped , mapped_column, relationship

from app.models.base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )
    
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id"),
        nullable=False,
    )
    
    chunk_index: Mapped[int]=mapped_column(
        Integer,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    page_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    document = relationship(
        "Document",
        back_populates="chunks",
    )