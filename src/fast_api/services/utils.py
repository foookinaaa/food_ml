from datetime import datetime
from typing import Any, Dict

from loguru import logger


async def print_logger_info(input_features: Dict[str, Any], predicted):
    """
    print_logger_info - printing logger.
    """
    logger.info({"input": input_features, "predicted": predicted})


def return_current_time():
    """
    Example func, return current time.
    """
    return datetime.utcnow().isoformat()
