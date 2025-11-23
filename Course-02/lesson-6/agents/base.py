"""
Base agent class for all refinery optimization agents.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI
from models import AgentResponse

load_dotenv()

client = OpenAI(
    base_url="https://openai.vocareum.com/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)


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
