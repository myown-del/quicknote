from pydantic.v1 import BaseSettings


class API(BaseSettings):
    workers: int = 1
    host: str
    port: int


class Config(BaseSettings):
    api: API

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
