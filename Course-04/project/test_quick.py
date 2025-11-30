"""
Quick test of the multi-agent system with a single request
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
if not load_dotenv():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(parent_dir, '.env')
    load_dotenv(env_path)

# Verify environment variables
print("Checking environment variables...")
api_key = os.getenv("UDACITY_OPENAI_API_KEY")
api_base = os.getenv("OPENAI_BASE_URL")

if not api_key:
    print("ERROR: UDACITY_OPENAI_API_KEY not found")
    sys.exit(1)
if not api_base:
    print("ERROR: OPENAI_BASE_URL not found")
    sys.exit(1)

print(f"API Key: {'*' * 20}{api_key[-4:]}")
print(f"API Base: {api_base}")
print("Environment variables OK!")

# Now import the main system
from multi_agent_system import init_database, orchestrator_agent

# Initialize database
print("\nInitializing database...")
init_database()

# Test a simple query
print("\nTesting orchestrator agent...")
test_request = """
Date: 2025-01-15
Context: Event planner organizing a wedding
Customer Request: I need a quote for 500 invitation cards for a wedding next month.

Please process this request appropriately.
"""

try:
    response = orchestrator_agent.run(test_request)
    print("\n" + "="*80)
    print("RESPONSE:")
    print("="*80)
    print(response)
    print("="*80)
    print("\nTest successful!")
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
