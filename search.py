import urllib.parse
import warnings
from typing import List, Dict


warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message=".*duckduckgo_search.*renamed to.*"
)

from duckduckgo_search import DDGS


def get_domain(url: str) -> str:
    """
    Extracts and normalizes a domain from a URL.

    Examples:
        https://www.bbc.com/news -> bbc.com
        https://edition.cnn.com/article -> cnn.com
        https://m.reuters.com/world -> reuters.com
    """
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.lower()

        
        prefixes = ["www.", "m.", "mobile.", "edition."]
        for prefix in prefixes:
            if domain.startswith(prefix):
                domain = domain[len(prefix):]

        
        parts = domain.split(".")
        if len(parts) >= 2:
            domain = ".".join(parts[-2:])

        return domain

    except Exception:
        return ""


def search_claim(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for evidence related to a news claim.

    Returns:
    [
        {
            "title": "...",
            "url": "...",
            "snippet": "...",
            "source": "bbc.com"
        }
    ]
    """

    if not query or not query.strip():
        return []

    results = []
    seen_urls = set()

    try:
        with DDGS() as ddgs:

            
            search_results = ddgs.text(
                query,
                max_results=max_results + 5
            )

            if not search_results:
                return []

            for result in search_results:

                url = result.get("href", "").strip()
                title = result.get("title", "").strip()
                snippet = result.get("body", "").strip()

                if not url:
                    continue

                
                if url in seen_urls:
                    continue

                seen_urls.add(url)

                domain = get_domain(url)

                results.append({
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                    "source": domain
                })

                
                if len(results) >= max_results:
                    break

    except Exception as e:
        print(f"[SEARCH ERROR] {e}")

    return results