# app/services/telephony_service.py
from vocode.streaming.models.agent import AgentConfig, LLMAgentConfig
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall
from vocode.streaming.telephony.conversation.twilio_phone_conversation import TwilioPhoneConversation
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from app.agents.vocode_sales_agent import VocodeSalesAgent
from app.config.settings import settings
from app.agents.sales_agent import SalesAgent
import redis
import logging

class MistralAgentConfig(LLMAgentConfig):
    class Config:
        arbitrary_types_allowed = True
        
    def __init__(self, **kwargs):
        super().__init__(
            prompt_preamble=SalesAgent.SYSTEM_PROMPT,
            model_name="mistral-custom",
            **kwargs
        )

class TelephonyService:
    def __init__(self, base_url: str):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base_url = base_url.strip()
        self.config_manager = RedisConfigManager(redis_client=self.redis_client)
        
        self.twilio_config = TwilioConfig(
            account_sid=settings.TWILIO_ACCOUNT_SID,
            auth_token=settings.TWILIO_AUTH_TOKEN
        )
        
        # Use custom Mistral config
        self.agent_config = MistralAgentConfig(
            initial_message=None,
            temperature=0.7,
            max_tokens=256
        )

    async def handle_inbound_call(self, call_sid: str, from_number: str, to_number: str):
        try:
            conversation = TwilioPhoneConversation(
                base_url=self.base_url,
                twilio_config=self.twilio_config,
                agent=VocodeSalesAgent(agent_config=self.agent_config),
                config_manager=self.config_manager,
                call_sid=call_sid,
                from_number=from_number,
                to_number=to_number
            )
            
            await self.config_manager.save_config(
                conversation.id, 
                conversation.to_config_dict()
            )
            
            self.logger.debug(f"Generated TwiML: {conversation.get_call_instructions()}")
            return conversation.get_call_instructions()
        
        except Exception as e:
            self.logger.error(f"Error handling inbound call: {e}")
            raise

    async def initiate_outbound_call(self, to_phone: str):
        try:
            outbound_call = OutboundCall(
                base_url=self.base_url,
                to_phone=to_phone,
                from_phone=settings.TWILIO_PHONE_NUMBER,
                config_manager=self.config_manager,
                agent=VocodeSalesAgent(agent_config=self.agent_config),
                telephony_config=self.twilio_config
            )
            
            conversation_id = await outbound_call.start()
            return conversation_id
        
        except Exception as e:
            self.logger.error(f"Error initiating outbound call: {e}")
            raise