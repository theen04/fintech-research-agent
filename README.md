# FinTech AI Research Agent

An autonomous AI research agent that combines LLM reasoning, web-based research tools, structured outputs, and persistent research logging. The project demonstrates how an AI agent can be designed not only to answer questions, but also to create reusable research data for future analytics, machine learning, and retrieval workflows.

## Overview

The FinTech AI Research Agent uses LangChain and OpenAI to research a user-provided topic, select and invoke appropriate tools, synthesize findings, and produce a structured research response.

Research findings are also stored in an append-only research log. This creates a persistent corpus that can eventually support downstream tasks such as topic analysis, source evaluation, trend detection, model training, or Retrieval-Augmented Generation (RAG).

The project is designed to demonstrate **agent architecture and data lifecycle thinking**, rather than simply provide a conversational AI interface.

## Architecture

```text
                         Research Query
                              │
                              ▼
                    ┌───────────────────┐
                    │   Research Agent  │
                    │   LLM + LangChain │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        DuckDuckGo        Wikipedia       Future Tools
        Web Search          API
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌───────────────────┐
                    │  Research Log     │
                    │  Append-Only Data │
                    └─────────┬─────────┘
                              │
                              ▼
                 Future Analytics / ML / RAG
```

## Key Capabilities

* **Tool-using AI agent** — dynamically invokes research tools based on the task.
* **Web research** — retrieves current information through DuckDuckGo.
* **Knowledge retrieval** — accesses encyclopedic information through the Wikipedia API.
* **Structured output** — returns research findings using a Pydantic schema.
* **Persistent research logging** — appends findings to a reusable research corpus.
* **Modular architecture** — separates agent orchestration, schemas, tools, and application execution.
* **Extensible design** — additional tools and downstream data workflows can be added without restructuring the core application.

## Technology

| Category        | Technologies                 |
| --------------- | ---------------------------- |
| Language        | Python                       |
| AI / LLM        | OpenAI, LangChain            |
| Agent Framework | LangChain Classic            |
| Structured Data | Pydantic                     |
| Web Research    | DuckDuckGo, Wikipedia API    |
| Configuration   | python-dotenv                |
| Testing         | pytest                       |
| Packaging       | setuptools, `pyproject.toml` |

## Project Structure

```text
fintech_research_agent/
│
├── src/
│   └── fintech_research_agent/
│       ├── main.py
│       ├── agent.py
│       ├── schemas.py
│       └── tools.py
│
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
│
├── docs/
│   ├── architecture.png
│   └── sample_report.md
│
├── outputs/
│   └── .gitkeep
│
├── .env.example
├── pyproject.toml
└── README.md
```

### Module Responsibilities

**`main.py`**
Application entry point that executes a research request.

**`agent.py`**
Defines the LLM, prompt, tools, agent chain, and `AgentExecutor`.

**`schemas.py`**
Defines the Pydantic models used for structured research output.

**`tools.py`**
Contains the custom research and persistence tools used by the agent.

**`tests/`**
Contains unit and integration tests for tools and agent behavior.

## Setup

Create and activate a Python environment, then install the project in editable mode:

```bash
pip install -e ".[search,dev]"
```

Create a `.env` file containing the required OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Run the agent:

```bash
python -m fintech_research_agent.main
```

## Example Workflow

A research request is submitted to the agent:

```text
Research the adoption of AI and machine learning in FinTech startups.
```

The agent can then:

1. Search the web for relevant information.
2. Retrieve supporting information from Wikipedia.
3. Save research findings to the persistent research log.
4. Synthesize the collected information.
5. Return a structured research response containing the topic, summary, sources, and tools used.

## Research Data Lifecycle

A key design goal is to treat agent output as **data**, rather than disposable responses.

```text
Research Request
       ↓
Agent Research
       ↓
Raw Research Log
       ↓
Structured Research Data
       ↓
Analytics / ML / RAG
```

The current implementation focuses on the first stages of this lifecycle. The persistent research corpus provides a foundation for future experimentation with:

* Topic classification
* Topic clustering
* Source quality analysis
* Trend detection
* Research summarization
* Model training datasets
* Retrieval-Augmented Generation

## Future Development

Potential extensions include:

* Additional research and data sources
* Automated source quality evaluation
* Structured JSON/JSONL research storage
* Research topic classification and clustering
* Vector database integration
* Retrieval-Augmented Generation
* Evaluation of agent research quality
* Downstream machine learning using the accumulated research corpus

## Project Status

**In Development**

The core research agent, tool architecture, structured output, and persistent research logging are implemented. Testing, evaluation, and downstream data workflows are planned as subsequent development stages.

---

**Built with ❤️ and curiosity about AI in FinTech**