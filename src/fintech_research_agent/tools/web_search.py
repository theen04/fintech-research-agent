from langchain_classic.tools import tool
from ddgs import DDGS

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