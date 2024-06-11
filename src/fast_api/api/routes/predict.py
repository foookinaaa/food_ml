from typing import Dict

from fastapi import APIRouter, BackgroundTasks

from fast_api.schemas.requests import FeatureRequest
from fast_api.services.model import TreeHealthClassifier
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
    result = TreeHealthClassifier.predict(feature_request)
    background_tasks.add_task(
        print_logger_info,
        feature_request.dict(),
        result,
    )
    return result
