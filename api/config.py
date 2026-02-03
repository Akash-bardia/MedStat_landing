from pydantic_settings import BaseSettings
from typing import List
import os

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
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = True
        extra = "ignore"

    def model_post_init(self, __context):
        if self.SMTP_PASSWORD:
            self.SMTP_PASSWORD = self.SMTP_PASSWORD.replace(" ", "")

# Create settings instance
settings = Settings()
