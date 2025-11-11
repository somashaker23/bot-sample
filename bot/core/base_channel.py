# ============================================================================
# bot/core/base_channel.py
# ============================================================================
"""Base class for all communication channels."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseChannel(ABC):
    """
    Abstract base class for all messaging channels.

    All channels must implement name, send_message, and receive_message.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return channel name."""
        pass

    @abstractmethod
    def send_message(self, recipient_id: str, message: str) -> None:
        """
        Send message to recipient.

        Args:
            recipient_id: Recipient identifier
            message: Message text to send
        """
        pass

    @abstractmethod
    def receive_message(self, payload: Any) -> Dict[str, str]:
        """
        Process incoming message payload.

        Args:
            payload: Raw message payload from channel

        Returns:
            Normalized message dict with 'user_id' and 'text' keys
        """
        pass
