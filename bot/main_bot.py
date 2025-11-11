# ============================================================================
# bot/main_bot.py
# ============================================================================
"""Main bot orchestrator."""

import json
from pathlib import Path
from typing import Dict, Optional
from bot.core.knowledge_engine import KnowledgeEngine
from bot.core.intent_engine import IntentEngine
from bot.core.action_router import ActionRouter
from bot.core.context_manager import ContextManager
from bot.core.base_channel import BaseChannel
from bot.skills.weather import WeatherAction
from bot.channels.telegram_channel import TelegramChannel
from bot.channels.whatsapp_channel import WhatsAppChannel
from bot.channels.mattermost_channel import MattermostChannel
from bot.channels.internal_channel import InternalChannel


class MainBot:
    """
    Main bot orchestrator.

    Responsibilities:
    - Initialize all engines and channels
    - Route incoming messages to correct logic
    - Handle multi-turn conversations
    - Manage context and state
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the bot.

        Args:
            config_path: Path to channels.json config file
        """
        # Initialize core engines
        self.knowledge = KnowledgeEngine()
        self.intent_engine = IntentEngine()
        self.action_router = ActionRouter()
        self.context_manager = ContextManager()

        # Register skills
        self._register_skills()

        # Initialize channels
        self.channels: Dict[str, BaseChannel] = {}
        if config_path:
            self._load_channels(config_path)
        else:
            # Default: only internal channel
            self.channels["internal"] = InternalChannel()

        print("🤖 Bot initialized successfully!")

    def _register_skills(self) -> None:
        """Register all available skills."""
        self.action_router.register(WeatherAction())
        print("✓ Registered skills: Weather")

    def _load_channels(self, config_path: str) -> None:
        """
        Load channels from config file.

        Args:
            config_path: Path to channels.json
        """
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            if "telegram" in config:
                self.channels["telegram"] = TelegramChannel(config["telegram"]["api_token"])

            if "whatsapp" in config:
                self.channels["whatsapp"] = WhatsAppChannel(config["whatsapp"]["api_key"])

            if "mattermost" in config:
                self.channels["mattermost"] = MattermostChannel(config["mattermost"]["webhook_url"])

            # Always include internal channel
            self.channels["internal"] = InternalChannel()

            print(f"✓ Loaded channels: {', '.join(self.channels.keys())}")

        except FileNotFoundError:
            print(f"⚠ Config file not found: {config_path}, using internal channel only")
            self.channels["internal"] = InternalChannel()
        except Exception as e:
            print(f"⚠ Error loading config: {e}, using internal channel only")
            self.channels["internal"] = InternalChannel()

    def process_message(self, user_id: str, text: str, channel: str = "internal") -> str:
        """
        Process incoming message and generate response.

        Args:
            user_id: User identifier
            text: Message text
            channel: Channel name

        Returns:
            Response string
        """
        # Handle empty messages
        if not text or not text.strip():
            return "Could you please say that again?"

        text = text.strip()

        # Check for pending context (multi-turn conversation)
        pending = self.context_manager.get_pending(user_id)

        if pending:
            return self._handle_followup(user_id, text, pending)
        else:
            return self._handle_new_message(user_id, text)

    def _handle_new_message(self, user_id: str, text: str) -> str:
        """
        Handle new message (no pending context).

        Args:
            user_id: User identifier
            text: Message text

        Returns:
            Response string
        """
        # Detect intent
        intent = self.intent_engine.detect_intent(text)

        if not intent:
            return "I didn't understand. Can you rephrase?"

        # Handle knowledge queries directly
        if intent == "ask_knowledge":
            entities = self.intent_engine.extract_entities(text, intent)
            key = entities.get("key", text)
            return self.knowledge.query(key)

        # Handle learn commands directly
        if intent == "learn_knowledge":
            entities = self.intent_engine.extract_entities(text, intent)
            key = entities.get("key")
            value = entities.get("value")

            if not key:
                self.context_manager.set_pending(user_id, intent, entities, ["key", "value"])
                return self.intent_engine.prompt_for_entity("key")

            if not value:
                self.context_manager.set_pending(user_id, intent, entities, ["value"])
                return self.intent_engine.prompt_for_entity("value")

            self.knowledge.add_knowledge(key, value)
            return f"Learned '{key}' = '{value}'"

        # Extract entities
        entities = self.intent_engine.extract_entities(text, intent)

        # Get required entities for this intent
        required = self.action_router.get_required_entities(intent)

        # Check for missing entities
        missing = self.intent_engine.get_missing_entities(required, entities)

        if missing:
            # Save context and ask for missing entity
            self.context_manager.set_pending(user_id, intent, entities, missing)
            return self.intent_engine.prompt_for_entity(missing[0])

        # All entities present, execute action
        response = self.action_router.route(intent, entities)
        return response

    def _handle_followup(self, user_id: str, text: str, context) -> str:
        """
        Handle follow-up message (has pending context).

        Args:
            user_id: User identifier
            text: Message text
            context: Pending conversation context

        Returns:
            Response string
        """
        # Try to extract the missing entity from user's response
        missing_entity = context.missing_entities[0] if context.missing_entities else None

        if not missing_entity:
            # No missing entities, execute action
            self.context_manager.clear(user_id)
            return self.action_router.route(context.intent, context.entities)

        # For knowledge learning, handle key/value specially
        if context.intent == "learn_knowledge":
            if missing_entity == "key":
                context.entities["key"] = text.strip()
            elif missing_entity == "value":
                context.entities["value"] = text.strip()

        # For other intents, try to extract entity from text
        else:
            extracted = self.intent_engine.extract_entities(text, context.intent)

            if missing_entity in extracted and extracted[missing_entity]:
                context.entities[missing_entity] = extracted[missing_entity]
            else:
                # Assume the entire text is the entity value
                context.entities[missing_entity] = text.strip()

        # Update context
        self.context_manager.update_entities(user_id, context.entities)

        # Check if still missing entities
        if context.missing_entities:
            # Ask for next missing entity
            return self.intent_engine.prompt_for_entity(context.missing_entities[0])

        # All entities collected, execute action
        self.context_manager.clear(user_id)

        # Special handling for learn command
        if context.intent == "learn_knowledge":
            key = context.entities.get("key")
            value = context.entities.get("value")
            if key and value:
                self.knowledge.add_knowledge(key, value)
                return f"Learned '{key}' = '{value}'"

        # Execute action
        return self.action_router.route(context.intent, context.entities)

    def send_message(self, channel_name: str, user_id: str, message: str) -> None:
        """
        Send message via specific channel.

        Args:
            channel_name: Name of channel to use
            user_id: Recipient user ID
            message: Message text to send
        """
        if channel_name in self.channels:
            try:
                self.channels[channel_name].send_message(user_id, message)
            except Exception as e:
                print(f"❌ Failed to send message via {channel_name}: {e}")
        else:
            print(f"⚠ Unknown channel: {channel_name}")

    def run_console_demo(self) -> None:
        """
        Run interactive console demo.

        This demonstrates the bot's capabilities in a simple console interface.
        """
        print("\n" + "=" * 60)
        print("🤖 Multi-Channel Conversational Bot - Console Demo")
        print("=" * 60)
        print("Type 'quit' or 'exit' to stop\n")

        user_id = "demo_user"
        channel = self.channels["internal"]

        # Demo conversation examples
        print("💡 Try these examples:")
        print("  - What's the weather")
        print("  - Learn capital_of_france = Paris")
        print("  - What is the capital of France?")
        print("  - Tell me the weather in Tokyo")
        print()

        while True:
            try:
                # Get user input
                user_input = input("[You] → ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break

                if not user_input:
                    continue

                # Process message
                response = self.process_message(user_id, user_input, "internal")

                # Send response
                channel.send_message(user_id, response)
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

