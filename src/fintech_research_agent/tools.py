"""
Custom tools for the AI Research Agent.

Each tool is decorated with @tool to make it compatible with LangChain agents.
The docstring of each function is crucial - it tells the LLM when and how to use the tool.
"""

import os
from datetime import datetime

from langchain_classic.tools import tool

def save_raw_text(
    text: str,
    query: str,
    tools_used: str,
    run_id: str,
) -> str:
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, "research_notes.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = (
        f"{'=' * 60}\n"
        f"Run ID: {run_id}\n"
        f"Timestamp: {timestamp}\n"
        f"{'=' * 60}\n\n"
        f"Query:\n{query}\n\n"
        f"Tools Used:\n{tools_used}\n\n"
        f"Findings:\n{text}\n\n"
    )

    existing_content = ""

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            existing_content = f.read()

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(record)
        f.write(existing_content)

    return filepath


@tool
def duckduckgo_tool(query: str) -> str:
    """
    Search DuckDuckGo for current information on a topic.
    
    Use this tool when you need:
    - Current events or news
    - Recent developments
    - Web-based information
    - Multiple perspectives on a topic
    
    Args:
        query: The search query string
        
    Returns:
        Formatted search results with titles and snippets
    """
    try:
        from ddgs import DDGS
        
        # Perform search
        results = DDGS().text(query, max_results=5)
        
        # Format results
        if not results:
            return f"No results found for query: {query}"
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   {result['body']}\n"
            )
        
        return "\n".join(formatted_results)
        
    except ImportError:
        return (
            "DuckDuckGo search is not available. "
            "Install it with: pip install ddgs"
        )
    except Exception as e:
        return f"Error performing search: {str(e)}"


@tool
def wikipedia_search(query: str) -> str:
    """
    Search Wikipedia for detailed, encyclopedic information on a topic.

    Use this tool when you need:
    - Historical information
    - Scientific concepts
    - Biographical information
    - Detailed explanations of topics
    - Well-established facts

    Args:
        query: The topic to search for on Wikipedia

    Returns:
        Summary of the Wikipedia article
    """
    try:
        import json
        from urllib.parse import urlencode
        from urllib.request import Request, urlopen

        search_params = urlencode({
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "utf8": 1,
            "srlimit": 1,
        })

        search_url = (
            f"https://en.wikipedia.org/w/api.php?{search_params}"
        )

        request = Request(
            search_url,
            headers={"User-Agent": "FinTech-AI-Agent/0.1"},
        )

        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        search_results = data.get("query", {}).get("search", [])

        if not search_results:
            return f"No Wikipedia article found for '{query}'"

        title = search_results[0]["title"]

        summary_params = urlencode({
            "action": "query",
            "prop": "extracts|info",
            "explaintext": 1,
            "exintro": 1,
            "inprop": "url",
            "titles": title,
            "format": "json",
            "utf8": 1,
        })

        summary_url = (
            f"https://en.wikipedia.org/w/api.php?{summary_params}"
        )

        request = Request(
            summary_url,
            headers={"User-Agent": "FinTech-AI-Agent/0.1"},
        )

        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        pages = data.get("query", {}).get("pages", {})
        page = next(iter(pages.values()))

        if "missing" in page:
            return f"No Wikipedia article found for '{query}'"

        summary = page.get("extract", "").strip()
        url = page.get("fullurl", "")

        if not summary:
            return f"Wikipedia article found, but no summary was available for '{title}'"

        return (
            f"Wikipedia Article: {title}\n"
            f"URL: {url}\n\n"
            f"Summary:\n{summary}"
        )

    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

@tool
def calculator(expression: str) -> str:
    """
    Perform mathematical calculations.
    
    Use this tool when you need to:
    - Calculate numbers
    - Perform arithmetic operations
    - Evaluate mathematical expressions
    
    Args:
        expression: A mathematical expression (e.g., "2 + 2", "10 * 5 - 3")
        
    Returns:
        The result of the calculation
        
    Example:
        calculator("100 / 4 + 10") returns "35.0"
    """
    try:
        # Security: Only allow safe mathematical operations
        # Using eval is dangerous, so we restrict to numbers and basic operators
        allowed_chars = set("0123456789+-*/()%. ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Expression contains invalid characters"
        
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
        
    except Exception as e:
        return f"Error calculating: {str(e)}"


# Export all tools for easy import
__all__ = [
    'duckduckgo_tool',
    'wikipedia_search',
    'save_raw_text',
    'calculator',
]