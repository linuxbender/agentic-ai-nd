# Refinery Optimization System

A sophisticated multi-agent system for optimizing refinery operations using prompt chaining architecture. This project demonstrates how multiple AI agents can work sequentially to solve complex decision-making problems in the petroleum refining industry.

## 🎯 Overview

The system analyzes crude oil feedstock and provides optimized production recommendations by chaining four specialized AI agents. Each agent performs a specific analysis and passes its output to the next, creating a comprehensive optimization pipeline.

## 🏗️ Architecture

The system implements a **Prompt Chaining** pattern with 4 specialized AI agents:

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| 🔬 **Feedstock Analyst** | Analyzes crude oil composition | Feedstock name | Chemical composition & characteristics |
| ⚗️ **Distillation Planner** | Plans refinery operations | Feedstock analysis | Product yield estimates (%) |
| 📊 **Market Analyst** | Evaluates market conditions | Product yields | Demand & profitability analysis |
| 🎯 **Production Optimizer** | Recommends strategy | Yields + Market data | Optimized production plan |

### Workflow Flow

```
Feedstock Input → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Final Recommendation
```

Each agent's output becomes the next agent's input, creating a sequential reasoning chain.

## 📁 Project Structure

```
lesson-6/
├── main.py                          # Application entry point
├── models.py                        # Data models (AgentResponse)
├── workflow.py                      # Workflow orchestration
├── utils.py                         # Utility functions
├── requirements.txt                 # Core dependencies
├── requirements-dev.txt             # Development dependencies
├── pytest.ini                       # Test configuration
├── README.md                        # This file
├── agents/                          # Agent implementations
│   ├── __init__.py
│   ├── base.py                      # RefineryAgent base class
│   ├── feedstock_analyst.py         # Agent 1
│   ├── distillation_planner.py      # Agent 2
│   ├── market_analyst.py            # Agent 3
│   └── production_optimizer.py      # Agent 4
└── tests/                           # Comprehensive test suite
    ├── __init__.py
    ├── conftest.py                  # Pytest fixtures & mocks
    ├── test_agents.py               # Unit tests (30+ tests)
    ├── test_workflow.py             # Integration tests
    └── __pycache__/
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key
- Virtual environment (recommended)

### Installation

```bash
# 1. Navigate to the project directory
cd Course-02/lesson-6

# 2. Install core dependencies
pip install -r requirements.txt

# 3. (Optional) Install development dependencies for testing
pip install -r requirements-dev.txt

# 4. Set up environment variables
# Create a .env file in the project root
echo "OPENAI_API_KEY=your_api_key_here" > ../../.env
```

### Running the System

```bash
# Run the complete workflow
python main.py
```

**Expected Output:**
```
================================================================================
🏭 REFINERY OPTIMIZATION WORKFLOW
📦 Processing feedstock: West Texas Intermediate Crude
================================================================================

🔬 [Feedstock Analyst] Analyzing feedstock: West Texas Intermediate Crude...
✅ [Feedstock Analyst] Analysis completed.

--- FEEDSTOCK ANALYSIS ---
[Detailed chemical composition and characteristics...]

⚗️  [Distillation Planner] Planning distillation process...
✅ [Distillation Planner] Distillation plan created.

--- DISTILLATION PLAN ---
[Product yield percentages...]

📊 [Market Analyst] Analyzing market conditions...
✅ [Market Analyst] Market analysis completed.

--- MARKET ANALYSIS ---
[Market demand and profitability insights...]

🎯 [Production Optimizer] Optimizing production strategy...
✅ [Production Optimizer] Optimization completed.

================================================================================
🎯 OPTIMIZED PRODUCTION RECOMMENDATION
================================================================================
[Final production recommendations...]

✨ Workflow completed!
```

## 🧪 Testing

The project includes a comprehensive test suite with 30+ unit and integration tests.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_agents.py

# Run specific test class
pytest tests/test_agents.py::TestFeedstockAnalystAgent

# Run specific test
pytest tests/test_agents.py::TestFeedstockAnalystAgent::test_initialization

# Run tests with specific marker
pytest -m unit
```

### Test Coverage

The test suite covers:

| Category | Coverage |
|----------|----------|
| ✅ Agent initialization | All 4 agents |
| ✅ LLM interaction handling | Success & error cases |
| ✅ Error handling | API failures & exceptions |
| ✅ Data flow between agents | Sequential chaining |
| ✅ Complete workflow execution | End-to-end integration |
| ✅ Input validation | Type checking & constraints |
| ✅ Response structure | AgentResponse dataclass |

### Test Structure

- **`conftest.py`**: Shared fixtures and mocks for OpenAI API
- **`test_agents.py`**: Unit tests for individual agents (20+ tests)
- **`test_workflow.py`**: Integration tests for workflow (10+ tests)

## 💡 Usage Examples

