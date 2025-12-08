# utils.py

def format_claims_with_citations(claims, citations):
    """
    Combine claims with citation sources for clean display
    """
    formatted = []
    for claim in claims:
        source = next((c['source'] for c in citations if c['claim'] == claim), "Unknown")
        formatted.append(f"{claim} → Source: {source}")
    return formatted
