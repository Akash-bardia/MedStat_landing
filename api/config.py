from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Explicitly load .env file if it exists (handles local dev)
# In production, this does nothing if file is missing, which is perfect
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    """Application configuration"""
    
    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Email addresses
    ADMIN_EMAIL: str = ""
    
    # CORS
    FRONTEND_URL: str = "http://localhost:8000"
    
    # API Settings
    API_TITLE: str = "MedStat API"
    API_VERSION: str = "1.0.0"
    
    class Config:
        case_sensitive = True
        extra = "ignore"

    def model_post_init(self, __context):
        if self.SMTP_PASSWORD:
            self.SMTP_PASSWORD = self.SMTP_PASSWORD.replace(" ", "")

# Create settings instance
settings = Settings()
