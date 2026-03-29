from pydantic import BaseModel, Field
from typing import List, Optional

# --- REQUEST SCHEMAS ---
class BusinessInput(BaseModel):
    business_name: str = Field(..., example="Sharma Manufacturing Works")
    gstin: str = Field(..., example="07AAAAA1234A1Z5")
    vintage_years: float = Field(..., ge=0, example=4.5)
    industry_type: str = Field(..., example="Manufacturing")

# --- RESPONSE SCHEMAS ---
class FactorBreakdown(BaseModel):
    cash_flow_stability: int
    business_vintage: int
    gst_compliance: int
    debt_coverage: int
    digital_footprint: int

class ScoreResponse(BaseModel):
    user_id: int
    total_score: int = Field(..., ge=0, le=850)
    breakdown: FactorBreakdown
    risk_tier: str = Field(..., example="Low Risk")

class Insight(BaseModel):
    category: str
    observation: str
    action_plan_90_days: str

class LenderMatch(BaseModel):
    lender_name: str
    lender_type: str
    max_loan_amount: float
    interest_rate_range: str

class FullReportResponse(BaseModel):
    score_data: ScoreResponse
    insights: List[Insight]
    eligible_lenders: List[LenderMatch]
