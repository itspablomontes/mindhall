from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infra.config import get_settings
from src.lifespan import lifespan


def create_app() -> FastAPI:

    settings = get_settings()

    app = FastAPI(
        title="TeachMeWoW Agent API",
        description="AI coaching agent for World of Warcraft",
        version="0.1.0",
        lifespan=lifespan,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routers here

    # app.include_router(router)

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
