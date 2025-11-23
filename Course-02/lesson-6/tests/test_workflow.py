"""
Unit tests for workflow orchestration.
"""
import pytest
from unittest.mock import patch, Mock
from workflow import RefineryOptimizationWorkflow
from models import AgentResponse


class TestRefineryOptimizationWorkflow:
    """Tests for RefineryOptimizationWorkflow."""
    
    def test_initialization(self):
        """Test workflow initialization."""
        workflow = RefineryOptimizationWorkflow()
        assert workflow.feedstock_analyst is not None
        assert workflow.distillation_planner is not None
        assert workflow.market_analyst is not None
        assert workflow.production_optimizer is not None
    
    def test_run_executes_all_agents(self, mock_llm_client, sample_feedstock_name):
        """Test that run() executes all four agents in sequence."""
        workflow = RefineryOptimizationWorkflow()
        
        # Mock different responses for each agent
        responses = [
            "Feedstock analysis result",
            "Distillation plan result",
            "Market analysis result",
            "Production optimization result"
        ]
        
        def side_effect(*args, **kwargs):
            mock_resp = Mock()
            mock_resp.choices = [Mock()]
            mock_resp.choices[0].message.content = responses.pop(0)
            return mock_resp
        
        mock_llm_client.chat.completions.create.side_effect = side_effect
        
        results = workflow.run(sample_feedstock_name)
        
        assert len(results) == 4
        assert 'feedstock_analysis' in results
        assert 'distillation_plan' in results
        assert 'market_analysis' in results
        assert 'production_optimization' in results
        
        # Verify all results are AgentResponse objects
        for key, response in results.items():
            assert isinstance(response, AgentResponse)
            assert response.success is True
    
    def test_run_returns_correct_structure(self, mock_llm_client, sample_feedstock_name):
        """Test that run() returns correctly structured results."""
        workflow = RefineryOptimizationWorkflow()
        results = workflow.run(sample_feedstock_name)
        
        # Check feedstock analysis
        assert results['feedstock_analysis'].agent_name == "Feedstock Analyst"
        
        # Check distillation plan
        assert results['distillation_plan'].agent_name == "Distillation Planner"
        
        # Check market analysis
        assert results['market_analysis'].agent_name == "Market Analyst"
        
        # Check production optimization
        assert results['production_optimization'].agent_name == "Production Optimizer"
    
    def test_agent_chain_data_flow(self, mock_llm_client, sample_feedstock_name):
        """Test that data flows correctly between agents."""
        workflow = RefineryOptimizationWorkflow()
        
        call_count = 0
        captured_prompts = []
        
        def capture_call(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            captured_prompts.append(kwargs['messages'][1]['content'])
            
            mock_resp = Mock()
            mock_resp.choices = [Mock()]
            mock_resp.choices[0].message.content = f"Response {call_count}"
            return mock_resp
        
        mock_llm_client.chat.completions.create.side_effect = capture_call
        
        results = workflow.run(sample_feedstock_name)
        
        # Verify that each subsequent agent receives previous agent's output
        # Agent 2 should receive Agent 1's output
        assert "Response 1" in captured_prompts[1]
        
        # Agent 3 should receive Agent 2's output
        assert "Response 2" in captured_prompts[2]
        
        # Agent 4 should receive both Agent 2's and Agent 3's outputs
        assert "Response 2" in captured_prompts[3]
        assert "Response 3" in captured_prompts[3]
    
    def test_run_with_different_feedstocks(self, mock_llm_client):
        """Test workflow with different feedstock types."""
        workflow = RefineryOptimizationWorkflow()
        
        feedstocks = [
            "West Texas Intermediate Crude",
            "Brent Crude Oil",
            "Heavy Sour Crude"
        ]
        
        for feedstock in feedstocks:
            results = workflow.run(feedstock)
            assert len(results) == 4
            assert all(isinstance(r, AgentResponse) for r in results.values())


class TestWorkflowIntegration:
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow_execution(self, mock_llm_client, sample_feedstock_name):
        """Test complete workflow execution from start to finish."""
        workflow = RefineryOptimizationWorkflow()
        
        # Set up realistic mock responses
        mock_responses = [
            "WTI is a light sweet crude with API gravity 39.6",
            "Expected yields: Gasoline 45%, Diesel 30%, Kerosene 15%, Other 10%",
            "High demand for gasoline, medium for diesel, low for kerosene",
            "Recommend prioritizing gasoline production to maximize profitability"
        ]
        
        response_iter = iter(mock_responses)
        
        def get_next_response(*args, **kwargs):
            mock_resp = Mock()
            mock_resp.choices = [Mock()]
            mock_resp.choices[0].message.content = next(response_iter)
            return mock_resp
        
        mock_llm_client.chat.completions.create.side_effect = get_next_response
        
        results = workflow.run(sample_feedstock_name)
        
        # Verify complete execution
        assert results['feedstock_analysis'].content == mock_responses[0]
        assert results['distillation_plan'].content == mock_responses[1]
        assert results['market_analysis'].content == mock_responses[2]
        assert results['production_optimization'].content == mock_responses[3]
        
        # Verify LLM was called 4 times (once per agent)
        assert mock_llm_client.chat.completions.create.call_count == 4
