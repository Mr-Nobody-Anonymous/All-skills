"""
Centralized Logger for the Core Engine.
Thin wrapper that delegates to utils.logger.
"""
from utils.logger import get_logger, setup_logging

__all__ = ["get_logger", "setup_logging"]
