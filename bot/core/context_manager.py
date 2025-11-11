# ============================================================================
# bot/core/context_manager.py
# ============================================================================
"""Manages conversation context for multi-turn dialogs."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta


class ConversationContext:
    """Holds context for a single conversation."""

    def __init__(self, user_id: str, intent: str, entities: Dict[str, str], missing: List[str]):
        self.user_id = user_id
        self.intent = intent
        self.entities = entities
        self.missing_entities = missing
        self.timestamp = datetime.now()

    def is_expired(self, timeout_minutes: int = 5) -> bool:
        """Check if context has expired."""
        return datetime.now() - self.timestamp > timedelta(minutes=timeout_minutes)


class ContextManager:
    """
    Manages conversation contexts for all users.

    Features:
    - Per-user context isolation
    - Pending intent tracking
    - Missing entity management
    - Context timeout handling
    """

    def __init__(self, timeout_minutes: int = 5):
        """
        Initialize context manager.

        Args:
            timeout_minutes: Minutes before context expires
        """
        self.contexts: Dict[str, ConversationContext] = {}
        self.timeout_minutes = timeout_minutes

    def set_pending(self, user_id: str, intent: str, entities: Dict[str, str], missing: List[str]) -> None:
        """
        Store pending conversation context.

        Args:
            user_id: User identifier
            intent: Detected intent
            entities: Already extracted entities
            missing: List of missing entity names
        """
        self.contexts[user_id] = ConversationContext(user_id, intent, entities, missing)

    def get_pending(self, user_id: str) -> Optional[ConversationContext]:
        """
        Retrieve pending context for user.

        Args:
            user_id: User identifier

        Returns:
            ConversationContext if exists and not expired, None otherwise
        """
        if user_id not in self.contexts:
            return None

        context = self.contexts[user_id]

        if context.is_expired(self.timeout_minutes):
            self.clear(user_id)
            return None

        return context

    def update_entities(self, user_id: str, new_entities: Dict[str, str]) -> None:
        """
        Update entities for pending context.

        Args:
            user_id: User identifier
            new_entities: New entities to merge
        """
        if user_id in self.contexts:
            self.contexts[user_id].entities.update(new_entities)
            # Remove filled entities from missing list
            self.contexts[user_id].missing_entities = [
                e for e in self.contexts[user_id].missing_entities
                if e not in new_entities or not new_entities[e]
            ]

    def clear(self, user_id: str) -> None:
        """
        Clear context for user.

        Args:
            user_id: User identifier
        """
        if user_id in self.contexts:
            del self.contexts[user_id]

    def cleanup_expired(self) -> int:
        """
        Remove all expired contexts.

        Returns:
            Number of contexts cleaned up
        """
        expired_users = [
            user_id for user_id, ctx in self.contexts.items()
            if ctx.is_expired(self.timeout_minutes)
        ]

        for user_id in expired_users:
            del self.contexts[user_id]

        return len(expired_users)
