from vocode.streaming.synthesizer import ElevenLabsSynthesizer
from app.config.settings import settings

class TTSService:
    @staticmethod
    def create_synthesizer():
        return ElevenLabsSynthesizer(
            api_key=settings.ELEVENLABS_API_KEY,
            voice_id=settings.ELEVENLABS_VOICE_ID,
            stability=0.71,
            similarity_boost=0.5
        )