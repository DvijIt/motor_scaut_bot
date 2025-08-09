"""
Telegram Bot for Car Scout Service
Handles user interactions, subscriptions, and alert sending
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import (
    Application, 
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CarScoutBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        self.application = ApplicationBuilder().token(self.token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up all bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for text messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🚗 Welcome to Car Scout, {user.first_name}!

I help you find great car deals on Kleinanzeigen.de by sending instant alerts when new listings match your criteria.

🔥 **What I can do:**
• Monitor Kleinanzeigen.de 24/7
• Send instant notifications for new cars
• Filter by price, brand, location, and more
• Help you never miss a great deal again!

💰 **Subscription Plans:**
• Basic: €5/month - 3 search filters
• Pro: €10/month - 10 search filters  
• Premium: €15/month - Unlimited filters + priority alerts

📱 **Getting Started:**
Use /subscribe to set up your first car alert!
Use /help to see all available commands.

Ready to find your dream car? 🎯
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Subscription", callback_data="subscribe")],
            [InlineKeyboardButton("📋 View Plans", callback_data="plans")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            welcome_text,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Car Scout Bot Commands:**

/start - Welcome message and getting started
/help - Show this help message
/subscribe - Set up new car search alerts
/status - Check your subscription and active alerts
/settings - Manage your account settings

📋 **How to use:**
1. Use /subscribe to create your first search
2. Set your filters (brand, price, location)
3. Get instant notifications when new cars match!

💡 **Tips:**
• Be specific with your search criteria
• Use location filters to find cars near you
• Set realistic price ranges for better results
• You can pause/resume alerts anytime

Need help? Just send me a message! 💬
        """
        
        await update.message.reply_html(help_text)
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /subscribe command"""
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="free_trial")],
            [InlineKeyboardButton("💳 Choose Plan", callback_data="choose_plan")],
            [InlineKeyboardButton("❓ Learn More", callback_data="learn_more")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        subscribe_text = """
🎯 **Ready to start finding great car deals?**

Choose how you'd like to begin:

🆓 **Free Trial** - 7 days, 1 search filter
💳 **Paid Plans** - Full access with multiple filters
❓ **Learn More** - How the service works

What would you like to do?
        """
        
        await update.message.reply_html(
            subscribe_text,
            reply_markup=reply_markup
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - show user's subscription status"""
        # TODO: Implement database lookup for user status
        status_text = """
📊 **Your Car Scout Status:**

🔄 **Subscription:** Free Trial (6 days remaining)
🎯 **Active Alerts:** 1 of 1 allowed
📱 **Notifications:** Enabled
🔍 **Last Check:** 5 minutes ago

**Your Active Searches:**
🚗 BMW 3 Series, €10,000-25,000, Munich area
   └ Last match: 2 hours ago

💡 Upgrade to Pro for more search filters!
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Search", callback_data="add_search")],
            [InlineKeyboardButton("⚙️ Manage Alerts", callback_data="manage_alerts")],
            [InlineKeyboardButton("⬆️ Upgrade Plan", callback_data="upgrade")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            status_text,
            reply_markup=reply_markup
        )
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        settings_text = """
⚙️ **Car Scout Settings:**

📱 **Notifications:** Enabled
🔔 **Alert Frequency:** Instant
🌍 **Default Location:** Munich, Germany
💰 **Price Format:** EUR (€)
⏰ **Quiet Hours:** 22:00 - 08:00

