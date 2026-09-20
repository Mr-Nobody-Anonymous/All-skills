"""
Core API Gateway and Client Manager.
Provides centralized routing and client reuse for third-party API invocations.
"""

from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class ApiManager:
    """Manages external service connections and API credentials."""

    def __init__(self):
        self._clients: Dict[str, Any] = {}
        self._endpoints: Dict[str, str] = {}

    def register_client(self, service_name: str, client_instance: Any) -> None:
        """Register an active service client."""
        self._clients[service_name] = client_instance

    def get_client(self, service_name: str) -> Optional[Any]:
        """Retrieve client instance."""
        return self._clients.get(service_name)

    def register_endpoint(self, service_name: str, url: str) -> None:
        """Register base URL for service."""
        self._endpoints[service_name] = url

    def get_endpoint(self, service_name: str) -> Optional[str]:
        return self._endpoints.get(service_name)
