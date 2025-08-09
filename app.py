"""
Simplified deployment version for Render
Just runs the Telegram bot without complex scheduling
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main entry point for deployment"""
    logger.info("Starting Car Scout Bot for deployment...")
    
    # Check required environment variables
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
        sys.exit(1)
    
    try:
        # Import and start the bot
        from src.bot.telegram_bot import CarScoutBot
        
        bot = CarScoutBot()
        logger.info("Bot initialized successfully")
        
        # Run the bot
        bot.run()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
