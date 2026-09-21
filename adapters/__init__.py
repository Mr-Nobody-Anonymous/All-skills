"""
All-Skills Input and Output Adapters Subsystem.
Transforms raw input signals (text, audio, vision, sensor) into normalized pipelines,
and formats multimodal execution outputs (speech, visual charts, system actions).
"""

from .input_adapters.text_input import TextInputAdapter
from .input_adapters.voice_input import VoiceInputAdapter
from .input_adapters.image_input import ImageInputAdapter
from .input_adapters.multimodal_input import MultimodalInputAdapter

from .output_adapters.text_output import TextOutputAdapter
from .output_adapters.voice_output import VoiceOutputAdapter
from .output_adapters.visual_output import VisualOutputAdapter
from .output_adapters.action_output import ActionOutputAdapter

__all__ = [
    "TextInputAdapter",
    "VoiceInputAdapter",
    "ImageInputAdapter",
    "MultimodalInputAdapter",
    "TextOutputAdapter",
    "VoiceOutputAdapter",
    "VisualOutputAdapter",
    "ActionOutputAdapter",
]
