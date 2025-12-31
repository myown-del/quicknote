from dataclasses import dataclass

from brain.domain.entities.common import Entity


@dataclass
class GraphNode(Entity):
    id: str
    title: str
    kind: str
    represents_keyword: bool | None = None
    has_keyword_note: bool | None = None


@dataclass
class GraphConnection(Entity):
    from_id: str
    to_id: str
    kind: str


@dataclass
class GraphData(Entity):
    nodes: list[GraphNode]
    connections: list[GraphConnection]
