# app/services/tts_service.py
from vocode.streaming.synthesizer import eleven_labs_synthesizer
from app.config.settings import settings
import logging

class TTSService:
    @staticmethod
    def create_synthesizer():
        logger = logging.getLogger("TTSService")
        try:
            return eleven_labs_synthesizer(
                api_key=settings.ELEVENLABS_API_KEY,
                voice_id="2EiwWnXFnvU5JabPnv8n",  
                stability=0.7,
                similarity_boost=0.5
            )
        except Exception as e:
            logger.error(f"Error creating synthesizer: {e}")
            raise