from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Deal(Base):
    __tablename__="deals"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    company_id:Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )
    
    name:Mapped[str] = mapped_column(String(255) , nullable=False)
    
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    
    company = relationship(
        "Company",
        back_populates="deals",
    )
    
    documents=relationship(
        "Document",
        back_populates = "deal",
        cascade="all , delete-orphan",
    )