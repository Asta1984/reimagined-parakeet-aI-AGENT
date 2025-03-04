# app/routers/call_router.py
from fastapi import APIRouter, HTTPException, Request
from app.services.telephony import TelephonyService
from app.config.settings import settings
from app.utils.responses import XMLResponse
import logging

router = APIRouter()
logger = logging.getLogger("CallRouter")

@router.post("/inbound-call", response_class=XMLResponse)
async def handle_inbound_call(request: Request):
    try:
        form_data = await request.form()
        call_sid = form_data.get("CallSid")
        from_number = form_data.get("From")
        to_number = form_data.get("To")
        
        if not all([call_sid, from_number, to_number]):
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        telephony_service = TelephonyService(
            base_url="https://d620-2409-4081-8783-3752-68dc-f21b-2fae-b02a.ngrok-free.app"  # Update this with your current ngrok URL
        )
        
        twiml_response = await telephony_service.handle_inbound_call(
            call_sid, from_number, to_number
        )
        
        return XMLResponse(twiml_response)
        
    except Exception as e:
        logger.error(f"Inbound call error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/outbound-call")
async def initiate_outbound_call(to_phone: str):
    try:
        telephony_service = TelephonyService(
            base_url="https://d620-2409-4081-8783-3752-68dc-f21b-2fae-b02a.ngrok-free.app"  # Same as above
        )
        conversation_id = await telephony_service.initiate_outbound_call(to_phone)
        return {"status": "success", "conversation_id": conversation_id}
    
    except Exception as e:
        logger.error(f"Outbound call error: {e}")
        raise HTTPException(status_code=500, detail=str(e))