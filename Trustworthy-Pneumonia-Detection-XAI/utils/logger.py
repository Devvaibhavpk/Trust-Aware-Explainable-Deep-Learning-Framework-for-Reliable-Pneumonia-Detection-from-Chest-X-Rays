"""
Simple logging configuration for training and evaluation scripts.
"""

import logging
import sys
from pathlib import Path

from configs.config import LOGS_DIR


def get_logger(name: str, log_file: str | None = None) -> logging.Logger:
    """
    Create a logger with console and optional file handlers.

    Args:
        name: Logger name (typically __name__).
        log_file: Optional filename under outputs/logs/.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(LOGS_DIR / log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
