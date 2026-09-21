"""
Asynchronous Helper Utilities.
"""

import asyncio
from typing import Coroutine, Any

def run_async_safe(coro: Coroutine) -> Any:
    """Runs a coroutine safely regardless of whether an event loop is active."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        # Schedule in existing running loop or background task
        return asyncio.create_task(coro)
    else:
        return loop.run_until_complete(coro)
