# FinTech AI Research Agent

An autonomous AI research agent that combines local LLM reasoning, web-based research tools, structured outputs, and persistent research logging.  

The project demonstrates how an AI agent can move beyond conversational question answering by autonomously selecting research tools, gathering information from multiple sources, synthesizing findings, and returning validated structured data.  

The project is designed to demonstrate **agent architecture, tool orchestration, structured data, testing, and data lifecycle thinking** rather than simply provide a conversational AI interface.  

## Overview

The FinTech AI Research Agent uses **Qwen3:30b running locally through Ollama** and LangChain to research a user-provided topic.  

The agent can select between complementary research tools:  

- **DuckDuckGo** for current web-based information, recent developments, and multiple perspectives
- **Wikipedia** for established concepts, historical context, and encyclopedic background

After gathering information, the agent synthesizes its findings into a validated `ResearchResponse` Pydantic model.  

Research findings can also be persisted to an append-only research log, creating a reusable corpus for future analytics, machine learning, and Retrieval-Augmented Generation (RAG) workflows.  

## Architecture

```text
                         Research Query
                              │
                              ▼
                    ┌───────────────────┐
                    │   Research Agent  │
                    │     Qwen3:30b     │
                    │     + LangChain   │
                    └─────────┬─────────┘
                              │
                       Tool Selection
                              │
              ┌───────────────┼───────────────┐
              ▼                               ▼
       ┌───────────────┐              ┌────────────────┐
       │  DuckDuckGo   │              │    Wikipedia   │
       │  Web Search   │              │      API       │
       └───────┬───────┘              └───────┬────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
                    ┌───────────────────┐
                    │ Research Synthesis│
                    └─────────┬─────────┘
                              ▼
                    ┌───────────────────┐
                    │ ResearchResponse  │
                    │     Pydantic      │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Research Log        Future Analytics
                                      / ML / RAG
```

## Key Capabilities

* **Tool-using AI agent** — dynamically selects research tools based on the information required.
* **Web research** — retrieves current information through DuckDuckGo.
* **Knowledge retrieval** — accesses encyclopedic information through the Wikipedia API.
* **Structured output** — validates research findings against a Pydantic schema.
* **Source tracking** — records URLs discovered during research.
* **Tool tracking** — records which research tools were used.
* **Confidence notes** — captures source quality, limitations, and uncertainty.
* **Persistent research** logging — creates a reusable research corpus.
* **Modular architecture** — separates agent orchestration, prompts, schemas, tools, services, and application execution.
* **Testable design** — separates fast unit tests from live agent integration tests.

## Structured Research Output

The agent returns a `ResearchResponse` containing:  

| **Field**               | **Description**                                                            |
| ------------------- | ---------------------------------------------------------------------- |
| `topic`             | Primary topic researched                                               |
| `executive_summary` | Concise summary of the research                                        |
| `key_findings`      | Most important findings discovered                                     |
| `entities`          | Companies, technologies, organizations, people, or concepts identified |
| `source_urls`       | URLs of sources used during research                                   |
| `tools_used`        | Research tools invoked by the agent                                    |
| `confidence_notes`  | Source quality, limitations, and uncertainty                           |


## Technology

| **Category**            | **Technologies**                 |
| ------------------- | ---------------------------- |
| Language            | Python 3.11+                 |
| LLM                 | Qwen3:30b                    |
| Local LLM Runtime   | Ollama                       |
| Agent Framework     | LangChain Classic            |
| Core LangChain      | LangChain Core               |
| Structured Data     | Pydantic                     |
| Web Research        | DuckDuckGo (`ddgs`)          |
| Knowledge Retrieval | Wikipedia API                |
| Configuration       | python-dotenv                |
| Testing             | pytest, pytest-cov           |
| Packaging           | setuptools, `pyproject.toml` |


## Project Structure

