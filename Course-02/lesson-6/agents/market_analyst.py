"""
Market Analyst Agent.

Analyzes market conditions and demand for refined petroleum products.
"""
from agents.base import RefineryAgent
from models import AgentResponse


class MarketAnalystAgent(RefineryAgent):
    """
    Agent 3: Market Analyst
    
    Analyzes market conditions and demand for refined petroleum products.
    Provides insights into profitability trends, demand levels, and
    relevant market factors affecting product value.
    """
    
    def __init__(self):
        system_prompt = (
            "You are an energy market analyst specializing in refined petroleum products. "
            "For the given list of refined products, provide a brief analysis of: \n"
            "1. Current market demand (high, medium, low)\n"
            "2. General profitability trends\n"
            "3. Any relevant market conditions or seasonal factors\n"
            "Be realistic and consider current global energy market trends."
        )
        super().__init__("Market Analyst", system_prompt)
    
    def execute(self, distillation_plan: str) -> AgentResponse:
        """Analyze market conditions for the distillation products."""
        print(f"📊 [{self.name}] Analyzing market conditions...")
        
        user_prompt = f"""Based on the following distillation plan, analyze the market conditions 
for these refined products:

--- DISTILLATION PLAN ---
{distillation_plan}
--- END PLAN ---

Provide market demand, profitability, and any relevant market insights."""
        
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Market analysis completed.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )
