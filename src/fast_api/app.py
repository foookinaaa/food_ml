from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from fast_api.api.routes.router import router as api_router


def get_app() -> FastAPI:
    """
    FastAPI app initialization.
    """
    fastapi_app = FastAPI(
        title="Tree health classification service",
        version="0.1.0",
        debug=False,
        description="ML service for predicting health of trees",
    )
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @fastapi_app.get("/")
    async def read_root():
        return {"message": "Welcome to the Tree Health Classification Service"}

    fastapi_app.include_router(api_router, prefix="/api")
    logger.info("FastAPI application has been initialized")
    return fastapi_app


app = get_app()
