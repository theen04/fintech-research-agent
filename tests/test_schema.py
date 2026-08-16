import pytest
from pydantic import ValidationError

from fintech_research_agent.schemas import ResearchResponse


class TestResearchResponse:
    """Tests for ResearchResponse validation."""

    def test_valid_response(self):
        """Test creation of a valid research response."""

        response = ResearchResponse(
            topic="AI in FinTech",
            executive_summary="AI is increasingly used across FinTech.",
            key_findings=[
                "Fraud detection is a major use case.",
                "Machine learning is used in credit modeling.",
            ],
            entities=[
                "ZestFinance",
                "Open banking",
            ],
            source_urls=[
                "https://example.com/source1",
                "https://example.com/source2",
            ],
            tools_used=[
                "duckduckgo_tool",
            ],
            confidence_notes="Findings are based on publicly available sources.",
        )

        assert response.topic == "AI in FinTech"
        assert len(response.key_findings) == 2
        assert len(response.entities) == 2
        assert len(response.source_urls) == 2
        assert response.tools_used == ["duckduckgo_tool"]

    def test_missing_required_field(self):
        """Test that missing required fields raise ValidationError."""

        with pytest.raises(ValidationError):
            ResearchResponse(
                topic="AI in FinTech",
                executive_summary="Test summary.",
                key_findings=["Finding"],
                entities=["Entity"],
                source_urls=["https://example.com"],
                tools_used=["duckduckgo_tool"],
                # confidence_notes intentionally omitted
            )

    def test_wrong_type(self):
        """Test that an incorrect field type raises ValidationError."""

        with pytest.raises(ValidationError):
            ResearchResponse(
                topic="AI in FinTech",
                executive_summary="Test summary.",
                key_findings="This should be a list",
                entities=["Entity"],
                source_urls=["https://example.com"],
                tools_used=["duckduckgo_tool"],
                confidence_notes="Test notes.",
            )

    def test_list_fields_contain_strings(self):
        """Test that list fields reject non-string values."""

        with pytest.raises(ValidationError):
            ResearchResponse(
                topic="AI in FinTech",
                executive_summary="Test summary.",
                key_findings=[123],
                entities=["Entity"],
                source_urls=["https://example.com"],
                tools_used=["duckduckgo_tool"],
                confidence_notes="Test notes.",
            )