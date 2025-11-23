"""
Unit tests for individual agents.
"""
import pytest
from unittest.mock import patch, Mock
from agents.feedstock_analyst import FeedstockAnalystAgent
from agents.distillation_planner import DistillationPlannerAgent
from agents.market_analyst import MarketAnalystAgent
from agents.production_optimizer import ProductionOptimizerAgent
from models import AgentResponse


class TestFeedstockAnalystAgent:
    """Tests for FeedstockAnalystAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = FeedstockAnalystAgent()
        assert agent.name == "Feedstock Analyst"
        assert "petrochemical expert" in agent.system_prompt.lower()
    
    def test_execute_success(self, mock_llm_client, sample_feedstock_name):
        """Test successful execution of feedstock analysis."""
        agent = FeedstockAnalystAgent()
        
        mock_llm_client.chat.completions.create.return_value.choices[0].message.content = \
            "WTI is a light sweet crude with high API gravity."
        
        result = agent.execute(sample_feedstock_name)
        
        assert isinstance(result, AgentResponse)
        assert result.agent_name == "Feedstock Analyst"
        assert result.success is True
        assert len(result.content) > 0
        mock_llm_client.chat.completions.create.assert_called_once()
    
    def test_execute_with_error(self, sample_feedstock_name):
        """Test execution with API error."""
        agent = FeedstockAnalystAgent()
        
        with patch('agents.base.client.chat.completions.create', side_effect=Exception("API Error")):
            result = agent.execute(sample_feedstock_name)
            
            assert isinstance(result, AgentResponse)
            assert "Error" in result.content


class TestDistillationPlannerAgent:
    """Tests for DistillationPlannerAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = DistillationPlannerAgent()
        assert agent.name == "Distillation Planner"
        assert "distillation tower" in agent.system_prompt.lower()
    
    def test_execute_success(self, mock_llm_client, sample_feedstock_analysis):
        """Test successful execution of distillation planning."""
        agent = DistillationPlannerAgent()
        
        mock_llm_client.chat.completions.create.return_value.choices[0].message.content = \
            "Gasoline: 45%, Diesel: 30%, Kerosene: 15%, Other: 10%"
        
        result = agent.execute(sample_feedstock_analysis)
        
        assert isinstance(result, AgentResponse)
        assert result.agent_name == "Distillation Planner"
        assert result.success is True
        assert len(result.content) > 0
    
    def test_execute_includes_analysis(self, mock_llm_client, sample_feedstock_analysis):
        """Test that feedstock analysis is included in the prompt."""
        agent = DistillationPlannerAgent()
        result = agent.execute(sample_feedstock_analysis)
        
        call_args = mock_llm_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert sample_feedstock_analysis in user_message


class TestMarketAnalystAgent:
    """Tests for MarketAnalystAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = MarketAnalystAgent()
        assert agent.name == "Market Analyst"
        assert "market analyst" in agent.system_prompt.lower()
    
    def test_execute_success(self, mock_llm_client, sample_distillation_plan):
        """Test successful execution of market analysis."""
        agent = MarketAnalystAgent()
        
        mock_llm_client.chat.completions.create.return_value.choices[0].message.content = \
            "High demand for gasoline, medium for diesel"
        
        result = agent.execute(sample_distillation_plan)
        
        assert isinstance(result, AgentResponse)
        assert result.agent_name == "Market Analyst"
        assert result.success is True


class TestProductionOptimizerAgent:
    """Tests for ProductionOptimizerAgent."""
    
    def test_initialization(self):
        """Test agent initialization."""
        agent = ProductionOptimizerAgent()
        assert agent.name == "Production Optimizer"
        assert "optimization" in agent.system_prompt.lower()
    
    def test_execute_success(self, mock_llm_client, sample_distillation_plan, sample_market_analysis):
        """Test successful execution of production optimization."""
        agent = ProductionOptimizerAgent()
        
        mock_llm_client.chat.completions.create.return_value.choices[0].message.content = \
            "Prioritize gasoline production due to high market demand"
        
        result = agent.execute(sample_distillation_plan, sample_market_analysis)
        
        assert isinstance(result, AgentResponse)
        assert result.agent_name == "Production Optimizer"
        assert result.success is True
    
    def test_execute_includes_both_inputs(self, mock_llm_client, 
                                         sample_distillation_plan, 
                                         sample_market_analysis):
        """Test that both distillation plan and market data are included."""
        agent = ProductionOptimizerAgent()
        result = agent.execute(sample_distillation_plan, sample_market_analysis)
        
        call_args = mock_llm_client.chat.completions.create.call_args
        user_message = call_args[1]['messages'][1]['content']
        assert sample_distillation_plan in user_message
        assert sample_market_analysis in user_message
    
    def test_execute_uses_lower_temperature(self, mock_llm_client,
                                           sample_distillation_plan,
                                           sample_market_analysis):
        """Test that optimization uses lower temperature for more deterministic output."""
        agent = ProductionOptimizerAgent()
        result = agent.execute(sample_distillation_plan, sample_market_analysis)
        
        call_args = mock_llm_client.chat.completions.create.call_args
        assert call_args[1]['temperature'] == 0.6


class TestAgentResponse:
    """Tests for AgentResponse dataclass."""
    
    def test_creation_with_defaults(self):
        """Test creating AgentResponse with default values."""
        response = AgentResponse(
            agent_name="Test Agent",
            content="Test content"
        )
        assert response.agent_name == "Test Agent"
        assert response.content == "Test content"
        assert response.success is True
        assert response.error is None
    
    def test_creation_with_error(self):
        """Test creating AgentResponse with error."""
        response = AgentResponse(
            agent_name="Test Agent",
            content="",
            success=False,
            error="Test error message"
        )
        assert response.success is False
        assert response.error == "Test error message"
