from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from twilio.twiml.voice_response import VoiceResponse
from app.services.telephony import TelephonyService
from app.services.stt import STTService
from app.services.tts import TTSService
from app.agents.sales_agent import MistralAgent
from app.utils.logger import ConversationLogger
from app.config.settings import settings
import asyncio
import json
from app.utils.responses import XMLResponse

router = APIRouter()

async def get_telephony_service():
    base_url = "https://9511-14-139-241-69.ngrok-free.app"
    config_manager = None
    return TelephonyService(base_url=base_url, config_manager=config_manager)

@router.post("/twilio-webhook")
async def handle_twilio_webhook(
    request: Request,
    telephony_service: TelephonyService = Depends(get_telephony_service)
):
    """Handle incoming Twilio calls"""
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        from_number = form_data.get("From")
        
        if not call_sid or not from_number:
            raise HTTPException(status_code=400, detail="Missing parameters")

        ConversationLogger.log_interaction(
            phone=from_number,
            input="Call initiated",
            output="Processing incoming call"
        )

        # Create config FIRST
        agent_config = {
            "type": "mistral_agent",
            "model": "mistral-tiny"
        }
        
        # Initialize agent WITH CONFIG
        agent = MistralAgent(agent_config=agent_config)

        twiml_response = await telephony_service.handle_inbound_call(
            request=request,
            agent_config=agent_config
        )

        return Response(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        ConversationLogger.log_interaction(
            phone=form_data.get("From", "unknown"),
            input="Error in webhook",
            output=f"Error: {str(e)}"
        )
        response = VoiceResponse()
        response.say("Technical difficulties. Please try again later.")
        return Response(content=str(response), media_type="application/xml")

@router.post("/outbound-call")
async def initiate_outbound_call(
    to_phone: str,
    telephony_service: TelephonyService = Depends(get_telephony_service)
):
    """Initiate outbound call"""
    try:
        # Create config FIRST
        agent_config = {
            "type": "mistral_agent",
            "model": "mistral-tiny"
        }
        
        # Initialize agent WITH CONFIG
        agent = MistralAgent(agent_config=agent_config)

        conversation_id = await telephony_service.make_outbound_call(
            to_phone=to_phone,
            from_phone=settings.TWILIO_PHONE_NUMBER,
            agent_config=agent_config
        )

        return {"status": "success", "conversation_id": conversation_id}
        
    except Exception as e:
        ConversationLogger.log_interaction(
            phone=to_phone,
            input="Outbound call request",
            output=f"Error: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")

@router.post("/call-status")
async def handle_call_status(
    request: Request,
    CallSid: str = Form(...),
    CallStatus: str = Form(...),
):
    """Handle Twilio call status callbacks"""
    try:
        # Log the call status update
        ConversationLogger.log_interaction(
            phone="system",
            input=f"Call status update for {CallSid}",
            output=f"Status: {CallStatus}"
        )
        
        # Return empty TwiML response
        response = VoiceResponse()
        return Response(content=str(response), media_type="application/xml")
        
    except Exception as e:
        # Log the error
        ConversationLogger.log_interaction(
            phone="system",
            input="Error in status callback",
            output=f"Error: {str(e)}"
        )
        
        # Return empty response on error
        response = VoiceResponse()
        return Response(content=str(response), media_type="application/xml")

@router.post("/outbound-call")
async def initiate_outbound_call(
    to_phone: str,
    telephony_service: TelephonyService = Depends(get_telephony_service)
):
    """Endpoint to initiate an outbound call to a specified number"""
    try:
        # Set up agent config
        agent = MistralAgent()
        agent_config = {
            "type": "mistral_agent",
            "model": "mistral-tiny"
        }
        
        # Initiate the call
        conversation_id = await telephony_service.make_outbound_call(
            to_phone=to_phone,
            from_phone=settings.TWILIO_PHONE_NUMBER,
            agent_config=agent_config
        )
        
        # Return success response
        return {"status": "success", "conversation_id": conversation_id}
        
    except Exception as e:
        # Log the error
        ConversationLogger.log_interaction(
            phone=to_phone,
            input="Outbound call request",
            output=f"Error: {str(e)}"
        )
        
        # Return error response
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {str(e)}")