**Subscription:**
💳 Plan: Free Trial
📅 Expires: December 23, 2024
        """
        
        keyboard = [
            [InlineKeyboardButton("🔔 Notification Settings", callback_data="notifications")],
            [InlineKeyboardButton("🌍 Change Location", callback_data="location")],
            [InlineKeyboardButton("💳 Billing Info", callback_data="billing")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            settings_text,
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "subscribe":
            await self.subscribe_command(update, context)
        elif data == "plans":
            await self.show_plans(query)
        elif data == "help":
            await self.help_command(update, context)
        elif data == "free_trial":
            await self.start_free_trial(query)
        elif data == "choose_plan":
            await self.show_plans(query)
        elif data == "learn_more":
            await self.show_learn_more(query)
        elif data == "add_search":
            await self.add_search_flow(query)
        elif data == "manage_alerts":
            await self.manage_alerts(query)
        elif data == "upgrade":
            await self.show_plans(query)
        elif data == "back_to_main":
            await self.show_main_menu(query)
        elif data == "back_to_subscribe":
            await self.show_subscribe_menu(query)
        elif data == "back_to_plans":
            await self.show_plans(query)
        elif data == "status":
            await self.show_status_menu(query)
        elif data == "trial_start":
            await self.start_free_trial(query)
        elif data.startswith("plan_"):
            plan_type = data.replace("plan_", "")
            await self.handle_plan_selection(query, plan_type)
        elif data == "create_search":
            await self.add_search_flow(query)
        else:
            await query.edit_message_text("Unknown action. Please try again.")
    
    async def show_plans(self, query):
        """Show subscription plans"""
        plans_text = """
💰 **Car Scout Subscription Plans:**

🆓 **Free Trial** - €0
• 7 days free access
• 1 search filter
• Basic notifications

🥉 **Basic Plan** - €5/month
• 3 search filters
• Instant notifications
• Email support

🥈 **Pro Plan** - €10/month ⭐ Most Popular
• 10 search filters
• Priority notifications
• Advanced filters
• Email support

🥇 **Premium Plan** - €15/month
• Unlimited search filters
• Instant priority alerts
• All advanced features
• Premium support

Which plan works best for you?
        """
        
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="trial_start")],
            [InlineKeyboardButton("🥉 Basic €5", callback_data="plan_basic")],
            [InlineKeyboardButton("🥈 Pro €10", callback_data="plan_pro")],
            [InlineKeyboardButton("🥇 Premium €15", callback_data="plan_premium")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_subscribe")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            plans_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def start_free_trial(self, query):
        """Start free trial process"""
        trial_text = """
🎉 **Welcome to your Free Trial!**

You now have 7 days of free access to Car Scout!

🚀 **Next Steps:**
1. Set up your first car search
2. Choose your filters (brand, price, location)
3. Start receiving instant alerts!

