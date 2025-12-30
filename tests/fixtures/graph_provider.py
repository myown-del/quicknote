import os

from dishka import Provider, Scope, provide

from quicknote.application.abstractions.config.models import INeo4jConfig
from quicknote.application.abstractions.repositories.notes_graph import INotesGraphRepository
from quicknote.config.models import Config
from tests.mocks.config import Neo4jConfig
from tests.mocks.notes_graph_repo import DummyNotesGraphRepository


class TestGraphProvider(Provider):
    scope = Scope.APP

    @provide(provides=INotesGraphRepository)
    def get_notes_graph_repo(self) -> DummyNotesGraphRepository:
        return DummyNotesGraphRepository()


class TestNeo4jConfigProvider(Provider):
    scope = Scope.APP

    @provide(provides=INeo4jConfig)
    def get_neo4j_config(self, config: Config) -> Neo4jConfig:
        from testcontainers.neo4j import Neo4jContainer

        neo4j = Neo4jContainer("neo4j:5")
        if os.name == "nt":
            neo4j.get_container_host_ip = lambda: "localhost"
        try:
            neo4j.start()
            if hasattr(neo4j, "get_connection_url"):
                uri = neo4j.get_connection_url()
            else:
                host = neo4j.get_container_host_ip()
                port = neo4j.get_exposed_port(7687)
                uri = f"bolt://{host}:{port}"

            password = "neo4j"
            if hasattr(neo4j, "get_admin_password"):
                password = neo4j.get_admin_password()
            elif hasattr(neo4j, "password"):
                password = neo4j.password

            user = getattr(neo4j, "username", None) or "neo4j"

            neo4j_config = Neo4jConfig(
                uri=uri,
                user=user,
                password=password,
                database="neo4j",
            )
            config.neo4j = neo4j_config
            yield neo4j_config
        finally:
            neo4j.stop()
