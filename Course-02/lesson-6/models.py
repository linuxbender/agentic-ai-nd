"""
Data models for the refinery optimization system.
"""
from dataclasses import dataclass
from typing import Optional


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
