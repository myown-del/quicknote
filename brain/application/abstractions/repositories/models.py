from dataclasses import dataclass


@dataclass
class WikilinkSuggestion:
    title: str
    represents_keyword: bool
