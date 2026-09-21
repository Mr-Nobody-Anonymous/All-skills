"""
All-Skills Model Management Subsystem.
Orchestrates downloading, caching, lazy loading, and registry of local and remote AI models.
"""

from .model_manager import ModelManager
from .model_registry import ModelRegistry

__all__ = ["ModelManager", "ModelRegistry"]