Let's create your first search now!
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Create First Search", callback_data="create_search")],
            [InlineKeyboardButton("🔙 Back to Plans", callback_data="back_to_plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            trial_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_learn_more(self, query):
        """Show detailed information about the service"""
        learn_text = """
🎓 **How Car Scout Works:**

**1. Set Your Search Criteria** 🎯
• Choose car brand (BMW, Audi, VW, etc.)
• Set price range (min-max)
• Select location radius
• Add specific model or features

**2. We Monitor 24/7** 👁️
• Check Kleinanzeigen.de every few minutes
• Find new listings that match your criteria
• Filter out duplicates and irrelevant posts

**3. Get Instant Alerts** 📱
• Receive Telegram notifications immediately
• See photos, price, and direct link
• Be the first to contact sellers

**4. Find Great Deals** 💰
• Never miss price drops
• Spot rare models quickly
• Get notifications faster than email alerts

Ready to start? 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Free Trial", callback_data="trial_start")],
            [InlineKeyboardButton("🔙 Back to Plans", callback_data="back_to_plans")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            learn_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def add_search_flow(self, query):
        """Start the flow to add a new search"""
        await query.edit_message_text(
            "🎯 **Create New Car Search**\n\n"
            "I'll help you set up a new car alert. "
            "Please send me the car brand you're looking for (e.g., BMW, Audi, Volkswagen):",
            parse_mode='HTML'
        )
        # TODO: Implement conversation state management
    
    async def manage_alerts(self, query):
        """Manage existing alerts"""
        # TODO: Implement alert management
        await query.edit_message_text(
            "⚙️ **Manage Your Alerts**\n\n"
            "Alert management coming soon! "
            "For now, use /status to see your active searches.",
            parse_mode='HTML'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        # TODO: Implement conversation flow handling
        response = (
            "Thanks for your message! 👋\n\n"
            "Use /help to see available commands or /subscribe to get started with car alerts!"
        )
        await update.message.reply_text(response)
    
    async def send_car_alert(self, user_id: int, car_listing: dict):
        """Send a car alert to a specific user"""
        try:
            alert_text = f"""
🚗 **New Car Alert!**

**{car_listing['title']}**
💰 Price: €{car_listing['price']:,}
📍 Location: {car_listing['location']}
📅 Posted: {car_listing['date']}

{car_listing['description'][:200]}...

🔗 [View on Kleinanzeigen.de]({car_listing['url']})
            """
            
            await self.application.bot.send_message(
                chat_id=user_id,
                text=alert_text,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            
            logger.info(f"Car alert sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to send alert to user {user_id}: {e}")
    
    async def show_main_menu(self, query):
        """Show main menu - equivalent to /start command"""
        user = query.from_user
        welcome_text = f"""
🚗 Welcome back to Car Scout, {user.first_name}!

I help you find great car deals on Kleinanzeigen.de by sending instant alerts when new listings match your criteria.

🔥 **What I can do:**
• Monitor Kleinanzeigen.de 24/7
• Send instant notifications for new cars
• Filter by price, brand, location, and more
• Help you never miss a great deal again!

💰 **Subscription Plans:**
• Basic: €5/month - 3 search filters
• Pro: €10/month - 10 search filters  
• Premium: €15/month - Unlimited filters + priority alerts

📱 **Quick Actions:**
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Start Subscription", callback_data="subscribe")],
            [InlineKeyboardButton("📋 View Plans", callback_data="plans")],
            [InlineKeyboardButton("📊 My Status", callback_data="status")],
            [InlineKeyboardButton("❓ Help", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_subscribe_menu(self, query):
        """Show subscription menu"""
        subscribe_text = """
🎯 **Ready to start finding great car deals?**

Choose how you'd like to begin:

🆓 **Free Trial** - 7 days, 1 search filter
💳 **Paid Plans** - Full access with multiple filters
❓ **Learn More** - How the service works

What would you like to do?
        """
        
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="free_trial")],
            [InlineKeyboardButton("💳 Choose Plan", callback_data="choose_plan")],
            [InlineKeyboardButton("❓ Learn More", callback_data="learn_more")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            subscribe_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_status_menu(self, query):
        """Show status menu like the /status command"""
        status_text = """
📊 **Your Car Scout Status:**

🔄 **Subscription:** Free Trial (6 days remaining)
🎯 **Active Alerts:** 1 of 1 allowed
📱 **Notifications:** Enabled
🔍 **Last Check:** 5 minutes ago

**Your Active Searches:**
🚗 BMW 3 Series, €10,000-25,000, Munich area
   └ Last match: 2 hours ago

💡 Upgrade to Pro for more search filters!
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add Search", callback_data="add_search")],
            [InlineKeyboardButton("⚙️ Manage Alerts", callback_data="manage_alerts")],
            [InlineKeyboardButton("⬆️ Upgrade Plan", callback_data="upgrade")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            status_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def handle_plan_selection(self, query, plan_type):
        """Handle specific plan selection"""
        plan_info = {
            "basic": {"name": "Basic", "price": "€5", "features": "3 search filters"},
            "pro": {"name": "Pro", "price": "€10", "features": "10 search filters + priority alerts"},
            "premium": {"name": "Premium", "price": "€15", "features": "Unlimited filters + premium support"}
        }
        
        plan = plan_info.get(plan_type, plan_info["basic"])
        
        text = f"""
✅ **{plan['name']} Plan Selected!**

💰 **Price:** {plan['price']}/month
🎯 **Features:** {plan['features']}

🚧 **Payment integration coming soon!**

For now, you can start with our free trial and we'll notify you when payment is ready.
        """
        
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial Instead", callback_data="trial_start")],
            [InlineKeyboardButton("🔙 Back to Plans", callback_data="back_to_plans")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Car Scout Bot...")
        self.application.run_polling()

if __name__ == "__main__":
    bot = CarScoutBot()
    bot.run()
