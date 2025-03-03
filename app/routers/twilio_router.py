from fastapi import APIRouter, Request
from twilio.twiml.voice_response import VoiceResponse
from app.services.telephony import TelephonyService
from app.services.stt import STTService
from app.services.tts import TTSService
from app.agents.sales_agent import BaseAgent
from app.utils.logger import ConversationLogger

router = APIRouter()

@router.post("/twilio-webhook")
async def handle_twilio_webhook(request: Request):
    try:
        # Initialize call handling
        call = TelephonyService.handle_incoming_call(request)
        agent = BaseAgent()
        
        # Start conversation
        call.start_conversation(
            transcriber=STTService.create_transcriber(),
            synthesizer=TTSService.create_synthesizer(),
            agent=agent
        )
        
        # Log initialization
        ConversationLogger.log_interaction(
            phone=call.from_number,
            input="Call started",
            output="Welcome message played"
        )
        
        return VoiceResponse().to_xml()
    
    except Exception as e:
        ConversationLogger.log_interaction(
            phone=call.from_number if 'call' in locals() else "unknown",
            input="Error occurred",
            output=str(e)
        )
        return VoiceResponse().say("Sorry, we're experiencing technical difficulties").to_xml()