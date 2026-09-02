from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.schemas.risk import RiskAnalysisResponse
from app.services.risk_service import analyze_deal_risk

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally: 
        db.close()
    
@router.post(
    "\{deal_id}/risks",
    response_model=RiskAnalysisResponse,
)

def analyze_risks(
    deal_id: int,
    db: Session= Depends(get_db),
):
    
    return analyze_deal_risk(
        db=db,
        deal_id=deal_id,
    )