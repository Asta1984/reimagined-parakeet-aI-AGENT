from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    DEEPGRAM_API_KEY: str
    ELEVENLABS_API_KEY: str
    MISTRAL_API_KEY: str
    ELEVENLABS_VOICE_ID: str = "EXAVITQu4vr4xnSDxMaL"
    
    class Config:
        env_file = ".env"

settings = Settings()