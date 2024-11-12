import os
from loguru import logger as loguru_logger
from src.config.settings import Settings


def setup_logger():
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)

    loguru_logger.remove()
    loguru_logger.add(
        "logs/app.log",
        rotation="1 week",
        retention="4 weeks",
        level=Settings.LOGGING_LEVEL,
        enqueue=True,
    )
    loguru_logger.add(
        "stdout",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
        enqueue=True,
    )
    return loguru_logger


logger = setup_logger()
