"""
Distillation Planner Agent.

Plans the allocation of feedstock through the distillation tower.
"""
from agents.base import RefineryAgent
from models import AgentResponse


class DistillationPlannerAgent(RefineryAgent):
    """
    Agent 2: Distillation Planner
    
    Plans the allocation of feedstock through the distillation tower.
    Estimates product yields based on feedstock analysis, considering
    typical distillation ranges and boiling points.
    """
    
    def __init__(self):
        system_prompt = (
            "You are a refinery distillation tower operations planner. "
            "Based on the provided feedstock analysis, estimate the potential percentage yields "
            "for major products like gasoline, diesel, kerosene, and other fractions. "
            "Be realistic and provide specific percentages that sum to 100%. "
            "Consider typical distillation ranges and boiling points."
        )
        super().__init__("Distillation Planner", system_prompt)
    
    def execute(self, feedstock_analysis: str) -> AgentResponse:
        """Plan distillation process based on feedstock analysis."""
        print(f"⚗️  [{self.name}] Planning distillation process...")
        
        user_prompt = f"""Based on the following feedstock analysis, provide a realistic distillation plan 
with percentage yields for the main products:

--- FEEDSTOCK ANALYSIS ---
{feedstock_analysis}
--- END ANALYSIS ---

Provide the yields in a clear format."""
        
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Distillation plan created.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )
