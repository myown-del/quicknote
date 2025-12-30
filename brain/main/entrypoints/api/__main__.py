import uvicorn

from brain.config.models import Config
from brain.config.parser import load_config

config = load_config(
    config_class=Config,
    env_file_path=".env",
)

if __name__ == "__main__":
    uvicorn.run(
        app="brain.main.entrypoints.api.factory:create_app",
        host=config.api.internal_host,
        port=config.api.port,
        reload=config.api.auto_reload,
        factory=True,
        access_log=False,
        workers=config.api.workers,
    )
