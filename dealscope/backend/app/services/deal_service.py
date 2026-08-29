from sqlalchemy.orm import Session
from app.models.company import Company
from app.models.deal import Deal
from app.schemas.deal import DealCreate

def create_deal(db: Session, data:DealCreate) -> Deal:
    company = (
        db.query(Company)
        .filter(Company.name == data.company_name)
        .first()
    )
    
    if company is None:
        company = Company(
            name=data.company_name,
            ticker = data.ticker,
            industry=data.industry,
        )
        
        db.add(company)
        db.flush()
    deal = Deal(
        company_id = company.id,
        name=data.deal_name,
        status="active",
    )
    
    db.add(deal)
    db.commit()
    db.refresh(deal)
    
    return deal