"""
Desktop Graphical User Interface Model.
Coordinates system tray indicators, desktop windows, notifications, and graphical settings.
"""

from typing import Dict, Any, Optional
from core.pipeline import Pipeline

class DesktopGui:
    def __init__(self, pipeline: Optional[Pipeline] = None):
        self.pipeline = pipeline or Pipeline()
        self.window_state = {"visible": False, "theme": "dark"}

    def show(self):
        self.window_state["visible"] = True
        return "GUI window displayed."

    def hide(self):
        self.window_state["visible"] = False
        return "GUI window minimized."

    def submit_user_input(self, text: str) -> Dict[str, Any]:
        return self.pipeline.process(text)
