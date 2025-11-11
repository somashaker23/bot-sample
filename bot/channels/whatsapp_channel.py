
# ============================================================================
# bot/channels/whatsapp_channel.py
# ============================================================================
"""WhatsApp channel implementation."""

from typing import Any, Dict
from bot.core.base_channel import BaseChannel


class WhatsAppChannel(BaseChannel):
    """
    WhatsApp messaging channel (mocked implementation).

    In production, this would use Twilio or WhatsApp Business API.
    """

    def __init__(self, api_key: str):
        """
        Initialize WhatsApp channel.

        Args:
            api_key: WhatsApp API key
        """
        self.api_key = api_key

    @property
    def name(self) -> str:
        """Return channel name."""
        return "whatsapp"

    def send_message(self, recipient_id: str, message: str) -> None:
        """
        Send message via WhatsApp (mocked).

        Args:
            recipient_id: WhatsApp phone number
            message: Message text
        """
        print(f"[WhatsApp] → {recipient_id}: {message}")

    def receive_message(self, payload: Any) -> Dict[str, str]:
        """
        Process WhatsApp webhook payload.

        Args:
            payload: WhatsApp message object

        Returns:
            Normalized message dict
        """
        if isinstance(payload, dict):
            return {
                "user_id": payload.get("phone", "unknown"),
                "text": payload.get("message", "")
            }
        return {"user_id": "unknown", "text": str(payload)}
