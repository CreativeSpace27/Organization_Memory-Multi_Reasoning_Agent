def expand_query(query: str):
    base = query.lower()

    expansions = [base]

    if "rate limit" in base:
        expansions += [
            "http 429 handling",
            "api throttling frontend",
            "debounce throttle react"
        ]

    return list(set(expansions))