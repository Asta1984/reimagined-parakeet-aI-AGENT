        # app/agents/sales_agent.py
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
from app.config.settings import settings
import logging
import asyncio

class SalesAgent:
    class SalesAgent:
        SYSTEM_PROMPT = """
    You are a professional sales agent. Your objectives:
    1. Build rapport quickly
    2. Ask insightful, open-ended questions
    3. Listen and understand customer needs
    4. Present tailored solutions
    5. Handle objections gracefully
    6. Guide conversation towards a positive outcome
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.mistral_client = MistralAsyncClient(api_key=settings.MISTRAL_API_KEY)
        self.conversation_history = [
            ChatMessage(role="system", content=self.SYSTEM_PROMPT)
        ]
    
    async def generate_response(self, user_input: str) -> str:
        try:
            self.conversation_history.append(ChatMessage(role="user", content=user_input))
            response = await self.mistral_client.chat(
                model=settings.MISTRAL_MODEL,
                messages=self.conversation_history
            )
            ai_response = response.choices[0].message.content
            self.conversation_history.append(ChatMessage(role="assistant", content=ai_response))
            return ai_response
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I'm having trouble connecting to the system. Could you please repeat that?"
