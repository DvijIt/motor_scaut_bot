"""
Main application entry point for Car Scout
Coordinates the bot, scraper, and alert system
"""

import os
import asyncio
import logging
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from src.bot.telegram_bot import CarScoutBot
from src.scraper.kleinanzeigen_scraper import KleinanzeigenScraper
from src.database.models import db_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('car_scout.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CarScoutApp:
    """Main application class that coordinates all components"""
    
    def __init__(self):
        self.bot = CarScoutBot()
        self.scraper = KleinanzeigenScraper(delay_seconds=5)
        self.db = db_manager
        
        # Create database tables
        self.db.create_tables()
        logger.info("Database tables created/verified")
    
    async def process_search_alerts(self):
        """Process all active search alerts and send notifications"""
        logger.info("Starting search alert processing...")
        
        # Get all active search alerts
        search_alerts = self.db.get_active_search_alerts()
        logger.info(f"Processing {len(search_alerts)} active search alerts")
        
        for alert in search_alerts:
            try:
                await self.process_single_alert(alert)
                
                # Update last check time
                session = self.db.get_session()
                alert.last_check = datetime.utcnow()
                session.commit()
                session.close()
                
                # Small delay between processing alerts
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing alert {alert.id}: {e}")
    
    async def process_single_alert(self, alert):
        """Process a single search alert"""
        logger.info(f"Processing alert {alert.id} for user {alert.user.telegram_id}")
        
        # Build search URL
        search_url = self.scraper.build_search_url(
            brand=alert.brand,
            min_price=alert.min_price,
            max_price=alert.max_price,
            location=alert.location,
            radius=alert.radius,
            min_year=alert.min_year,
            max_mileage=alert.max_mileage
        )
        
        # Scrape listings (only first page for alerts)
        listings = self.scraper.scrape_listings(search_url, max_pages=1)
        
        new_listings_count = 0
        
        for listing in listings:
            try:
                # Save listing to database
                listing_data = {
                    'external_id': listing.id,
                    'title': listing.title,
                    'price': listing.price,
                    'location': listing.location,
                    'date_posted': listing.date,
                    'description': listing.description,
                    'url': listing.url,
                    'image_url': listing.image_url,
                    'mileage': listing.mileage,
                    'year': listing.year,
                    'fuel_type': listing.fuel_type
                }
                
                saved_listing = self.db.save_car_listing(listing_data)
                
                # Check if we've already sent this listing to this user
                if not self.db.has_been_sent(alert.id, saved_listing.id):
                    # Check if listing is new (within last 2 hours)
                    is_new_listing = (
                        datetime.utcnow() - saved_listing.first_seen
                    ) < timedelta(hours=2)
                    
                    if is_new_listing:
                        # Send alert to user
                        await self.send_listing_alert(alert.user, listing)
                        
                        # Mark as sent
                        self.db.mark_listing_sent(alert.id, saved_listing.id)
                        new_listings_count += 1
                        
                        logger.info(f"Sent alert for listing {listing.id} to user {alert.user.telegram_id}")
                        
                        # Small delay between notifications
                        await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error processing listing {listing.id}: {e}")
        
        logger.info(f"Sent {new_listings_count} new alerts for search {alert.id}")
    
    async def send_listing_alert(self, user, listing):
        """Send a car listing alert to a user"""
        if not user.notifications_enabled:
            return
        
        try:
            alert_text = f"""
🚗 **New Car Match!**

**{listing.title}**
💰 **Price:** €{listing.price:,}
📍 **Location:** {listing.location}
📅 **Posted:** {listing.date}

"""
            
            if listing.year:
                alert_text += f"📅 **Year:** {listing.year}\\n"
            if listing.mileage:
                alert_text += f"🛣️ **Mileage:** {listing.mileage}\\n"
            if listing.fuel_type:
                alert_text += f"⛽ **Fuel:** {listing.fuel_type}\\n"
                
            if listing.description:
                # Truncate description to avoid message length limits
                desc = listing.description[:300]
                if len(listing.description) > 300:
                    desc += "..."
                alert_text += f"\\n📝 **Description:**\\n{desc}\\n"
            
            alert_text += f"\\n🔗 [View on Kleinanzeigen.de]({listing.url})"
            
            await self.bot.application.bot.send_message(
                chat_id=user.telegram_id,
                text=alert_text,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            
        except Exception as e:
            logger.error(f"Failed to send alert to user {user.telegram_id}: {e}")
    
    def run_scheduled_tasks(self):
        """Run scheduled tasks in a separate thread"""
        schedule.every(10).minutes.do(self.schedule_alert_processing)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def schedule_alert_processing(self):
        """Schedule alert processing to run in async context"""
        asyncio.create_task(self.process_search_alerts())
    
    async def start_bot(self):
        """Start the Telegram bot"""
        logger.info("Starting Telegram bot...")
        
        # Start the bot
        await self.bot.application.initialize()
        await self.bot.application.start()
        await self.bot.application.updater.start_polling()
        
        logger.info("Bot started successfully")
    
    async def run_async(self):
        """Run the application asynchronously"""
        # Start bot
        await self.start_bot()
        
        # Run alert processing loop
        while True:
            try:
                await self.process_search_alerts()
                await asyncio.sleep(600)  # Wait 10 minutes
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main entry point"""
    logger.info("Starting Car Scout application...")
    
    # Verify required environment variables
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.error("Please check your .env file")
        return
    
    # Create and run the application
    app = CarScoutApp()
    
    try:
        # For development, just run the bot
        if os.getenv('DEVELOPMENT', 'false').lower() == 'true':
            logger.info("Running in development mode (bot only)")
            app.bot.run()
        else:
            # For production, run full application
            logger.info("Running in production mode (bot + alerts)")
            asyncio.run(app.run_async())
            
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")

if __name__ == "__main__":
    main()
