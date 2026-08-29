from fastapi import FastAPI
from app.core.config import settings
from app.api.health import router as health_router
from app.api.deals import router as deals_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic AI & M&A Due-Diligence Copilot"
)

app.include_router(health_router)
app.include_router(deals_router)
@app.get("/")
def root():
    return{
        "message": "Welcome to DealScope",
        "version": settings.APP_VERSION
    }