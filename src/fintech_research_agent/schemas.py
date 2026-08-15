from pydantic import BaseModel, Field
from typing import List


class ResearchResponse(BaseModel):
    """Structured output returned by the research agent."""

    topic: str = Field(
        description="Primary topic researched"
    )

    executive_summary: str = Field(
        description="Concise executive summary of the research findings"
    )

    key_findings: List[str] = Field(
        description="Most important findings discovered during research"
    )

    entities: List[str] = Field(
        description="Key companies, technologies, organizations, people, or concepts identified"
    )

    source_urls: List[str] = Field(
        description="URLs of sources used during research"
    )

    tools_used: List[str] = Field(
        description="Tools used by the agent during research"
    )

    confidence_notes: str = Field(
        description="Notes about source quality, limitations, or confidence in findings"
    )