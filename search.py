"""Web search module for the Local AI Telegram Assistant.

This module provides functionality to perform quick web searches using
the DuckDuckGo Search API and return snippets of the results.
"""

import logging
from duckduckgo_search import DDGS


def quick_search(query: str, max_results: int = 3):
    """Perform a web search and return a summary of snippets.

    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of search results to retrieve.
            Defaults to 3.

    Returns:
        str: A concatenated string of search result snippets or a status message.
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(f"{r['title']}: {r['body']}")
        
        if not results:
            return "No results found."
        return "\n\n".join(results)
    except Exception as e:
        logging.error(f"Web search failed for query '{query}': {e}", exc_info=True)
        return "Web search is currently unavailable. Please try again later."
