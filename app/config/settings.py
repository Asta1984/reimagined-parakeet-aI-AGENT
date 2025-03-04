from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mistral_api_key: str = ""
    agent_id: str = "ag:your_agent_id_here"
    twilio_auth_token: str = ""
    deepgram_api_key: str = ""
    elevenlabs_api_key: str = ""
    log_file: str = "conversation_logs.json"
    model: str = "mistral-small-latest"
    max_tokens: int = 150
    temperature: float = 0.7
    top_p: float = 1
    random_seed: int = 42

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields in the environment

settings = Settings()
