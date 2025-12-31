from pydantic import BaseModel


class GraphNodeSchema(BaseModel):
    id: str
    title: str
    has_keyword_note: bool
    kind: str


class GraphConnectionSchema(BaseModel):
    from_id: str
    to_id: str
    kind: str


class GraphSchema(BaseModel):
    nodes: list[GraphNodeSchema]
    connections: list[GraphConnectionSchema]
