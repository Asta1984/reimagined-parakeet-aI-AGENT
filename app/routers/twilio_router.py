from fastapi import APIRouter, Request
from twilio.twiml.voice_response import VoiceResponse
from app.services.stt import STTService
from app.services.tts import TTSService
from app.agents.sales_agent import SalesAgent
from app.config.settings import settings
from vocode.streaming.telephony.twilio import TwilioCall

router = APIRouter()

@router.post("/twilio-webhook")
async def handle_twilio_webhook(request: Request):
    try:
        call = TwilioCall.from_request(request)
        agent = SalesAgent()
        call.start_conversation(
            transcriber=STTService.create_transcriber(),
            synthesizer=TTSService.create_synthesizer(),
            agent=agent
        )
        return VoiceResponse().to_xml()
    except Exception as e:
        return VoiceResponse().say("Error processing request").to_xml()