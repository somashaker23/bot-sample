# ============================================================================
# bot/channels/internal_channel.py
# ============================================================================
"""Internal/console channel for testing."""

from typing import Any, Dict
from bot.core.base_channel import BaseChannel


class InternalChannel(BaseChannel):
    """
    Internal console channel for testing and demo.

    Prints messages to console and reads from stdin.
    """

    @property
    def name(self) -> str:
        """Return channel name."""
        return "internal"

    def send_message(self, recipient_id: str, message: str) -> None:
        """
        Send message to console.

        Args:
            recipient_id: User identifier
            message: Message text
        """
        print(f"[Bot] → {message}")

    def receive_message(self, payload: Any) -> Dict[str, str]:
        """
        Process console input.

        Args:
            payload: Text input or dict

        Returns:
            Normalized message dict
        """
        if isinstance(payload, dict):
            return payload
        return {
            "user_id": "console_user",
            "text": str(payload)
        }