### Example 1: Basic Workflow

```python
from workflow import RefineryOptimizationWorkflow

# Initialize the workflow
workflow = RefineryOptimizationWorkflow()

# Run complete analysis
results = workflow.run("West Texas Intermediate Crude")

# Access individual results
print(results['feedstock_analysis'].content)
print(results['production_optimization'].content)
```

### Example 2: Save Results to JSON

```python
from workflow import RefineryOptimizationWorkflow
from utils import save_results_to_json

workflow = RefineryOptimizationWorkflow()
results = workflow.run("Brent Crude Oil")

# Save results for later analysis
save_results_to_json(results, "brent_crude_analysis.json")
```

### Example 3: Use Individual Agents

```python
from agents.feedstock_analyst import FeedstockAnalystAgent
from agents.distillation_planner import DistillationPlannerAgent

# Use agents independently
analyst = FeedstockAnalystAgent()
analysis = analyst.execute("Light Sweet Crude")

planner = DistillationPlannerAgent()
plan = planner.execute(analysis.content)

print(f"Analysis: {analysis.content}")
print(f"Plan: {plan.content}")
```

### Example 4: Test Different Feedstocks

```python
from workflow import RefineryOptimizationWorkflow

workflow = RefineryOptimizationWorkflow()

feedstocks = [
    "West Texas Intermediate Crude",
    "Brent Crude Oil",
    "Dubai Crude",
    "Heavy Sour Crude"
]

for feedstock in feedstocks:
    print(f"\n{'='*60}")
    print(f"Analyzing: {feedstock}")
    print('='*60)
    results = workflow.run(feedstock)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root (Course-02/):

```env
OPENAI_API_KEY=your_api_key_here
```

### OpenAI Configuration

The system uses the following OpenAI settings (configured in `agents/base.py`):

```python
client = OpenAI(
    base_url="https://openai.vocareum.com/v1",  # Vocareum endpoint
    api_key=os.getenv("OPENAI_API_KEY"),
)

# Model: gpt-4o-mini
# Temperature: 0.7 (default), 0.6 (optimizer)
```

## 📊 Data Models

### AgentResponse

Each agent returns a structured `AgentResponse` object:

```python
@dataclass
class AgentResponse:
    agent_name: str            # Name of the agent that generated the response
    content: str               # The actual LLM response content
    success: bool = True       # Whether the operation was successful
    error: Optional[str] = None # Error message if the operation failed
```

**Example:**
```python
response = AgentResponse(
    agent_name="Feedstock Analyst",
    content="WTI is a light sweet crude with API gravity 39.6...",
    success=True
)
```

## 🎯 Design Principles

### SOLID Principles Applied

- **Single Responsibility**: Each agent focuses on one specific analysis task
- **Open/Closed**: Base `RefineryAgent` class is open for extension, closed for modification
- **Liskov Substitution**: All agent classes can be used interchangeably through base class
- **Interface Segregation**: Agents implement only the `execute()` method they need
- **Dependency Inversion**: Agents depend on abstractions (base class) not implementations

### Additional Principles

- ✅ **Modularity**: Agents can be used independently or in workflows
- ✅ **Testability**: Comprehensive test coverage with mocked LLM calls
- ✅ **Type Safety**: Full type hints throughout the codebase
- ✅ **Error Handling**: Graceful handling of API failures
- ✅ **Clean Code**: Clear naming, documentation, and structure

## 🔍 Key Concepts Demonstrated

1. **Prompt Chaining**: Sequential agent execution where each output feeds the next input
2. **Agent Architecture**: Specialized AI agents with distinct roles and responsibilities
3. **LLM Integration**: Using OpenAI's API for natural language processing
4. **Test-Driven Development**: Comprehensive unit and integration tests
5. **Professional Python**: Type hints, dataclasses, proper project structure

## 📈 Future Enhancements

### Potential Improvements

- [ ] **Pydantic Models**: Add structured output validation with Pydantic
- [ ] **Async Execution**: Implement parallel agent execution where possible
- [ ] **Caching**: Add result caching to reduce API calls
- [ ] **Web API**: Create FastAPI/Flask interface for HTTP access
- [ ] **Monitoring**: Add logging, metrics, and observability
- [ ] **Multi-LLM**: Support for multiple LLM providers (Anthropic, Cohere, etc.)
- [ ] **Streaming**: Real-time streaming of agent outputs
- [ ] **Persistence**: Database storage for results and audit trail
- [ ] **UI Dashboard**: Web interface for visualization and interaction

## 🤝 Contributing

This is an educational project. Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Learning Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [AI Agent Design Patterns](https://www.deeplearning.ai/)

## 👨‍💻 Author

Created as part of Course 02, Lesson 6: Prompt Chaining Workflows

---

**Note**: This project demonstrates educational concepts and should not be used for production refinery operations without proper validation and safety measures.
