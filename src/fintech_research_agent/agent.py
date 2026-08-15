from dotenv import load_dotenv

#from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain_classic.agents.output_parsers.openai_tools import (
    OpenAIToolsAgentOutputParser,
)

from .schemas import ResearchResponse
from .tools import (
    duckduckgo_tool,
    wikipedia_search
)


load_dotenv()


def create_agent_executor(run_id: str) -> AgentExecutor:
    """Create and configure the research agent."""

    # --------------------
    # Output Parser
    # --------------------
    parser = PydanticOutputParser(
        pydantic_object=ResearchResponse
    )

    # --------------------
    # LLM
    # --------------------
    #llm = ChatOpenAI(
    #    model_name="gpt-4",
    #    temperature=0.4,
    #)

    llm = ChatOllama(
        model="qwen3:30b",
        temperature=0
    )

    # --------------------
    # Tools
    # --------------------

    tools = [
        duckduckgo_tool,
        wikipedia_search,
    ]

    llm_with_tools = llm.bind_tools(tools)

    # --------------------
    # Prompt
    # --------------------
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """You are a research assistant.

    Your task:

    1. Use search tools to gather information about the topic
    2. Save research findings using the save_raw_text tool
    3. After gathering all information, provide your final answer

    IMPORTANT: Your final response MUST be valid JSON matching this schema:
    {format_instructions}

    Track which tools you use and which sources you find.
    """,
        ),
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]).partial(
        format_instructions=parser.get_format_instructions()
    )

    # --------------------
    # Agent Chain
    # --------------------
    agent = (
        {
            "query": lambda x: x["query"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )

    # --------------------
    # Agent Executor
    # --------------------
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
    )