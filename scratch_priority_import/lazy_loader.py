"""
Lazy Loader for All-Skills.
Defers loading of non-essential (Tier 5 Low & Tier 6 Lazy) skills until first invocation,
drastically reducing startup latency and resident memory footprint.
"""

from typing import Dict, Any, Callable, Optional, Set
import importlib
import logging
import threading

logger = logging.getLogger(__name__)


class LazySkillProxy:
    """Proxy object that wraps a skill and loads the underlying implementation on demand."""

    def __init__(self, skill_name: str, loader_callable: Callable[[], Any]):
        self._skill_name = skill_name
        self._loader_callable = loader_callable
        self._instance: Optional[Any] = None
        self._is_loaded = False
        self._lock = threading.Lock()

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def get_instance(self) -> Any:
        """Resolve and instantiate underlying skill instance."""
        if not self._is_loaded:
            with self._lock:
                if not self._is_loaded:
                    logger.info(f"Lazy loading skill on first access: {self._skill_name}")
                    self._instance = self._loader_callable()
                    self._is_loaded = True
        return self._instance

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute/method calls to underlying instance."""
        instance = self.get_instance()
        return getattr(instance, name)

    def __getitem__(self, key: Any) -> Any:
        """Delegate item access to underlying instance."""
        instance = self.get_instance()
        return instance[key]



class LazyLoaderManager:
    """Coordinates deferred loading registry across all domains."""

    def __init__(self):
        self._proxies: Dict[str, LazySkillProxy] = {}
        self._lazy_registered: Set[str] = set()

    def register_lazy(self, skill_name: str, loader_fn: Callable[[], Any]) -> LazySkillProxy:
        """Register a lazy proxy for a skill."""
        proxy = LazySkillProxy(skill_name, loader_fn)
        self._proxies[skill_name] = proxy
        self._lazy_registered.add(skill_name)
        return proxy

    def get(self, skill_name: str) -> Optional[Any]:
        """Access skill, instantiating if deferred."""
        proxy = self._proxies.get(skill_name)
        if proxy:
            return proxy.get_instance()
        return None

    def is_lazy(self, skill_name: str) -> bool:
        """Check if skill is registered as deferred."""
        return skill_name in self._lazy_registered

    def is_instantiated(self, skill_name: str) -> bool:
        """Check if lazy skill has already been loaded into memory."""
        proxy = self._proxies.get(skill_name)
        return proxy.is_loaded if proxy else False

    def unload(self, skill_name: str) -> bool:
        """Unload instantiated skill instance to free memory."""
        proxy = self._proxies.get(skill_name)
        if proxy and proxy.is_loaded:
            with proxy._lock:
                proxy._instance = None
                proxy._is_loaded = False
                logger.info(f"Unloaded lazy skill from memory: {skill_name}")
                return True
        return False
