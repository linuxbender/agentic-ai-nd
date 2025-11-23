"""
Pytest configuration and fixtures for refinery optimization tests.
"""
import pytest
from unittest.mock import Mock, patch
from models import AgentResponse


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Mock LLM response"
    return mock_response


@pytest.fixture
def sample_feedstock_name():
    """Sample feedstock name for testing."""
    return "West Texas Intermediate Crude"


@pytest.fixture
def sample_feedstock_analysis():
    """Sample feedstock analysis response."""
    return """West Texas Intermediate (WTI) Crude is a high-quality, light sweet crude oil.
Key components:
- API Gravity: 39.6° (light crude)
- Sulfur Content: 0.24% (sweet crude)
- High paraffin content
Excellent suitability for gasoline and diesel production."""


@pytest.fixture
def sample_distillation_plan():
    """Sample distillation plan response."""
    return """Based on WTI analysis, potential yields:
- Gasoline: 45%
- Diesel: 28%
- Kerosene: 15%
- Other fractions: 12%"""


@pytest.fixture
def sample_market_analysis():
    """Sample market analysis response."""
    return """Market Analysis:
- Gasoline: High demand, high profitability
- Diesel: Medium demand, stable prices
- Kerosene: Low demand, seasonal variations"""


@pytest.fixture
def mock_llm_client():
    """Mock the OpenAI client."""
    with patch('agents.base.client') as mock_client:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Mock response"
        mock_client.chat.completions.create.return_value = mock_response
        yield mock_client
