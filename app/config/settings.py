# app/config/settings.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # Redis configuration
    REDIS_HOST: str = "172.28.9.249"  
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Vocode configuration
    VOCODE_API_KEY: str = ""
    
    # AI Model Configuration
    MISTRAL_API_KEY: str = ""
    MISTRAL_MODEL: str = "mistral-small"
    
    # Telephony Credentials
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Speech Services
    DEEPGRAM_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    
    # Logging and Debugging
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()