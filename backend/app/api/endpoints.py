from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import BusinessInput, ScoreResponse, FullReportResponse

# Import our new Scoring Engine
from app.services.scorer import CreditScoringEngine

router = APIRouter()

@router.post("/upload-statement", summary="Upload Bank Statement & Sync GST")
async def upload_statement(
    file: UploadFile = File(...),
    business_name: str = Form(...),
    gstin: str = Form(...),
    vintage_years: float = Form(...)
):
    if not file.filename.endswith(('.pdf', '.csv')):
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported.")
    
    # Placeholder for Phase 4: Parser Service execution
    return {
        "status": "success", 
        "message": f"File {file.filename} processed successfully.",
        "simulated_data_extraction": "Pending Phase 4 database linkage"
    }

@router.post("/calculate-score", response_model=ScoreResponse, summary="Generate Credit Readiness Score")
async def calculate_score(user_data: BusinessInput):
    """
    Triggers the scoring engine using the parsed financial data and GST inputs.
    """
    # 1. Simulate the data that would normally be pulled from the 'financial_data' SQL table
    mock_parsed_data = {
        "monthly_revenue": 150000.0,
        "cash_flow_volatility_pct": 25.0,
        "estimated_monthly_emi": 30000.0
    }
    
    # 2. Execute the actual mathematical engine we built in Phase 5
    result = CreditScoringEngine.calculate_crs(
        parsed_financials=mock_parsed_data, 
        user_inputs=user_data.model_dump() 
    )
    
    # 3. Return the exact structure our Pydantic schema expects
    return {
        "user_id": 1, # Hardcoded temporarily until we connect the DB
        "total_score": result["total_score"],
        "breakdown": result["breakdown"],
        "risk_tier": result["risk_tier"]
    }

@router.get("/get-report/{user_id}", response_model=FullReportResponse, summary="Fetch Comprehensive Credit Report")
async def get_report(user_id: int):
    raise HTTPException(status_code=501, detail="Report generation logic pending Phase 6 & 7")
