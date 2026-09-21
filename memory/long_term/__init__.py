"""
Long-term semantic vector stores, structured knowledge bases, and user profiles.
"""

from .vector_store import VectorStore
from .knowledge_base import KnowledgeBase
from .user_profiles import UserProfiles

__all__ = ["VectorStore", "KnowledgeBase", "UserProfiles"]
