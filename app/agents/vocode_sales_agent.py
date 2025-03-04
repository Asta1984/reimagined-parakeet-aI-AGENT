# app/agents/vocode_sales_agent.py
from vocode.streaming.agent.base_agent import BaseAgent
from app.agents.sales_agent import SalesAgent
from typing import AsyncGenerator

class VocodeSalesAgent(BaseAgent):
    def __init__(self, agent_config, **kwargs):
        super().__init__(agent_config=agent_config)
        self.sales_agent = SalesAgent()
        
    async def respond(
        self,
        human_input: str,
        conversation_id: str,
        is_interrupt: bool = False
    ) -> AsyncGenerator[str, None]:
        response = self.sales_agent.generate_response(human_input)
        yield response