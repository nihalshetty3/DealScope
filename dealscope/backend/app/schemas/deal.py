from pydantic import BaseModel, Field
class DealCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=255)
    ticker: str | None = Field(default=None , max_length=20)
    industry: str | None=Field(default=None , max_length=100)
    deal_name: str = Field(min_length=1 , max_length=255)
    
class DealResponse(BaseModel):
    id: int
    company_id: int
    name:str
    status: str
    
    model_config = {
        "from_attributes": True
    }