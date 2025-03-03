from vocode.streaming.agent import BaseAgent
from mistralai import Mistral
from app.config.settings import settings

SALES_SYSTEM_PROMPT = """
You are a professional sales agent. Follow these rules:
1. Greet warmly and ask open-ended questions
2. Keep responses under 20 words
3. Handle objections gracefully
4. Collect contact information
"""

class MistralAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = "mistral-small-latest"
        self.messages = [{"role": "system", "content": SALES_SYSTEM_PROMPT}]
    
    async def respond(self, human_input, conversation_id=None, is_interrupt=False):
        # Add user message
        self.messages.append({"role": "user", "content": human_input})
        
        # Get response using the new API format
        response = await self.client.chat.complete_async(
            model=self.model,
            messages=self.messages,
        )
        
        # Add assistant message
        assistant_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    async def handle_error(self, error):
        return "Sorry, I'm having trouble. Please try again later."