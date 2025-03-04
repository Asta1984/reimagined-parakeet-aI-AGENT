# app/services/stt_service.py
from vocode.streaming.transcriber import deepgram_transcriber
from app.config.settings import settings
import logging

class STTService:
    @staticmethod
    def create_transcriber():
        logger = logging.getLogger("STTService")
        try:
            return deepgram_transcriber(
                api_key=settings.DEEPGRAM_API_KEY,
                sampling_rate=8000,
                audio_encoding="mulaw",
                endpointing_config={"timeout_seconds": 1.0}
            )
        except Exception as e:
            logger.error(f"Error creating transcriber: {e}")
            raise
