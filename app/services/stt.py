from vocode.streaming.transcriber import deepgram_transcriber
from app.config.settings import settings

class STTService:
    @staticmethod
    def create_transcriber():
        return deepgram_transcriber(
            api_key=settings.DEEPGRAM_API_KEY,
            sampling_rate=8000,
            audio_encoding="mulaw",
            endpointing_config={"timeout_seconds": 1.0}
        )
    
