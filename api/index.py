from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import logging
from datetime import datetime

# Import email service
from email_service import send_contact_notification, send_demo_notification

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="MedStat API",
    description="Backend API for MedStat landing page form submissions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "http://localhost:5500",  # Live Server
        "*"  # Allow all for development - restrict in production!
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    type: str
    message: str = Field(..., min_length=10, max_length=1000)

class DemoRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    clinic: str = Field(..., min_length=2, max_length=200)
    role: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    interests: Optional[str] = Field(None, max_length=500)

class SuccessResponse(BaseModel):
    success: bool
    message: str
    timestamp: str

# Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MedStat API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/contact", response_model=SuccessResponse)
async def submit_contact_form(form_data: ContactForm):
    """
    Handle contact form submissions
    
    - Validates form data
    - Sends email notification to admin
    - Returns success response
    """
    try:
        logger.info(f"Contact form submission from: {form_data.email}")
        
        # Send email notification
        email_sent = await send_contact_notification(form_data)
        
        if not email_sent:
            logger.error("Email notification failed for contact form")
            raise HTTPException(
                status_code=500,
                detail="Failed to send email notification. Please try again later."
            )
        
        return SuccessResponse(
            success=True,
            message="Thank you for contacting us! We'll get back to you within 24 hours.",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your request. Please try again later."
        )

@app.post("/api/demo-request", response_model=SuccessResponse)
async def submit_demo_request(demo_data: DemoRequest):
    """
    Handle demo request submissions
    
    - Validates form data
    - Sends email notification to admin
    - Returns success response
    """
    try:
        logger.info(f"Demo request from: {demo_data.email}")
        
        # Send email notification
        email_sent = await send_demo_notification(demo_data)
        
        if not email_sent:
            logger.error("Email notification failed for demo request")
            raise HTTPException(
                status_code=500,
                detail="Failed to send email notification. Please try again later."
            )
        
        return SuccessResponse(
            success=True,
            message="Demo request received! Our team will contact you within 24 hours to schedule your personalized demo.",
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error processing demo request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process your request. Please try again later."
        )

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "detail": "The requested resource was not found"
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "detail": "An unexpected error occurred. Please try again later."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
