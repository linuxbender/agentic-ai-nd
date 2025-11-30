# OpenAI API Key Information

## 1. Environment Variables

For OpenAI API access in this project, use the following environment variables:

- **`UDACITY_OPENAI_API_KEY`** - Your OpenAI API key
- **`OPENAI_BASE_URL`** - The base URL for the OpenAI API endpoint

These variables are pre-configured in the `.env` file located in the root directory of the project.

## 2. Setup Instructions

### 2.1 Loading Environment Variables

The project uses `python-dotenv` to load environment variables. Here's how to use them:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key and base URL
api_key = os.getenv("UDACITY_OPENAI_API_KEY")
api_base = os.getenv("OPENAI_BASE_URL")
```

### 2.2 Configuration for Different Frameworks

#### Using **smolagents**:
```python
from smolagents import OpenAIServerModel
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.getenv("UDACITY_OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL")
)
```

#### Using **pydantic-ai**:
```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
import os
from dotenv import load_dotenv

load_dotenv()

model = OpenAIModel(
    'gpt-4o-mini',
    api_key=os.getenv("UDACITY_OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

agent = Agent(model=model)
```

#### Using **OpenAI SDK directly**:
```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("UDACITY_OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
```

## 3. Recommended Models

For this project, the following models are recommended:

- **`gpt-4o-mini`** - Fast, efficient, cost-effective for most tasks
- **`gpt-4o`** - More capable for complex reasoning tasks
- **`gpt-4-turbo`** - Balance between performance and cost

## 4. Best Practices

### 4.1 Security
- ✅ Never hardcode API keys in your source code
- ✅ Always use environment variables
- ✅ Add `.env` to your `.gitignore` file
- ✅ Don't commit API keys to version control

### 4.2 Error Handling
```python
import os
from dotenv import load_dotenv

load_dotenv()

# Validate that required environment variables are set
api_key = os.getenv("UDACITY_OPENAI_API_KEY")
api_base = os.getenv("OPENAI_BASE_URL")

if not api_key:
    raise ValueError("UDACITY_OPENAI_API_KEY environment variable is not set")
if not api_base:
    raise ValueError("OPENAI_BASE_URL environment variable is not set")
```

### 4.3 Rate Limiting
- Be mindful of API rate limits
- Implement retry logic with exponential backoff
- Monitor your API usage

## 5. Troubleshooting

### Common Issues:

**Issue**: `KeyError` or `None` value when accessing environment variables
- **Solution**: Ensure `.env` file exists and `load_dotenv()` is called before accessing variables

**Issue**: `Authentication Error`
- **Solution**: Verify that `UDACITY_OPENAI_API_KEY` is correctly set and valid

**Issue**: `Connection Error`
- **Solution**: Check that `OPENAI_BASE_URL` is correct and accessible

## 6. Example: Complete Agent Setup

```python
import os
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, OpenAIServerModel, tool

# Load environment variables
load_dotenv()

# Validate environment variables
if not os.getenv("UDACITY_OPENAI_API_KEY"):
    raise ValueError("Missing UDACITY_OPENAI_API_KEY")

# Initialize model
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_key=os.getenv("UDACITY_OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL")
)

# Create agent
agent = ToolCallingAgent(
    tools=[],  # Add your tools here
    model=model,
    name="my_agent"
)

# Use the agent
result = agent.run("Your prompt here")
print(result)
```

---

**Note**: Always refer to the official documentation of your chosen framework for the most up-to-date configuration options.
