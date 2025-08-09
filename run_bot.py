#!/usr/bin/env python3
"""
Simple script to run just the Telegram bot for development/testing
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

from src.bot.telegram_bot import CarScoutBot

def main():
    """Run the bot"""
    print("🚗 Starting Car Scout Bot...")
    print("Press Ctrl+C to stop")
    
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please add your bot token to the .env file")
        return
    
    try:
        bot = CarScoutBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n✅ Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
