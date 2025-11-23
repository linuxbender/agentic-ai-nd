"""
Feedstock Analyst Agent.

Analyzes hydrocarbon feedstock composition and characteristics.
"""
from agents.base import RefineryAgent
from models import AgentResponse


class FeedstockAnalystAgent(RefineryAgent):
    """
    Agent 1: Feedstock Analyst
    
    Analyzes hydrocarbon feedstock composition and characteristics.
    Provides detailed insights into the chemical makeup and suitability
    for refining into various petroleum products.
    """
    
    def __init__(self):
        system_prompt = (
            "You are a petrochemical expert analyzing hydrocarbon feedstocks. "
            "Provide a concise analysis of the given feedstock, highlighting its key components "
            "and general suitability for producing valuable refined products like gasoline, diesel, and kerosene. "
            "Be specific about the chemical composition and refining characteristics."
        )
        super().__init__("Feedstock Analyst", system_prompt)
    
    def execute(self, feedstock_name: str) -> AgentResponse:
        """Analyze the given feedstock and return detailed composition analysis."""
        print(f"🔬 [{self.name}] Analyzing feedstock: {feedstock_name}...")
        
        user_prompt = f"Analyze the feedstock: {feedstock_name}"
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Analysis completed.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )
