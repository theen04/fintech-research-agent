from unittest.mock import patch
import pytest
from langchain_classic.agents import AgentExecutor
from fintech_research_agent.schemas import ResearchResponse
from fintech_research_agent.agent import create_agent_executor


class TestCreateAgentExecutor:
    """Tests for research agent construction."""

    @patch("fintech_research_agent.agent.ChatOllama")
    def test_creates_agent_executor(self, mock_llm):
        """Test that the agent executor is created successfully."""

        executor = create_agent_executor(
            run_id="test-run-001"
        )

        assert isinstance(executor, AgentExecutor)
        mock_llm.assert_called_once_with(
            model="qwen3:30b",
            temperature=0,
        )

    @patch("fintech_research_agent.agent.ChatOllama")
    def test_registers_research_tools(self, mock_llm):
        """Test that the expected research tools are registered."""

        executor = create_agent_executor(
            run_id="test-run-001"
        )

        tool_names = {
            tool.name
            for tool in executor.tools
        }

        assert "duckduckgo_tool" in tool_names
        assert "wikipedia_search" in tool_names

    @patch("fintech_research_agent.agent.ChatOllama")
    def test_executor_has_expected_configuration(self, mock_llm):
        """Test important AgentExecutor configuration."""

        executor = create_agent_executor(
            run_id="test-run-001"
        )

        assert executor.tools
        assert len(executor.tools) == 2
        assert executor.agent is not None

    @patch("fintech_research_agent.agent.ChatOllama")
    def test_accepts_run_id(self, mock_llm):
        """Test that create_agent_executor accepts a run ID."""

        executor = create_agent_executor(
            run_id="2026-08-16-test"
        )

        assert executor is not None

class TestAgentIntegration:
    """Integration tests for the full research agent."""

    @pytest.mark.integration
    def test_agent_returns_structured_response(self):
        """Test that the live agent returns a valid ResearchResponse."""

        executor = create_agent_executor(
            run_id="integration-test-001"
        )

        result = executor.invoke({
            "query": (
                "Research the current adoption of AI and machine learning "
                "in FinTech startups. Focus on major use cases and trends."
            )
        })

        assert "output" in result

        response = ResearchResponse.model_validate_json(
            result["output"]
        )

        assert response.topic
        assert response.executive_summary
        assert response.key_findings
        assert response.entities
        assert response.source_urls
        assert response.tools_used
        assert response.confidence_notes