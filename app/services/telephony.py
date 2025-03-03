# telephony_service.py
import os
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from pydantic import BaseModel
from loguru import logger

from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.conversation.twilio_phone_conversation import TwilioPhoneConversation
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.models.agent import AgentConfig

class TelephonyService:
    def __init__(self, base_url: str, config_manager: RedisConfigManager):
        """Initialize the telephony service
        
        Args:
            base_url: The public base URL for the application
            config_manager: The configuration manager for telephony service
        """
        self.base_url = base_url
        self.config_manager = config_manager
        self.twilio_config = self._initialize_twilio()
    
    def _initialize_twilio(self) -> TwilioConfig:
        """Initialize Twilio configuration with credentials from environment"""
        return TwilioConfig(
            account_sid=os.environ["TWILIO_ACCOUNT_SID"],
            auth_token=os.environ["TWILIO_AUTH_TOKEN"],
        )
    
    async def handle_inbound_call(self, request: Request, agent_config: AgentConfig) -> str:
        """Process an incoming Twilio call
        
        Args:
            request: The FastAPI request object containing Twilio webhook data
            agent_config: Configuration for the agent to handle the conversation
            
        Returns:
            A TwiML response for the incoming call
        """
        try:
            # Extract form data from the request
            form_data = await request.form()
            
            # Extract Twilio parameters
            call_sid = form_data.get("CallSid")
            from_number = form_data.get("From")
            to_number = form_data.get("To")
            
            if not call_sid or not from_number or not to_number:
                logger.error(f"Missing required parameters in Twilio webhook: {form_data}")
                raise HTTPException(status_code=400, detail="Missing required Twilio parameters")
            
            logger.info(f"Handling inbound call from {from_number} to {to_number} (SID: {call_sid})")
            
            # Create a conversation object to handle the call
            conversation = TwilioPhoneConversation(
                base_url=self.base_url,
                twilio_config=self.twilio_config,
                agent_config=agent_config,
                config_manager=self.config_manager,
                call_sid=call_sid,
                from_number=from_number,
                to_number=to_number,
            )
            
            # Save the conversation in the config manager
            await self.config_manager.save_config(
                conversation.id, conversation.to_config_dict()
            )
            
            # Generate and return the TwiML response
            return conversation.get_call_instructions()
            
        except Exception as e:
            logger.exception(f"Error processing inbound call: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing call: {str(e)}")
    
    async def make_outbound_call(
        self, 
        to_phone: str, 
        from_phone: str, 
        agent_config: AgentConfig
    ) -> str:
        """Initiate an outbound call
        
        Args:
            to_phone: The phone number to call
            from_phone: The phone number to call from
            agent_config: Configuration for the agent to handle the conversation
            
        Returns:
            The conversation ID if successful
            
        Raises:
            HTTPException: If there's an error initiating the call
        """
        try:
            logger.info(f"Initiating outbound call to {to_phone} from {from_phone}")
            
            # Create outbound call object
            outbound_call = OutboundCall(
                base_url=self.base_url,
                to_phone=to_phone,
                from_phone=from_phone,
                config_manager=self.config_manager,
                agent_config=agent_config,
                telephony_config=self.twilio_config,
            )
            
            # Start the call
            conversation_id = await outbound_call.start()
            
            logger.info(f"Outbound call started successfully, conversation ID: {conversation_id}")
            return conversation_id
            
        except Exception as e:
            logger.exception(f"Error making outbound call: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error initiating outbound call: {str(e)}")
    
    async def end_call(self, conversation_id: str) -> bool:
        """End an active call
        
        Args:
            conversation_id: The ID of the conversation to end
            
        Returns:
            True if the call was ended successfully, False otherwise
        """
        try:
            logger.info(f"Ending call for conversation ID: {conversation_id}")
            
            # Get the conversation config
            conversation_config = await self.config_manager.get_config(conversation_id)
            if not conversation_config:
                logger.warning(f"No conversation found with ID: {conversation_id}")
                return False
            
            # Extract the call SID
            call_sid = conversation_config.get("call_sid")
            if not call_sid:
                logger.warning(f"No call SID found for conversation ID: {conversation_id}")
                return False
            
            # Import the Twilio client
            from twilio.rest import Client
            
            # Create Twilio client
            client = Client(self.twilio_config.account_sid, self.twilio_config.auth_token)
            
            # End the call
            call = client.calls(call_sid).update(status="completed")
            
            # Check if the call was ended successfully
            return call.status == "completed"
            
        except Exception as e:
            logger.exception(f"Error ending call: {str(e)}")
            return False