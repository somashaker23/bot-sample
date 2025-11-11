# ============================================================================
# bot/core/intent_engine.py
# ============================================================================
"""Intent detection and entity extraction engine."""

import re
from typing import Dict, List, Optional, Tuple


class IntentEngine:
    """
    Detects intents from text and extracts entities.

    Supports:
    - Fuzzy intent matching
    - Regex-based entity extraction
    - Missing entity identification
    - Natural language prompts for missing info
    """

    def __init__(self):
        """Initialize intent patterns and entity extractors."""
        self.intent_patterns = {
            "get_weather": [
                r"\b(weather|temperature|forecast)\b",
                r"\bhow'?s?\s+it\s+outside\b",
                r"\bwhat'?s?\s+the\s+weather\b"
            ],
            "learn_knowledge": [
                r"\blearn\b",
                r"\bteach\b",
                r"\bremember\b",
                r"\b[\w_]+\s*=\s*.+\b"
            ],
            "ask_knowledge": [
                r"\bwhat\s+is\b",
                r"\btell\s+me\s+about\b",
                r"\bdo\s+you\s+know\b",
                r"\bwhat'?s\b"
            ]
        }

    def detect_intent(self, text: str) -> Optional[str]:
        """
        Detect intent from text using pattern matching.

        Args:
            text: User input text

        Returns:
            Detected intent string or None
        """
        text_lower = text.lower().strip()

        if not text_lower:
            return None

        # Check for learn pattern first (has = sign)
        if "=" in text_lower:
            return "learn_knowledge"

        # Check other patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent

        return None

    def extract_entities(self, text: str, intent: str) -> Dict[str, str]:
        """
        Extract entities based on intent.

        Args:
            text: User input text
            intent: Detected intent

        Returns:
            Dictionary of extracted entities
        """
        entities = {}

        if intent == "get_weather":
            entities["location"] = self._extract_location(text)

        elif intent == "learn_knowledge":
            key, value = self._extract_key_value(text)
            if key:
                entities["key"] = key
            if value:
                entities["value"] = value

        elif intent == "ask_knowledge":
            entities["key"] = self._extract_question_key(text)

        return entities

    def _extract_location(self, text: str) -> Optional[str]:
        """Extract location from weather query."""
        # Look for "in <location>" pattern
        match = re.search(r"\bin\s+([A-Za-z\s]+?)(?:\s+\?|$|\.|,)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Look for city names (simple pattern)
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ["weather", "forecast", "temperature"]:
                if i + 1 < len(words):
                    # Take next word(s) as location
                    location_parts = []
                    for j in range(i + 1, min(i + 4, len(words))):
                        if words[j][0].isupper() or j == i + 1:
                            location_parts.append(words[j].strip("?.,!"))
                        else:
                            break
                    if location_parts:
                        return " ".join(location_parts)

        return None

    def _extract_key_value(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract key-value pair from learn command."""
        # Pattern: "learn key = value" or "key = value"
        match = re.search(r"(?:learn\s+)?([a-z_]\w*)\s*=\s*(.+?)(?:\s*$|\.|\?)", text, re.IGNORECASE)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            return key, value

        return None, None

    def _extract_question_key(self, text: str) -> Optional[str]:
        """Extract key from question."""
        # Remove common question words
        cleaned = re.sub(r"\b(what|is|the|tell|me|about|do|you|know)\b", "", text, flags=re.IGNORECASE)
        cleaned = re.sub(r"[?.,!]", "", cleaned).strip()

        if cleaned:
            return cleaned.lower().replace(" ", "_")

        return None

    def get_missing_entities(self, required: List[str], extracted: Dict[str, str]) -> List[str]:
        """
        Identify missing required entities.

        Args:
            required: List of required entity names
            extracted: Dictionary of extracted entities

        Returns:
            List of missing entity names
        """
        missing = []
        for entity in required:
            if entity not in extracted or not extracted[entity]:
                missing.append(entity)
        return missing

    def prompt_for_entity(self, entity_name: str) -> str:
        """
        Generate natural language prompt for missing entity.

        Args:
            entity_name: Name of missing entity

        Returns:
            Natural language prompt string
        """
        prompts = {
            "location": "Can you please tell me the location?",
            "key": "What would you like me to learn?",
            "value": "What's the value for that?",
        }

        return prompts.get(entity_name, f"Can you please tell me the {entity_name}?")

