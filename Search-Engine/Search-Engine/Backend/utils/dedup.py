# utils/dedup.py

def deduplicate(results):
    seen = set()
    unique = []

    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique