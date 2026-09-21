"""
Centralized Logging Utility.
"""

import logging
import sys
from typing import Optional

def setup_logger(name: str = "all_skills", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

def get_logger(name: str = "all_skills") -> logging.Logger:
    return logging.getLogger(name)
