"""
Production Optimizer Agent.

Optimizes production strategy by balancing yields with market conditions.
"""
from agents.base import RefineryAgent
from models import AgentResponse


class ProductionOptimizerAgent(RefineryAgent):
    """
    Agent 4: Production Optimizer
    
    Optimizes production strategy by balancing potential yields with
    current market conditions. Provides actionable recommendations to
    maximize refinery value and profitability.
    """
    
    def __init__(self):
        system_prompt = (
            "You are a refinery production optimization expert. "
            "Your goal is to recommend a production strategy that maximizes value "
            "by balancing potential yields with current market conditions. "
            "Provide specific, actionable recommendations on which products to prioritize, "
            "any adjustments to distillation parameters, and expected business impact."
        )
        super().__init__("Production Optimizer", system_prompt)
    
    def execute(self, distillation_plan: str, market_data: str) -> AgentResponse:
        """Generate optimized production recommendation based on distillation plan and market data."""
        print(f"🎯 [{self.name}] Optimizing production strategy...")
        
        user_prompt = f"""Given the following potential distillation plan:
--- DISTILLATION PLAN ---
{distillation_plan}
--- END DISTILLATION PLAN ---

And the following market analysis:
--- MARKET ANALYSIS ---
{market_data}
--- END MARKET ANALYSIS ---

Please provide a concise recommendation on which products the refinery should prioritize 
or focus on to maximize value, considering both the potential yield and market conditions. 
Include specific actions and expected outcomes."""
        
        response = self.get_llm_response(user_prompt, temperature=0.6)
        
        print(f"✅ [{self.name}] Optimization completed.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )
