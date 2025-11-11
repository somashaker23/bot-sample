
# ============================================================================
# bot/channels/telegram_channel.py
# ============================================================================
"""Telegram channel implementation."""

from typing import Any, Dict
from bot.core.base_channel import BaseChannel


class TelegramChannel(BaseChannel):
    """
    Telegram messaging channel (mocked implementation).

    In production, this would use python-telegram-bot library.
    """

    def __init__(self, api_token: str):
        """
        Initialize Telegram channel.

        Args:
            api_token: Telegram Bot API token
        """
        self.api_token = api_token

    @property
    def name(self) -> str:
        """Return channel name."""
        return "telegram"

    def send_message(self, recipient_id: str, message: str) -> None:
        """
        Send message via Telegram (mocked).

        Args:
            recipient_id: Telegram chat ID
            message: Message text
        """
        print(f"[Telegram] → {recipient_id}: {message}")

    def receive_message(self, payload: Any) -> Dict[str, str]:
        """
        Process Telegram webhook payload.

        Args:
            payload: Telegram update object

        Returns:
            Normalized message dict
        """
        # Mock implementation
        if isinstance(payload, dict):
            return {
                "user_id": payload.get("from_id", "unknown"),
                "text": payload.get("text", "")
            }
        return {"user_id": "unknown", "text": str(payload)}


