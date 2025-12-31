from dataclasses import asdict

from brain.domain.entities.graph import GraphData, GraphNode, GraphConnection
from brain.presentation.api.routes.graph.models import (
    GraphSchema,
    GraphNodeSchema,
    GraphConnectionSchema,
)


def map_graph_node_to_schema(node: GraphNode) -> GraphNodeSchema:
    return GraphNodeSchema.model_validate(asdict(node))


def map_graph_connection_to_schema(
    connection: GraphConnection,
) -> GraphConnectionSchema:
    return GraphConnectionSchema.model_validate(asdict(connection))


def map_graph_to_schema(graph: GraphData) -> GraphSchema:
    return GraphSchema(
        nodes=[map_graph_node_to_schema(node) for node in graph.nodes],
        connections=[
            map_graph_connection_to_schema(connection)
            for connection in graph.connections
        ],
    )
