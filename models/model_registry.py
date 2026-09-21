"""
Model Registry for All-Skills Platform.
Tracks available model families (STT, TTS, LLM, Vision, Embeddings, Classifiers)
and their hardware/runtime requirements.
"""

from typing import Dict, Any, List, Optional

class ModelRegistry:
    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {}
        self._register_defaults()

    def _register_defaults(self):
        defaults = [
            {"id": "whisper-base", "task": "stt", "engine": "whisper", "size_mb": 140, "requires_gpu": False},
            {"id": "piper-en-lessac", "task": "tts", "engine": "piper", "size_mb": 65, "requires_gpu": False},
            {"id": "silero-vad", "task": "vad", "engine": "silero", "size_mb": 2, "requires_gpu": False},
            {"id": "yolov8n", "task": "vision_detection", "engine": "ultralytics", "size_mb": 6, "requires_gpu": False},
            {"id": "all-MiniLM-L6-v2", "task": "embeddings", "engine": "sentence-transformers", "size_mb": 90, "requires_gpu": False},
            {"id": "vader-sentiment", "task": "sentiment", "engine": "vader", "size_mb": 1, "requires_gpu": False},
        ]
        for d in defaults:
            self.register(d["id"], d)

    def register(self, model_id: str, metadata: Dict[str, Any]):
        self._models[model_id] = metadata

    def get(self, model_id: str) -> Optional[Dict[str, Any]]:
        return self._models.get(model_id)

    def list_models(self, task: Optional[str] = None) -> List[Dict[str, Any]]:
        models = list(self._models.values())
        if task:
            models = [m for m in models if m.get("task") == task]
        return models
