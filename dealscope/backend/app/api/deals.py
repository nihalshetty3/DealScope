from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.deal import DealCreate, DealResponse
from app.services.deal_service import create_deal

router = APIRouter(
    prefix="/deals",
    tags=["Deals"],
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
@router.post("", response_model=DealResponse)
def create_new_deal(
    data:DealCreate,
    db: Session = Depends(get_db),
):
    return create_deal(db , data)