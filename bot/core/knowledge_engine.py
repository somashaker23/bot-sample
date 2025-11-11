# ============================================================================
# bot/core/knowledge_engine.py
# ============================================================================
"""Knowledge Engine for storing and retrieving facts."""

from typing import Dict, Optional


class KnowledgeEngine:
    """
    Manages a simple key-value knowledge base with fuzzy matching support.

    Features:
    - Case-insensitive storage and retrieval
    - Fuzzy matching for similar keys
    - Friendly fallback messages
    """

    def __init__(self):
        """Initialize empty knowledge base."""
        self.knowledge: Dict[str, str] = {}

    def add_knowledge(self, key: str, value: str) -> None:
        """
        Store a fact in the knowledge base.

        Args:
            key: Knowledge key (case-insensitive)
            value: Associated value
        """
        normalized_key = key.lower().strip()
        self.knowledge[normalized_key] = value.strip()

    def query(self, question: str) -> str:
        """
        Query the knowledge base.

        Args:
            question: Question or key to look up

        Returns:
            Answer string or friendly fallback message
        """
        # Normalize the question
        normalized = question.lower().strip()

        # Direct match
        if normalized in self.knowledge:
            return self.knowledge[normalized]

        # Fuzzy match - check if question contains any key
        for key, value in self.knowledge.items():
            if key in normalized or normalized in key:
                return value

        # No match found
        return "I don't know that yet. Try teaching me!"

    def get(self, key: str) -> Optional[str]:
        """
        Direct key lookup (case-insensitive).

        Args:
            key: Knowledge key

        Returns:
            Value if found, None otherwise
        """
        return self.knowledge.get(key.lower().strip())

    def list_knowledge(self) -> Dict[str, str]:
        """Return all stored knowledge."""
        return self.knowledge.copy()

