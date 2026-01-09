import logging
import sys
from pythonjsonlogger import jsonlogger

from pomodoro_quest.core.config import settings


def configure_logging() -> None:
    """
    Configure structured JSON logging.

    This makes logs easier to search and parse in CloudWatch later.
    """
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    # Replace handlers to avoid duplicate logs in reload scenarios.
    logger.handlers = [handler]
