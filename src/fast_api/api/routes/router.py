from fastapi import APIRouter

from fast_api.api.routes import healthcheck, predict

router = APIRouter()

router.include_router(predict.router, tags=["predict"])
router.include_router(healthcheck.router, tags=["healthcheck"])
