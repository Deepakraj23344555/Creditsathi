from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="CreditSaathi API",
    description="Backend engine for MSME Credit Intelligence Platform",
    version="1.0.0"
)

# Configure CORS for frontend communication (Streamlit defaults to port 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "*"], # Restrict "*" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our endpoints
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "active", "system": "CreditSaathi Core API"}
