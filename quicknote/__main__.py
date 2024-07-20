import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        app="quicknote.app:create_app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        factory=True,
        access_log=False,
        workers=1
    )
