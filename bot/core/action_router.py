# ============================================================================
# bot/core/action_router.py
# ============================================================================
"""Routes intents to appropriate skill handlers."""

from typing import Any, Dict, List
from .base_action import BaseAction


class ActionRouter:
    """
    Manages registered actions and routes intents to appropriate handlers.

    Features:
    - Action registration
    - Intent-to-action routing
    - Graceful fallback for unhandled intents
    """

    def __init__(self):
        """Initialize with empty action list."""
        self.actions: List[BaseAction] = []

    def register(self, action: BaseAction) -> None:
        """
        Register a new action/skill.

        Args:
            action: Action instance to register
        """
        self.actions.append(action)

    def route(self, intent: str, params: Dict[str, Any]) -> str:
        """
        Route intent to appropriate action handler.

        Args:
            intent: Detected intent string
            params: Extracted entities and parameters

        Returns:
            Response string from action or fallback message
        """
        for action in self.actions:
            if action.can_handle(intent):
                try:
                    return action.execute(params)
                except Exception as e:
                    return f"Sorry, an error occurred: {str(e)}"

        return f"Sorry, I don't have an action for '{intent}'."

    def get_required_entities(self, intent: str) -> List[str]:
        """
        Get required entities for an intent.

        Args:
            intent: Intent string

        Returns:
            List of required entity names
        """
        for action in self.actions:
            if action.can_handle(intent):
                return action.required_entities()
        return []

