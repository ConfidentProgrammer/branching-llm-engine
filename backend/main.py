from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from database import get_db
from schemas import DBStatusResponse
from services.db_service import DatabaseService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chattree")

app = FastAPI(
    title="ChatTree Backend",
    version="1.0.0",
    description="Modular, enterprise-grade FastAPI backend for ChatTree"
)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "ChatTree API is running successfully!", "timestamp": datetime.now()}

@app.get("/test-db", response_model=DBStatusResponse, tags=["Health"])
def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint leveraging the service layer to check database connectivity.
    """
    try:
        query_result = DatabaseService.check_connection(db)
        return {
            "status": "success",
            "message": "Successfully connected to PostgreSQL via SQLAlchemy!",
            "test_query_result": query_result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        # Fail fast: Return a clean HTTP 500 error with descriptive debugging details
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {str(e)}"
        )