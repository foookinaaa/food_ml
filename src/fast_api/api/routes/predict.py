from typing import Dict

from fastapi import APIRouter, BackgroundTasks

from fast_api.connections.broker import celery_app
from fast_api.schemas.requests import FeatureRequest
from src.fast_api.services.utils import print_logger_info

router = APIRouter()


@router.post("/predict/")
async def predict(
    feature_request: FeatureRequest, background_tasks: BackgroundTasks
) -> Dict:
    """
    Predict health of tree

    Args:
        feature_request (TextRequest): Features with values

    Returns:
        dict: predictions as dict
    """
    async_result = celery_app.send_task("predict", args=[feature_request.dict()])
    result = async_result.get()

    background_tasks.add_task(
        print_logger_info,
        feature_request.dict(),
        result,
    )
    return result
