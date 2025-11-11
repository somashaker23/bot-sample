
# ============================================================================
# bot/skills/weather.py
# ============================================================================
"""Weather skill implementation."""

from typing import Any, Dict, List
import random
from bot.core.base_action import BaseAction


class WeatherAction(BaseAction):
    """
    Provides weather information (simulated).

    Intent: get_weather
    Required entities: location
    """

    def can_handle(self, intent: str) -> bool:
        """Handle get_weather intent."""
        return intent == "get_weather"

    def required_entities(self) -> List[str]:
        """Require location entity."""
        return ["location"]

    def execute(self, params: Dict[str, Any]) -> str:
        """
        Execute weather query.

        Args:
            params: Must contain 'location' key

        Returns:
            Simulated weather response
        """
        location = params.get("location", "unknown")

        # Simulate weather conditions
        conditions = ["sunny ☀️", "cloudy ☁️", "rainy 🌧️", "snowy ❄️", "partly cloudy ⛅"]
        temp = random.randint(15, 30)
        condition = random.choice(conditions)

        return f"The weather in {location} is {condition} with a temperature of {temp}°C."
