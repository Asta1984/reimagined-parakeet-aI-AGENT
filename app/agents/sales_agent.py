from vocode.streaming.agent import BaseAgent
from mistralai import Mistral
from app.config.settings import settings
import asyncio

SALES_SYSTEM_PROMPT = """
You are a professional sales agent. Follow these rules:
1. Greet warmly and ask open-ended questions
2. Keep responses under 20 words
3. Handle objections gracefully
4. Collect contact information
"""

class MistralAgent(BaseAgent):
    def __init__(self, agent_config):  # Accept agent_config
        super().__init__(agent_config=agent_config)  # Pass to parent
        self.client = Mistral(api_key=settings.MISTRAL_API_KEY)
        self.model = agent_config.get("model", "mistral-small-latest")  # Use config value
        self.messages = [{"role": "system", "content": SALES_SYSTEM_PROMPT}]
    
    async def respond(self, human_input, conversation_id=None, is_interrupt=False):
        self.messages.append({"role": "user", "content": human_input})
        
        full_response = ""
        response_stream = await self.client.chat.stream_async(
            model=self.model,
            messages=self.messages,
        )
        
        async for chunk in response_stream:
            if chunk.data.choices[0].delta.content is not None:
                full_response += chunk.data.choices[0].delta.content
        
        self.messages.append({"role": "assistant", "content": full_response})
        return full_response
    
    async def handle_error(self, error):
        return f"Sorry, I'm having trouble. Error: {str(error)[:50]}. Please try again later."