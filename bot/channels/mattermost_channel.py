# ============================================================================
# bot/channels/mattermost_channel.py
# ============================================================================
"""Mattermost channel implementation."""

from typing import Any, Dict
from bot.core.base_channel import BaseChannel


class MattermostChannel(BaseChannel):
    """
    Mattermost messaging channel (mocked implementation).

    In production, this would use mattermostdriver library.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize Mattermost channel.

        Args:
            webhook_url: Mattermost incoming webhook URL
        """
        self.webhook_url = webhook_url

    @property
    def name(self) -> str:
        """Return channel name."""
        return "mattermost"

    def send_message(self, recipient_id: str, message: str) -> None:
        """
        Send message via Mattermost (mocked).

        Args:
            recipient_id: Mattermost channel or user ID
            message: Message text
        """
        print(f"[Mattermost] → {recipient_id}: {message}")

    def receive_message(self, payload: Any) -> Dict[str, str]:
        """
        Process Mattermost webhook payload.

        Args:
            payload: Mattermost post object

        Returns:
            Normalized message dict
        """
        if isinstance(payload, dict):
            return {
                "user_id": payload.get("user_id", "unknown"),
                "text": payload.get("text", "")
            }
        return {"user_id": "unknown", "text": str(payload)}

