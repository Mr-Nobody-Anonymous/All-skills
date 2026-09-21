"""
Model Manager for All-Skills Platform.
Manages lazy model downloading, local caching, and lifecycle unloading to conserve RAM/VRAM.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from .model_registry import ModelRegistry

class ModelManager:
    def __init__(self, cache_dir: Optional[Path] = None, registry: Optional[ModelRegistry] = None):
        self.cache_dir = cache_dir or (Path(__file__).resolve().parent / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.registry = registry or ModelRegistry()
        self.loaded_instances: Dict[str, Any] = {}

    def is_cached(self, model_id: str) -> bool:
        model_path = self.cache_dir / model_id
        return model_path.exists()

    def get_or_load(self, model_id: str) -> Any:
        """Lazy loads model instance, caching in-memory."""
        if model_id in self.loaded_instances:
            return self.loaded_instances[model_id]

        meta = self.registry.get(model_id) or {"id": model_id, "task": "custom"}
        # Mock instance container for zero-dependency lazy initialization
        instance = {
            "model_id": model_id,
            "metadata": meta,
            "status": "ready",
            "cache_path": str(self.cache_dir / model_id)
        }
        self.loaded_instances[model_id] = instance
        return instance

    def unload(self, model_id: str):
        if model_id in self.loaded_instances:
            del self.loaded_instances[model_id]
