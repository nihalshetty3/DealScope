from enum import Enum
from pydnatic import BaseModel, Field

class RiskSeverity(str , Enum):
    LOW="low",
    MEDIUM="MEDIUM",
    HIGH="HIGH",
    CRITICAL="CRITICAL"
    
class RiskCategory(str , Enum):
    FINANCIAL="Financial"
    LEGAL="Legal"
    OPERATIONAL="Operational"
    MARKET="Market"
    CUSTOMER = "Customer"
    TECHNOLOGY = "Technology"
    REGULATORY = "Regulatory"
    OTHER = "Other"
    
class Risk(BaseModel):
    category: RiskCategory
    severity: RiskSeverity
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    evidence: str = Field(min_length=1)
    document_id: int
    page_number: int | None=None
    chunk_index: int
    
class RiskAnalysisResponse(BaseModel):
    deal_id: int
    risks: list[Risk]