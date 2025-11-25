from workflow_agents.base_agents import AugmentedPromptAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

augmented_agent = AugmentedPromptAgent(openai_api_key, persona)

augmented_agent_response = augmented_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# The agent likely used its general knowledge from the LLM (GPT-3.5-turbo) to answer the question about France's capital.
# The system prompt specifying the persona caused the agent to structure its response by starting with "Dear students," 
# making the tone more educational and professional, as expected from a college professor.
