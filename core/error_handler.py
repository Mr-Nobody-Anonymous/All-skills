"""
Core Error Handler.
Centralized exception containment and error dialogue generator.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Catches, logs, and transforms skill exceptions into graceful conversational responses."""

    @staticmethod
    def handle_skill_error(skill_name: str, error: Exception) -> str:
        """Log error and return polite spoken notification."""
        logger.error(f"Skill '{skill_name}' encountered an error: {error}", exc_info=True)
        return f"I had trouble processing that request with {skill_name}. Please try again later."

    @staticmethod
    def format_error_response(skill_name: str, code: str, message: str) -> Dict[str, Any]:
        return {
            "success": False,
            "skill": skill_name,
            "error_code": code,
            "message": message
        }

    def handle(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.error(f"Pipeline error: {error}", exc_info=True)
        return {
            "success": False,
            "error": str(error),
            "context": context or {},
            "message": "Encountered an internal error while processing request."
        }
