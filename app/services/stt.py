from vocode.streaming.transcriber import DeepgramTranscriber
from app.config.settings import settings

class STTService:
    @staticmethod
    def create_transcriber():
        return DeepgramTranscriber(
            api_key=settings.DEEPGRAM_API_KEY,
            sampling_rate=8000,
            audio_encoding="mulaw",
            endpointing_config={"timeout_seconds": 1.0}
        )