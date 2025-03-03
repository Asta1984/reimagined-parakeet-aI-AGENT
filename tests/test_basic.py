import pytest
from app.config.settings import settings

def test_config_loading():
    assert settings.TWILIO_ACCOUNT_SID is not None
    assert settings.DEEPGRAM_API_KEY is not None
    assert settings.ELEVENLABS_API_KEY is not None