from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import BusinessInput, ScoreResponse, FullReportResponse

# Importing all the custom engines we just built
from app.services.scorer import CreditScoringEngine
from app.services.insights import InsightEngine
from app.services.matcher import LenderMatchEngine

router = APIRouter()

@router.post("/upload-statement", summary="Upload Bank Statement & Sync GST")
async def upload_statement(
    file: UploadFile = File(...),
    business_name: str = Form(...),
    gstin: str = Form(...),
    vintage_years: float = Form(...)
):
    """
    Accepts a PDF/CSV bank statement and basic business details.
    """
    if not file.filename.endswith(('.pdf', '.csv')):
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported.")
    
    # Placeholder for Phase 4: Parser Service execution
    return {
        "status": "success", 
        "message": f"File {file.filename} processed successfully.",
        "simulated_data_extraction": "Pending Database Linkage"
    }

@router.post("/calculate-score", response_model=ScoreResponse, summary="Generate Credit Readiness Score")
async def calculate_score(user_data: BusinessInput):
    """
    Triggers the scoring engine standalone. 
    (Useful if the frontend just wants to show the score before the full report).
    """
    mock_parsed_data = {
        "monthly_revenue": 150000.0,
        "cash_flow_volatility_pct": 25.0,
        "estimated_monthly_emi": 30000.0
    }
    
    result = CreditScoringEngine.calculate_crs(
        parsed_financials=mock_parsed_data, 
        user_inputs=user_data.model_dump() 
    )
    
    return {
        "user_id": 1,
        "total_score": result["total_score"],
        "breakdown": result["breakdown"],
        "risk_tier": result["risk_tier"]
    }

@router.post("/get-report", response_model=FullReportResponse, summary="Generate Complete Credit Intelligence Report")
async def generate_full_report(user_data: BusinessInput):
    """
    The Master Orchestrator. 
    Takes MSME inputs, calculates the score, drafts insights, and finds lenders in one payload.
    """
    # 1. Simulate parsed financial data
    mock_parsed_data = {
        "monthly_revenue": 250000.0,      # ₹2.5 Lakhs/month -> ₹30L Annual
        "cash_flow_volatility_pct": 25.0,
        "estimated_monthly_emi": 30000.0
    }
    
    # 2. Generate the Score
    score_result = CreditScoringEngine.calculate_crs(
        parsed_financials=mock_parsed_data, 
        user_inputs=user_data.model_dump()
    )
    
    # 3. Generate Actionable Insights
    insights_list = InsightEngine.generate(breakdown=score_result["breakdown"])
    
    # 4. Find Eligible Lenders
    lender_matches = LenderMatchEngine.find_eligible_lenders(
        user_score=score_result["total_score"],
        monthly_revenue=mock_parsed_data["monthly_revenue"]
    )
    
    # 5. Return the full aggregated package
    return {
        "score_data": {
            "user_id": 1,
            "total_score": score_result["total_score"],
            "breakdown": score_result["breakdown"],
            "risk_tier": score_result["risk_tier"]
        },
        "insights": insights_list,
        "eligible_lenders": lender_matches
    }
