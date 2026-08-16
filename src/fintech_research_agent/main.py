from datetime import datetime

from fintech_research_agent.agent import create_agent_executor
from fintech_research_agent.services.persistence import save_raw_text


def main():
    query = "Research the adoption of AI and machine learning in FinTech startups."

    run_id = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    agent_executor = create_agent_executor(run_id)

    result = agent_executor.invoke({
        "query": query,
    })

    save_raw_text(
        text=result["output"],
        query=query,
        tools_used="duckduckgo_tool",
        run_id=run_id,
    )

    print(result["output"])


if __name__ == "__main__":
    main()