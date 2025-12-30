from neo4j import AsyncGraphDatabase, AsyncDriver

from quicknote.application.abstractions.config.models import INeo4jConfig


def create_driver(config: INeo4jConfig) -> AsyncDriver:
    return AsyncGraphDatabase.driver(
        config.uri,
        auth=(config.user, config.password),
    )
