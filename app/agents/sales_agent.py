from vocode.streaming.agent import ChatGPTAgent
from app.config.settings import settings

SALES_SYSTEM_PROMPT = """
You are a professional sales agent. Follow these rules:
1. Greet warmly and ask open-ended questions
2. Keep responses under 20 words
3. Handle objections gracefully
4. Collect contact information
"""

class SalesAgent(ChatGPTAgent):
    def __init__(self):
        super().__init__(
            system_prompt=SALES_SYSTEM_PROMPT,
            model_name="mistral-small-latest",
            api_key=settings.MISTRAL_API_KEY
        )
    
    async def handle_error(self, error):
        return "Sorry, I'm having trouble. Please try again later."