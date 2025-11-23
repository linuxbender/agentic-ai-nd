"""
Refinery Optimization Workflow.

Orchestrates the complete agent chain for refinery optimization.
"""
from typing import Dict
from models import AgentResponse
from agents.feedstock_analyst import FeedstockAnalystAgent
from agents.distillation_planner import DistillationPlannerAgent
from agents.market_analyst import MarketAnalystAgent
from agents.production_optimizer import ProductionOptimizerAgent


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
        print(f"📦 Processing feedstock: {feedstock_name}")
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
        print("✨ Workflow completed!")
        print("="*80)
        
        return results
