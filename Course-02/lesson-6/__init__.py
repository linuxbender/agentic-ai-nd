"""
Refinery Optimization System

A multi-agent system for optimizing refinery operations through
sequential analysis of feedstock, distillation planning, market analysis,
and production optimization.
"""
from models import AgentResponse
from workflow import RefineryOptimizationWorkflow
from utils import save_results_to_json

__version__ = "1.0.0"
__all__ = [
    "AgentResponse",
    "RefineryOptimizationWorkflow",
    "save_results_to_json",
]
