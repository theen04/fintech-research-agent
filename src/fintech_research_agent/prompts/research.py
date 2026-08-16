from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

def create_research_prompt():

    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a research assistant.

Your task:

1. Use search tools to gather information about the topic.
2. After gathering information, provide your final answer.

IMPORTANT:
Your final response MUST be valid JSON matching this schema:

{format_instructions}

Track which tools you use and which sources you find.
""",
        ),
        ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])