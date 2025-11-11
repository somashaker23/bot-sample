# ============================================================================
# bot/core/base_action.py
# ============================================================================
"""Base class for all bot actions/skills."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAction(ABC):
    """
    Abstract base class for bot actions (skills).

    All skills must implement can_handle() and execute().
    """

    @abstractmethod
    def can_handle(self, intent: str) -> bool:
        """
        Check if this action can handle the given intent.

        Args:
            intent: Intent string to check

        Returns:
            True if this action handles the intent
        """
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> str:
        """
        Execute the action with given parameters.

        Args:
            params: Dictionary of extracted entities and parameters

        Returns:
            Response string to send to user
        """
        pass

    @abstractmethod
    def required_entities(self) -> List[str]:
        """
        Return list of required entity names for this action.

        Returns:
            List of required entity names
        """
        pass

