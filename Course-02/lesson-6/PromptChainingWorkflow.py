import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI
import json
from dataclasses import dataclass

load_dotenv()

client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


@dataclass
class AgentResponse:
    """
    Data structure for agent responses.
    
    Attributes:
        agent_name: Name of the agent that generated the response
        content: The actual response content from the LLM
        success: Whether the operation was successful
        error: Error message if the operation failed
    """
    agent_name: str
    content: str
    success: bool = True
    error: Optional[str] = None


class RefineryAgent:
    """
    Base class for all refinery optimization agents.
    
    Provides common functionality for LLM interactions and response handling.
    All specialized agents inherit from this class.
    
    Attributes:
        name: The agent's display name
        system_prompt: The system prompt that defines the agent's role and behavior
    """
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
    
    def get_llm_response(self, user_prompt: str, temperature: float = 0.7) -> str:
        """Send a request to the LLM and return the response."""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def execute(self, *args, **kwargs) -> AgentResponse:
        """Execute the agent's main logic. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute()")


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
        print(f"🔬 [{self.name}] Analysiere Rohstoff: {feedstock_name}...")
        
        user_prompt = f"Analyze the feedstock: {feedstock_name}"
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Analyse abgeschlossen.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )


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
        print(f"⚗️  [{self.name}] Plane Destillationsprozess...")
        
        user_prompt = f"""Based on the following feedstock analysis, provide a realistic distillation plan 
with percentage yields for the main products:

--- FEEDSTOCK ANALYSIS ---
{feedstock_analysis}
--- END ANALYSIS ---

Provide the yields in a clear format."""
        
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Destillationsplan erstellt.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )


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
        print(f"📊 [{self.name}] Analysiere Marktbedingungen...")
        
        user_prompt = f"""Based on the following distillation plan, analyze the market conditions 
for these refined products:

--- DISTILLATION PLAN ---
{distillation_plan}
--- END PLAN ---

Provide market demand, profitability, and any relevant market insights."""
        
        response = self.get_llm_response(user_prompt)
        
        print(f"✅ [{self.name}] Marktanalyse abgeschlossen.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )


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
        print(f"🎯 [{self.name}] Optimiere Produktionsstrategie...")
        
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
        
        print(f"✅ [{self.name}] Optimierung abgeschlossen.")
        return AgentResponse(
            agent_name=self.name,
            content=response
        )


class RefineryOptimizationWorkflow:
    """
    Orchestrates the complete refinery optimization workflow.
    
    Manages the sequential execution of all four agents in the prompt chain:
    1. Feedstock Analysis
    2. Distillation Planning
    3. Market Analysis
    4. Production Optimization
    
    Each agent's output feeds into the next, creating a comprehensive
    optimization pipeline.
    """
    
    def __init__(self):
        self.feedstock_analyst = FeedstockAnalystAgent()
        self.distillation_planner = DistillationPlannerAgent()
        self.market_analyst = MarketAnalystAgent()
        self.production_optimizer = ProductionOptimizerAgent()
    
    def run(self, feedstock_name: str) -> Dict[str, AgentResponse]:
        """Execute the complete optimization workflow for the given feedstock."""
        print("="*80)
        print(f"🏭 REFINERY OPTIMIZATION WORKFLOW")
        print(f"📦 Verarbeite Rohstoff: {feedstock_name}")
        print("="*80)
        print()
        
        results = {}
        
        # Agent 1: Feedstock Analysis
        analysis_response = self.feedstock_analyst.execute(feedstock_name)
        results['feedstock_analysis'] = analysis_response
        print(f"\n--- FEEDSTOCK ANALYSIS ---")
        print(analysis_response.content)
        print()
        
        # Agent 2: Distillation Planning
        plan_response = self.distillation_planner.execute(analysis_response.content)
        results['distillation_plan'] = plan_response
        print(f"\n--- DISTILLATION PLAN ---")
        print(plan_response.content)
        print()
        
        # Agent 3: Market Analysis
        market_response = self.market_analyst.execute(plan_response.content)
        results['market_analysis'] = market_response
        print(f"\n--- MARKET ANALYSIS ---")
        print(market_response.content)
        print()
        
        # Agent 4: Production Optimization
        optimization_response = self.production_optimizer.execute(
            plan_response.content,
            market_response.content
        )
        results['production_optimization'] = optimization_response
        print(f"\n{'='*80}")
        print(f"🎯 OPTIMIZED PRODUCTION RECOMMENDATION")
        print(f"{'='*80}")
        print(optimization_response.content)
        print(f"\n{'='*80}")
        print("✨ Workflow abgeschlossen!")
        print("="*80)
        
        return results


def main():
    """Main function to execute the refinery optimization workflow."""
    feedstocks = [
        "West Texas Intermediate Crude",
        # Alternative feedstocks for testing:
        # "Brent Crude Oil",
        # "Light Sweet Crude",
        # "Heavy Sour Crude",
    ]
    
    workflow = RefineryOptimizationWorkflow()
    
    current_feedstock = feedstocks[0]
    results = workflow.run(current_feedstock)
    
    # Optional: Save results to JSON
    # save_results_to_json(results, "refinery_optimization_results.json")


def save_results_to_json(results: Dict[str, AgentResponse], filename: str):
    """Save workflow results to a JSON file."""
    json_results = {
        key: {
            "agent_name": response.agent_name,
            "content": response.content,
            "success": response.success
        }
        for key, response in results.items()
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Ergebnisse gespeichert in: {filename}")


if __name__ == "__main__":
    main()
