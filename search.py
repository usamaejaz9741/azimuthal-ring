from duckduckgo_search import DDGS

def quick_search(query: str, max_results: int = 3):
    """
    Returns a small snippet of search results.
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
        return f"Search failed: {e}"
