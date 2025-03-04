# app/agents/sales_agent.py
from mistralai.client import MistralClient
from app.config.settings import settings
import logging

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
        self.mistral_client = MistralClient(api_key=settings.MISTRAL_API_KEY)
        self.conversation_history = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
    
    def generate_response(self, user_input: str) -> str:
        try:
            self.conversation_history.append({"role": "user", "content": user_input})
            response = self.mistral_client.chat(
                model=settings.MISTRAL_MODEL,
                messages=self.conversation_history
            )
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "I'm having trouble connecting to the system. Could you please repeat that?"

