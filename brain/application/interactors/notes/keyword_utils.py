def normalize_keyword_names(names: list[str]) -> list[str]:
    """Normalize keyword names by trimming whitespace, removing empty strings, and deduplicating."""
    seen: set[str] = set()
    normalized: list[str] = []
    for name in names:
        trimmed = name.strip()
        if not trimmed or trimmed in seen:
            continue
        seen.add(trimmed)
        normalized.append(trimmed)
    return normalized
