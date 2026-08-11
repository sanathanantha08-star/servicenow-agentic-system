from pydantic import BaseModel, Field



class RcaResponse(BaseModel):
    ticket_id: str = Field(..., description="Unique identifier for the ticket associated with the root cause analysis")
    rca_summary: str = Field(..., description="Summary of the root cause analysis")
    
    recommendations: list[str] = Field(..., description="Recommendations for preventing similar issues in the future")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score of the root cause analysis, ranging from 0 to 1")
    kb_references: list[str] = Field(..., description="List of knowledge base references related to the root cause analysis")