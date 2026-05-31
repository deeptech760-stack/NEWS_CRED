import sys
from search import search_claim

def main():
    
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  

    print("=== Web-Assisted News Credibility Checker - Search Test ===")
    
    
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])
    else:
        
        default_claim = "NASA discovers liquid water on Mars"
        try:
            claim = input(f"Enter a news claim to search [Default: '{default_claim}']: ").strip()
        except EOFError:
            claim = ""
        if not claim:
            claim = default_claim
    
    print(f"\nSearching for: '{claim}'...\n")
    results = search_claim(claim, max_results=5)
    
    if not results:
        print("No results found or search failed.")
        return

    print(f"Top {len(results)} Search Results:")
    for idx, r in enumerate(results, 1):
        print("=" * 60)
        print(f"[{idx}] {r['title']}")
        print(f"    Source  : {r['source']}")
        print(f"    URL     : {r['url']}")
        print(f"    Snippet : {r['snippet']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
