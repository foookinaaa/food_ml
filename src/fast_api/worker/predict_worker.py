from loguru import logger

from fast_api.schemas.requests import FeatureRequest
from fast_api.services.model import TreeHealthClassifier
from src.fast_api.connections.broker import celery_app


@celery_app.task(name="predict")
def predict_health(features: FeatureRequest):
    """
    Predict health of tree

    """
    try:
        result = TreeHealthClassifier.predict(features)
        return result
    except Exception as ex:
        logger.exception(ex)
        return None
