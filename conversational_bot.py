"""
Multi-Channel Conversational Bot Package
==========================================
A complete implementation of an extensible conversational bot with:
- Knowledge engine
- Intent extraction and entity handling
- Multi-turn conversations with missing entity follow-up
- Multiple channel support (Telegram, WhatsApp, Mattermost, Internal)
- Pluggable skills architecture
"""
import json
from pathlib import Path

from bot.main_bot import MainBot


# ============================================================================
# Example usage and main entry point
# ============================================================================

def create_sample_config():
    """Create a sample channels.json config file."""
    config = {
        "telegram": {
            "api_token": "FAKE_TELEGRAM_TOKEN_12345"
        },
        "whatsapp": {
            "api_key": "FAKE_WHATSAPP_KEY_67890"
        },
        "mattermost": {
            "webhook_url": "https://mattermost.example.com/hooks/fake123"
        }
    }
    
    config_dir = Path("bot/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = config_dir / "channels.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    return str(config_path)


def run_automated_demo():
    """Run automated demonstration of bot capabilities."""
    print("\n" + "="*60)
    print("🤖 AUTOMATED DEMO - Multi-Channel Conversational Bot")
    print("="*60 + "\n")
    
    # Initialize bot
    bot = MainBot()
    channel = bot.channels["internal"]
    user_id = "demo_user"
    
    # Demo conversations
    demo_conversations = [
        # Example 1: Multi-turn weather query
        {
            "title": "Example 1: Multi-turn Weather Query",
            "messages": [
                "What's the weather",
                "in Tokyo"
            ]
        },
        # Example 2: Learning and querying knowledge
        {
            "title": "Example 2: Learning Knowledge",
            "messages": [
                "learn capital_of_germany = Berlin",
                "what is the capital of Germany?",
                "what is the capital of Spain?"
            ]
        },
        # Example 3: Direct weather query with location
        {
            "title": "Example 3: Direct Weather Query",
            "messages": [
                "Tell me the weather in Paris"
            ]
        },
        # Example 4: Multi-turn learning
        {
            "title": "Example 4: Multi-turn Learning",
            "messages": [
                "learn something new",
                "capital_of_japan",
                "Tokyo"
            ]
        },
        # Example 5: Unknown intent
        {
            "title": "Example 5: Handling Unknown Intent",
            "messages": [
                "Can you dance?",
            ]
        }
    ]
    
    for demo in demo_conversations:
        print(f"\n{'─'*60}")
        print(f"📌 {demo['title']}")
        print('─'*60 + "\n")
        
        for msg in demo['messages']:
            print(f"[You] → {msg}")
            response = bot.process_message(user_id, msg, "internal")
            channel.send_message(user_id, response)
            print()
        
        # Clear context between examples
        bot.context_manager.clear(user_id)
    
    print("="*60)
    print("✅ Demo completed!")
    print("="*60 + "\n")


def main():
    """Main entry point."""
    import sys
    
    print("\n🚀 Starting Bot System...\n")
    
    # Create sample config
    config_path = create_sample_config()
    print(f"✓ Created sample config: {config_path}\n")
    
    # Choose mode
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run automated demo
        run_automated_demo()
    else:
        # Run interactive console
        bot = MainBot(config_path)
        bot.run_console_demo()


if __name__ == "__main__":
    main()