```text
fintech_research_agent/
│
├── src/
│   └── fintech_research_agent/
│       ├── __init__.py
│       ├── main.py
│       ├── agent.py
│       ├── schemas.py
│       │
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── research.py
│       │
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── web_search.py
│       │   └── wikipedia.py
│       │
│       └── services/
│           └── ...
│
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
│
├── docs/
│   ├── architecture.txt
│   ├── sample-report.md
│   └── testing_guide.md
│
├── outputs/
│   └── research_notes.txt
│
├── pyproject.toml
├── README.md
└── .env.example

### Module Responsibilities

**`main.py`**
Application entry point that executes a research request and manages the application workflow.  

**`agent.py`**
Configures the local Qwen3 model, research tools, prompt, tool-calling agent, and `AgentExecutor`.  

**`schemas.py`**
Defines the Pydantic models used to validate structured research output.  

**`prompts.py`**
Contains prompts that define the agent's research strategy, tool-selection guidance, source-quality expectations, and output requirements.  

**`tools.py`**
Contains the research tools available to the agent.  

* `web_search.py` — DuckDuckGo web search
* `wikipedia.py` — Wikipedia API search and retrieval

**`services.py`**  
Contains application services responsible for supporting workflows such as research persistence and output handling.  

**`tests/`**  
Contains unit tests for individual components and integration tests for the live agent workflow.  

## Setup

### 1 - Install Ollama

Install and run Ollama, then pull the Qwen3 model:  

```bash
ollama pull qwen3:30b
```

Make sure Ollama is running before executing the agent.  

### 2 - Create Python Environment

Create and activate a Python 3.11+ environment, then install the project:  

```bash
pip install -e ".[search,dev]"
```

### 3 - Run the agent

```bash
python -m fintech_research_agent.main
```

## Example Workflow

A research request is submitted to the agent:  

```text
Research the adoption of AI and machine learning in FinTech startups.
```

The agent then:  

1) Interprets the research question  
2) Determines which information is needed  
3) Selects appropriate research tools  
4) Searches DuckDuckGo and/or Wikipedia  
5) Evaluates and synthesizes the retrieved information  
6) Produces a structured ResearchResponse  
7) Records the tools and sources used  
8) Persists research findings for future workflows  

## Testing

The project separates fast unit tests from live integration tests.  

### Unit Tests
Run the standard test suite:  

```bash
pytest
```

Unit tests mock external research calls and verify individual components such as:  

* DuckDuckGo search behavior
* Wikipedia search behavior
* Error handling
* Empty search results
* Agent configuration

### Integration Tests
The integration test runs the actual Qwen3:30b model and research tools:  

```bash
pytest -m integration
```

This validates the complete workflow:  

```raw
Research Query
      ↓
Qwen3:30b
      ↓
Tool Selection
      ↓
Research Tools
      ↓
Research Synthesis
      ↓
ResearchResponse
```

Integration tests are intentionally separated because they require a running local LLM and take significantly longer than unit tests.  


## Research Data Lifecycle

A key design goal is to treat agent output as **data**, rather than disposable responses.   

```text
Research Request
       ↓
Agent Research
       ↓
Structured ResearchResponse
       ↓
Persistent Research Log
       ↓
Analytics / ML / RAG
```

The current implementation establishes the research and structured-output stages while providing the foundation for a reusable research corpus.  

Future workflows could use this corpus for:  

* Topic classification
* Topic clustering
* Source quality analysis
* Trend detection
* Research summarization
* Model training datasets
* Retrieval-Augmented Generation

## Current Status  

In Development

The current implementation includes:  

* Local Qwen3:30b inference through Ollama
* LangChain tool-calling agent
* DuckDuckGo web search
* Wikipedia retrieval
* Structured Pydantic output
* Modular project architecture
* Unit tests
* Live agent integration testing
* Research persistence foundation


Future development will focus on evaluation, source quality assessment, additional research tools and downstream analysis of the accumulated research corpus.

## Future Development  

Potential extensions include:
* Additional research and data sources
* Automated source quality evaluation
* Structured JSON/JSONL research storage
* Research topic classification and clustering
* Vector database integration
* Retrieval-Augmented Generation
* Agent research-quality evaluation
* Tool-selection evaluation
* Downstream machine learning using the accumulated research corpus

---

**Built with ❤️ and curiosity about AI in FinTech**