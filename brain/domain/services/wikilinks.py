import re

# Example 1: [[Child]] -> ["Child"]
# Example 2: [[Child|alias]] -> ["Child"]
WIKILINK_PATTERN = re.compile(r"\[\[([^\[\]\n]+)\]\]")


def extract_link_targets(text: str) -> list[str]:
    if not text:
        return []

    raw_titles = WIKILINK_PATTERN.findall(text)
    seen: set[str] = set()
    targets: list[str] = []
    for title in raw_titles:
        cleaned = title.strip()
        if "|" in cleaned:
            cleaned = cleaned.split("|", 1)[0].strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            targets.append(cleaned)
    return targets


def extract_wikilinks(text: str) -> list[str]:
    return extract_link_targets(text)
