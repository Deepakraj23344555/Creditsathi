from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import BusinessInput, ScoreResponse, FullReportResponse
# We will import our services here in later phases
# from app.services import parser, scorer, insights, matcher

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
    In a live environment, this would also trigger the GST API sync.
    """
    if not file.filename.endswith(('.pdf', '.csv')):
        raise HTTPException(status_code=400, detail="Only PDF and CSV files are supported.")
    
    # Placeholder for Phase 4: Parser Service
    # parsed_data = await parser.extract_financials(file)
    
    return {
        "status": "success", 
        "message": f"File {file.filename} processed successfully.",
        "simulated_data_extraction": "Pending Phase 4 implementation"
    }

@router.post("/calculate-score", response_model=ScoreResponse, summary="Generate Credit Readiness Score")
async def calculate_score(user_data: BusinessInput):
    """
    Triggers the scoring engine using the parsed financial data and GST inputs.
    """
    # Placeholder for Phase 5: Scoring Engine
    # score_result = scorer.calculate_crs(user_data)
    
    # Returning dummy data to satisfy the schema for now
    return {
        "user_id": 1,
        "total_score": 720,
        "breakdown": {
            "cash_flow_stability": 210,
            "business_vintage": 100,
            "gst_compliance": 150,
            "debt_coverage": 140,
            "digital_footprint": 120
        },
        "risk_tier": "Low Risk"
    }

@router.get("/get-report/{user_id}", response_model=FullReportResponse, summary="Fetch Comprehensive Credit Report")
async def get_report(user_id: int):
    """
    Aggregates the Score, AI Insights, and Lender Matches into a single payload for the frontend.
    """
    # Placeholder for Phase 6 & 7: Insights and Matching Engines
    # insights_data = insights.generate(user_id)
    # matches = matcher.find_eligible_lenders(user_id)
    
    raise HTTPException(status_code=501, detail="Report generation logic pending Phase 6 & 7")
