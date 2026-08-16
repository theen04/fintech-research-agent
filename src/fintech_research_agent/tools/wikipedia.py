from langchain_classic.tools import tool


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
