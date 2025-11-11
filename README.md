# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================
"""
📚 USAGE GUIDE
==============

1. BASIC USAGE (Interactive Mode):
   python bot/main_bot.py

2. AUTOMATED DEMO:
   python bot/main_bot.py --demo

3. PACKAGE STRUCTURE:
   bot/
   ├── __init__.py
   ├── main_bot.py              # Main orchestrator
   ├── core/
   │   ├── knowledge_engine.py   # Knowledge storage
   │   ├── action_router.py      # Intent routing
   │   ├── base_action.py        # Action interface
   │   ├── base_channel.py       # Channel interface
   │   ├── intent_engine.py      # NLP processing
   │   └── context_manager.py    # Conversation state
   ├── skills/
   │   └── weather.py            # Weather skill
   ├── channels/
   │   ├── telegram_channel.py   # Telegram integration
   │   ├── whatsapp_channel.py   # WhatsApp integration
   │   ├── mattermost_channel.py # Mattermost integration
   │   └── internal_channel.py   # Console interface
   └── config/
       └── channels.json         # Channel configuration

4. ADDING NEW SKILLS:
   
   from bot.core.base_action import BaseAction
   
   class MySkill(BaseAction):
       def can_handle(self, intent: str) -> bool:
           return intent == "my_intent"
       
       def required_entities(self) -> List[str]:
           return ["entity1", "entity2"]
       
       def execute(self, params: Dict[str, Any]) -> str:
           # Your logic here
           return "Response"
   
   # Register in main_bot.py:
   self.action_router.register(MySkill())

5. ADDING NEW CHANNELS:
   
   from bot.core.base_channel import BaseChannel
   
   class MyChannel(BaseChannel):
       @property
       def name(self) -> str:
           return "my_channel"
       
       def send_message(self, recipient_id: str, message: str):
           # Send via your API
           pass
       
       def receive_message(self, payload: Any) -> Dict[str, str]:
           # Parse incoming message
           return {"user_id": "...", "text": "..."}

6. EXTENDING INTENT ENGINE:
   
   # Add pattern to IntentEngine.__init__():
   self.intent_patterns["my_intent"] = [
       r"\bmy_pattern\b",
       r"\banother_pattern\b"
   ]
   
   # Add entity extraction in extract_entities()

7. PRODUCTION DEPLOYMENT:
   
   - Replace mock channels with real API clients
   - Add proper error handling and logging
   - Implement webhook endpoints for each channel
   - Add database for persistent knowledge storage
   - Implement rate limiting and security measures
   - Add monitoring and analytics
   - Use environment variables for secrets
   
8. ADVANCED FEATURES TO ADD:
   
   - NLU with spaCy or Hugging Face
   - Vector database (Chroma, FAISS) for semantic search
   - Multi-language support
   - User authentication and authorization
   - Conversation analytics
   - A/B testing framework
   - Sentiment analysis
   - Rich media support (images, buttons, cards)

9. TESTING:
   
   import unittest
   from bot.main_bot import MainBot
   
   class TestBot(unittest.TestCase):
       def setUp(self):
           self.bot = MainBot()
       
       def test_weather_query(self):
           response = self.bot.process_message(
               "user1", 
               "What's the weather in London"
           )
           self.assertIn("London", response)

10. EXAMPLE CONVERSATIONS:
    
    ✓ Simple weather: "weather in NYC" → Direct response
    ✓ Multi-turn: "weather" → "location?" → "NYC" → Response
    ✓ Learning: "learn x = y" → "Learned x = y"
    ✓ Querying: "what is x?" → "y"
    ✓ Unknown: "teach me math" → Fallback message

🎯 KEY FEATURES:
================
✓ Multi-channel support (Telegram, WhatsApp, Mattermost, Console)
✓ Intent detection with fuzzy matching
✓ Entity extraction (regex-based, extensible)
✓ Multi-turn conversations with context management
✓ Missing entity follow-up
✓ Knowledge base with learning capability
✓ Pluggable skills architecture
✓ Graceful error handling
✓ Context timeout and cleanup
✓ Easy to extend and customize

🔧 CONFIGURATION:
=================
Edit bot/config/channels.json to add real API credentials.
Currently uses mock implementations for offline testing.

🚀 NEXT STEPS:
==============
1. Add more skills (calendar, reminders, search, etc.)
2. Integrate real NLU (spaCy, BERT, GPT)
3. Add persistent storage (PostgreSQL, MongoDB)
4. Implement webhook servers for channels
5. Add user authentication
6. Deploy to cloud (AWS, GCP, Azure)
7. Add monitoring and logging (Prometheus, ELK)
8. Implement CI/CD pipeline
"""
                