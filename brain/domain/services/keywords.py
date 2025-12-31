from uuid import UUID


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


def collect_cleanup_keyword_names(
    link_targets: list[str],
    represents_keyword_id: UUID | None,
    title: str | None,
) -> list[str]:
    names = list(link_targets)
    if represents_keyword_id and title:
        names.append(title)
    return normalize_keyword_names(names)
