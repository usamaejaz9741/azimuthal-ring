"""Web search module for the Local AI Telegram Assistant.

This module provides functionality to perform quick web searches using
the DuckDuckGo Search API and return snippets of the results.
"""

import logging
from duckduckgo_search import DDGS


def quick_search(query: str, max_results: int = 8):
    """Perform a web search and return a summary of snippets.

    Args:
        query (str): The search query string.
        max_results (int, optional): The maximum number of search results to retrieve.
            Defaults to 5.

    Returns:
        str: A concatenated string of search result snippets or a status message.
    """
    import time
    try:
        results = []
        with DDGS() as ddgs:
            # 1. Standard (Local IP Default)
            search_results = list(ddgs.text(query, max_results=max_results))
            
            # 2. English-Specific (Preference)
            if not search_results:
                time.sleep(1) # Bypass rate-limit
                search_results = list(ddgs.text(query, region="us-en", max_results=max_results))
            
            # 3. Global
            if not search_results:
                time.sleep(1)
                search_results = list(ddgs.text(query, region="wt-wt", max_results=max_results))
            
            # 4. Final attempt with lite backend
            if not search_results:
                time.sleep(1)
                search_results = list(ddgs.text(query, backend="lite", max_results=max_results))
            
            if search_results:
                for r in search_results[:max_results]:
                    results.append(f"{r['title']}: {r['body']}")
                return "\n".join(results)
            else:
                return "No results found for this query after multiple attempts."
    except Exception as e:
        logging.error(f"Web search failed for query '{query}': {e}", exc_info=True)
        return "Web search is currently unavailable. Please try again later."
