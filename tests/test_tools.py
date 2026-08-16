"""
Unit tests for research agent tools.

External search services are mocked so these tests:
- do not require network access
- do not depend on live search results
- run quickly and deterministically
"""

import json
from unittest.mock import MagicMock, patch
from fintech_research_agent.tools.web_search import duckduckgo_tool
from fintech_research_agent.tools.wikipedia import wikipedia_search


class TestDuckDuckGoTool:
    """Tests for the DuckDuckGo search tool."""

    @patch("fintech_research_agent.tools.web_search.DDGS")
    def test_successful_search(self, mock_ddgs):
        """Test that search results are formatted correctly."""

        mock_ddgs.return_value.text.return_value = [
            {
                "title": "Test Result 1",
                "href": "https://example.com/1",
                "body": "This is the first test result.",
            },
            {
                "title": "Test Result 2",
                "href": "https://example.com/2",
                "body": "This is the second test result.",
            },
        ]

        result = duckduckgo_tool.invoke({"query": "test query"})

        assert "Test Result 1" in result
        assert "https://example.com/1" in result
        assert "This is the first test result." in result

        assert "Test Result 2" in result
        assert "https://example.com/2" in result
        assert "This is the second test result." in result

        mock_ddgs.return_value.text.assert_called_once_with(
            "test query",
            max_results=5,
        )

    @patch("fintech_research_agent.tools.web_search.DDGS")
    def test_empty_search_results(self, mock_ddgs):
        """Test that empty search results are handled gracefully."""

        mock_ddgs.return_value.text.return_value = []

        result = duckduckgo_tool.invoke({"query": "obscure query"})

        assert result == "No results found for query: obscure query"

        mock_ddgs.return_value.text.assert_called_once_with(
            "obscure query",
            max_results=5,
        )

    @patch("fintech_research_agent.tools.web_search.DDGS")
    def test_search_exception_handling(self, mock_ddgs):
        """Test that search exceptions are handled gracefully."""

        mock_ddgs.return_value.text.side_effect = Exception("API Error")

        result = duckduckgo_tool.invoke({"query": "test query"})

        assert result == "Error performing search: API Error"

class TestWikipediaSearch:
    """Tests for the Wikipedia search tool."""

    @staticmethod
    def _response(data):
        """Create a mocked HTTP response containing JSON data."""

        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps(data).encode("utf-8")
        return response

    @patch("urllib.request.urlopen")
    def test_successful_search(self, mock_urlopen):
        """Test successful Wikipedia article retrieval."""

        search_response = {
            "query": {
                "search": [
                    {"title": "Artificial Intelligence"}
                ]
            }
        }

        summary_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Artificial Intelligence",
                        "extract": "This is a test summary about AI.",
                        "fullurl": (
                            "https://en.wikipedia.org/wiki/"
                            "Artificial_intelligence"
                        ),
                    }
                }
            }
        }

        mock_urlopen.side_effect = [
            self._response(search_response),
            self._response(summary_response),
        ]

        result = wikipedia_search.invoke({
            "query": "Artificial Intelligence"
        })

        assert "Wikipedia Article: Artificial Intelligence" in result
        assert "https://en.wikipedia.org/wiki/Artificial_intelligence" in result
        assert "This is a test summary about AI." in result
        assert mock_urlopen.call_count == 2

    @patch("urllib.request.urlopen")
    def test_no_article_found(self, mock_urlopen):
        """Test handling when Wikipedia returns no search results."""

        search_response = {
            "query": {
                "search": []
            }
        }

        mock_urlopen.side_effect = [
            self._response(search_response),
        ]

        result = wikipedia_search.invoke({"query": "obscure topic"})

        assert result == (
            "No Wikipedia article found for 'obscure topic'"
        )

        assert mock_urlopen.call_count == 1

    @patch("urllib.request.urlopen")
    def test_missing_page(self, mock_urlopen):
        """Test handling when the Wikipedia page is marked as missing."""

        search_response = {
            "query": {
                "search": [
                    {"title": "Test Article"}
                ]
            }
        }

        summary_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Test Article",
                        "missing": True,
                    }
                }
            }
        }

        mock_urlopen.side_effect = [
            self._response(search_response),
            self._response(summary_response),
        ]

        result = wikipedia_search.invoke({"query": "Test Article"})

        assert result == (
            "No Wikipedia article found for 'Test Article'"
        )

        assert mock_urlopen.call_count == 2

    @patch("urllib.request.urlopen")
    def test_no_summary_available(self, mock_urlopen):
        """Test handling when an article has no summary."""

        search_response = {
            "query": {
                "search": [
                    {"title": "Test Article"}
                ]
            }
        }

        summary_response = {
            "query": {
                "pages": {
                    "123": {
                        "title": "Test Article",
                        "extract": "",
                        "fullurl": (
                            "https://en.wikipedia.org/wiki/Test_Article"
                        ),
                    }
                }
            }
        }

        mock_urlopen.side_effect = [
            self._response(search_response),
            self._response(summary_response),
        ]

        result = wikipedia_search.invoke({"query": "Test Article"})

        assert "no summary was available" in result
        assert "Test Article" in result

    @patch("urllib.request.urlopen")
    def test_search_exception_handling(self, mock_urlopen):
        """Test that HTTP/API errors are handled gracefully."""

        mock_urlopen.side_effect = Exception("Wikipedia API Error")

        result = wikipedia_search.invoke({"query": "test query"})

        assert result == (
            "Error searching Wikipedia: Wikipedia API Error"
        )