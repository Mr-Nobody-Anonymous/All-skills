"""
All-Skills Multi-Modal Interfaces Subsystem.
Provides CLI, Voice, Web, REST API, Desktop GUI, and Chat widget interfaces.
"""

from .cli.terminal_interface import TerminalInterface
from .voice.voice_interface import VoiceInterface
from .web.web_interface import WebInterface
from .api.rest_api import RestApi
from .gui.desktop_gui import DesktopGui
from .chat.chat_interface import ChatInterface

__all__ = [
    "TerminalInterface",
    "VoiceInterface",
    "WebInterface",
    "RestApi",
    "DesktopGui",
    "ChatInterface",
]
