"""
Utility functions for the refinery optimization system.
"""
import json
from typing import Dict
from models import AgentResponse


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
    
    print(f"\n💾 Results saved to: {filename}")
