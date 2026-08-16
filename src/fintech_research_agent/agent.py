from dotenv import load_dotenv

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent,
)

from .prompts.research import create_research_prompt
from .schemas import ResearchResponse
from .tools import (
    duckduckgo_tool,
    wikipedia_search,
)


def create_agent_executor(run_id: str) -> AgentExecutor:
    """Create and configure the research agent."""

    parser = PydanticOutputParser(
        pydantic_object=ResearchResponse
    )

    llm = ChatOllama(
        model="qwen3:30b",
        temperature=0
    )

    tools = [
        duckduckgo_tool,
        wikipedia_search,
    ]

    prompt = create_research_prompt().partial(
        format_instructions=parser.get_format_instructions()
    )


    # --------------------
    # Agent Chain
    # --------------------
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )

    # --------------------
    # Agent Executor
    # --------------------
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )