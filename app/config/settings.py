from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mistral_api_key: str
    deepgram_api_key: str
    elevenlabs_api_key: str
    elevenlabs_voice_id: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    
    class Config:
        env_file = ".env"

settings = Settings()