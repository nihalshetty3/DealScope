from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import engine

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
def health_check():
    return {
        "status":"healthy",
        "service":"DealScope"
    }
    
@router.get("/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error":str(e)
        }