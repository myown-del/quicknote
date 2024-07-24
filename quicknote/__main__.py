import uvicorn

from quicknote.config import load_config

config = load_config()

if __name__ == "__main__":
    uvicorn.run(
        app="quicknote.app:create_app",
        host=config.api.internal_host,
        port=config.api.port,
        reload=config.api.auto_reload,
        factory=True,
        access_log=False,
        workers=config.api.workers,
    )
