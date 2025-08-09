"""
Telegram Bot for Car Scout Service
Handles user interactions, subscriptions, and alert sending
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, MenuButtonCommands, BotCommand
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
        
        # New menu command handlers
        self.application.add_handler(CommandHandler("find", self.find_command))
        self.application.add_handler(CommandHandler("account", self.account_command))
        self.application.add_handler(CommandHandler("pricing", self.pricing_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for text messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    

    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command with simple main menu"""
        user = update.effective_user
        welcome_text = f"""
🚗 **Welcome to Car Scout, {user.first_name}!**

Find your perfect car deal on Kleinanzeigen.de with instant alerts! 🎯

**Choose what you want to do:**
        """
        
        # Simple main menu with clear options
        keyboard = [
            [
                InlineKeyboardButton("🎯 Find Cars", callback_data="find_cars"),
                InlineKeyboardButton("📊 My Account", callback_data="my_account")
            ],
            [
                InlineKeyboardButton("💰 Pricing", callback_data="pricing"),
                InlineKeyboardButton("❓ How it Works", callback_data="how_it_works")
            ],
            [
                InlineKeyboardButton("🆓 Start Free Trial", callback_data="start_free_trial")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            welcome_text,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 **Car Scout Bot Help**

**📱 Easy Navigation:**
• Tap the **Menu** button next to the message field
• Use the quick commands from the menu
• Or use buttons in any message

**🎯 Main Commands:**
/start - 🏠 Main Menu
/find - 🎯 Find Cars
/account - 📊 My Account  
/pricing - 💰 View Plans
/help - ❓ This help message
/settings - ⚙️ Bot settings

**📋 How Car Scout Works:**
1. **Set Your Criteria** - Tell me what car you want
2. **We Monitor 24/7** - Check Kleinanzeigen.de constantly  
3. **Get Instant Alerts** - Telegram notifications when matches found
4. **Be First to Contact** - Beat other buyers to great deals!

**💡 Pro Tips:**
• Use specific search criteria for better results
• Set realistic price ranges  
• Try different locations and radius
• Enable notifications for fastest alerts

**Need help?** Just send me a message! 💬
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Create First Search", callback_data="create_search")],
            [InlineKeyboardButton("❓ How it Works", callback_data="how_it_works")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            help_text,
            reply_markup=reply_markup
        )
    
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
        
        # Main menu options
        if data == "find_cars":
            await self.show_find_cars_menu(query)
        elif data == "my_account":
            await self.show_my_account_menu(query)
        elif data == "pricing":
            await self.show_pricing_menu(query)
        elif data == "how_it_works":
            await self.show_how_it_works(query)
        elif data == "start_free_trial":
            await self.start_free_trial_flow(query)
        
        # Legacy/secondary menu options
        elif data == "subscribe":
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
        
        # Navigation
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
        
        # Additional handlers for new menu items
        elif data == "my_searches":
            await self.show_my_searches(query)
        elif data == "browse_cars":
            await self.browse_recent_cars(query)
        elif data == "account_settings":
            await self.show_account_settings(query)
        elif data == "usage_stats":
            await self.show_usage_stats(query)
        elif data == "example_search":
            await self.show_example_search(query)
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
    
    async def show_find_cars_menu(self, query):
        """Show Find Cars menu - main functionality"""
        text = """
🎯 **Find Your Perfect Car**

Set up smart alerts to get notified when cars matching your criteria are posted on Kleinanzeigen.de!

**What do you want to do?**
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Create New Search", callback_data="create_search")],
            [InlineKeyboardButton("📋 My Active Searches", callback_data="my_searches")],
            [InlineKeyboardButton("🔍 Browse Recent Cars", callback_data="browse_cars")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_my_account_menu(self, query):
        """Show My Account menu"""
        text = """
📊 **My Account**

**Current Status:**
🔄 Subscription: Free Trial (6 days left)
🎯 Active Searches: 1 of 1 allowed
📱 Notifications: Enabled

**Account Actions:**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📈 Upgrade Plan", callback_data="pricing"),
                InlineKeyboardButton("⚙️ Settings", callback_data="account_settings")
            ],
            [
                InlineKeyboardButton("📋 View My Searches", callback_data="my_searches"),
                InlineKeyboardButton("📊 Usage Stats", callback_data="usage_stats")
            ],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_pricing_menu(self, query):
        """Show simplified pricing menu"""
        text = """
💰 **Car Scout Pricing**

**🆓 Free Trial**
• 7 days free access
• 1 search alert
• Basic notifications

**💳 Premium Plans**
• **Basic €5/month** - 3 searches
• **Pro €10/month** - 10 searches ⭐
• **Premium €15/month** - Unlimited

**What would you like to do?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="start_free_trial")],
            [
                InlineKeyboardButton("🥉 Basic €5", callback_data="plan_basic"),
                InlineKeyboardButton("🥈 Pro €10", callback_data="plan_pro")
            ],
            [InlineKeyboardButton("🥇 Premium €15", callback_data="plan_premium")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_how_it_works(self, query):
        """Show How it Works explanation"""
        text = """
❓ **How Car Scout Works**

**1. 🎯 Set Your Criteria**
Tell me what car you want:
• Brand (BMW, Audi, VW, etc.)
• Price range (min-max)
• Location & radius
• Year, mileage, etc.

**2. 🔍 We Monitor 24/7**
I check Kleinanzeigen.de every few minutes for new cars matching your search.

**3. 📱 Get Instant Alerts**
As soon as a matching car is posted, you get a Telegram message with:
• Car details & photos
• Price & location
• Direct link to listing

**4. 🏃‍♂️ Be First to Contact**
You see new cars before most people, giving you the best chance to get great deals!

**Ready to start?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Create My First Search", callback_data="create_search")],
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="start_free_trial")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def start_free_trial_flow(self, query):
        """Start free trial with simplified flow"""
        text = """
🎉 **Welcome to Your Free Trial!**

**You now have:**
✅ 7 days of free access
✅ 1 car search alert
✅ Instant notifications

**Next Step:**
Let's create your first car search! I'll ask you a few quick questions about what car you're looking for.

**Ready to start?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Create My First Search", callback_data="create_search")],
            [InlineKeyboardButton("📋 See Example Search", callback_data="example_search")],
            [InlineKeyboardButton("🔙 Back to Main", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_my_searches(self, query):
        """Show user's active searches"""
        text = """
📋 **My Active Searches**

**Search #1: BMW 3 Series**
🎯 BMW, €10,000-25,000, Munich (50km)
📅 Created: 2 days ago
🔔 Status: Active
📊 Matches found: 3 cars

**Available Actions:**
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Add New Search", callback_data="create_search")],
            [InlineKeyboardButton("⚙️ Edit Search #1", callback_data="edit_search_1")],
            [InlineKeyboardButton("⏸️ Pause Search #1", callback_data="pause_search_1")],
            [InlineKeyboardButton("🔙 Back", callback_data="find_cars")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def browse_recent_cars(self, query):
        """Browse recent cars without setting up alerts"""
        text = """
🔍 **Browse Recent Cars**

**Latest BMW Cars in Munich:**

🚗 **BMW 320d, 2018**
💰 €18,500 | 📍 Munich | 🛣️ 85,000 km
⏰ Posted 2 hours ago

🚗 **BMW X3, 2020** 
💰 €32,000 | 📍 Augsburg | 🛣️ 45,000 km
⏰ Posted 4 hours ago

**Want personalized alerts for cars like these?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Create Search Alert", callback_data="create_search")],
            [InlineKeyboardButton("🔄 Refresh Results", callback_data="browse_cars")],
            [InlineKeyboardButton("🔙 Back", callback_data="find_cars")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_account_settings(self, query):
        """Show account settings"""
        text = """
⚙️ **Account Settings**

**Notification Settings:**
📱 Telegram Alerts: ✅ Enabled
🔔 Sound: ✅ Enabled  
⏰ Quiet Hours: 22:00 - 08:00

**Location Settings:**
🌍 Default Location: Munich, Germany
📍 Default Radius: 50 km

**Language & Currency:**
🌐 Language: English
💰 Currency: EUR (€)
        """
        
        keyboard = [
            [InlineKeyboardButton("🔔 Notification Settings", callback_data="notification_settings")],
            [InlineKeyboardButton("🌍 Location Settings", callback_data="location_settings")],
            [InlineKeyboardButton("🔙 Back to Account", callback_data="my_account")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_usage_stats(self, query):
        """Show usage statistics"""
        text = """
📊 **Usage Statistics**

**This Month:**
🎯 Active Searches: 1
📧 Alerts Sent: 8
🚗 Cars Found: 12
⚡ Response Time: < 2 minutes

**All Time:**
📅 Member Since: 3 days ago
📧 Total Alerts: 8
🎯 Searches Created: 1
💰 Money Saved: Priceless! 😄

**Most Active Search:**
🚗 BMW 3 Series in Munich
   └ 8 alerts sent
        """
        
        keyboard = [
            [InlineKeyboardButton("📈 Detailed Stats", callback_data="detailed_stats")],
            [InlineKeyboardButton("🔙 Back to Account", callback_data="my_account")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def show_example_search(self, query):
        """Show an example search to help users understand"""
        text = """
📋 **Example Car Search**

Here's how a typical search looks:

**Search Name:** "BMW 3 Series for Daily Commute"

**Criteria:**
🚗 **Brand:** BMW
🏷️ **Model:** 3 Series (320d, 320i, 330i)
💰 **Price:** €15,000 - €30,000
📍 **Location:** Munich + 30km radius
📅 **Year:** 2016 or newer
🛣️ **Max Mileage:** 100,000 km
⛽ **Fuel:** Diesel or Petrol

**Result:** You'll get instant alerts when cars matching these criteria are posted!

**Ready to create your own?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Create Similar Search", callback_data="create_search")],
            [InlineKeyboardButton("📋 See Another Example", callback_data="example_search_2")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_free_trial")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    async def find_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /find command - equivalent to 'Find Cars' button"""
        user = update.effective_user
        text = """
🎯 **Find Your Perfect Car**

Set up smart alerts to get notified when cars matching your criteria are posted on Kleinanzeigen.de!

**What do you want to do?**
        """
        
        keyboard = [
            [InlineKeyboardButton("➕ Create New Search", callback_data="create_search")],
            [InlineKeyboardButton("📋 My Active Searches", callback_data="my_searches")],
            [InlineKeyboardButton("🔍 Browse Recent Cars", callback_data="browse_cars")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            text,
            reply_markup=reply_markup
        )
    
    async def account_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /account command - equivalent to 'My Account' button"""
        user = update.effective_user
        text = """
📊 **My Account**

**Current Status:**
🔄 Subscription: Free Trial (6 days left)
🎯 Active Searches: 1 of 1 allowed
📱 Notifications: Enabled

**Account Actions:**
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📈 Upgrade Plan", callback_data="pricing"),
                InlineKeyboardButton("⚙️ Settings", callback_data="account_settings")
            ],
            [
                InlineKeyboardButton("📋 View My Searches", callback_data="my_searches"),
                InlineKeyboardButton("📊 Usage Stats", callback_data="usage_stats")
            ],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            text,
            reply_markup=reply_markup
        )
    
    async def pricing_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pricing command - equivalent to 'Pricing' button"""
        user = update.effective_user
        text = """
💰 **Car Scout Pricing**

**🆓 Free Trial**
• 7 days free access
• 1 search alert
• Basic notifications

**💳 Premium Plans**
• **Basic €5/month** - 3 searches
• **Pro €10/month** - 10 searches ⭐
• **Premium €15/month** - Unlimited

**What would you like to do?**
        """
        
        keyboard = [
            [InlineKeyboardButton("🆓 Start Free Trial", callback_data="start_free_trial")],
            [
                InlineKeyboardButton("🥉 Basic €5", callback_data="plan_basic"),
                InlineKeyboardButton("🥈 Pro €10", callback_data="plan_pro")
            ],
            [InlineKeyboardButton("🥇 Premium €15", callback_data="plan_premium")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_html(
            text,
            reply_markup=reply_markup
        )
    
    async def post_init(self, application):
        """Set up menu button after bot starts"""
        await self._setup_menu_button_direct()
    
    async def _setup_menu_button_direct(self):
        """Set up the persistent menu button with bot commands"""
        try:
            # Define the commands that will appear in the menu
            commands = [
                BotCommand("start", "🏠 Main Menu - Get started with Car Scout"),
                BotCommand("find", "🎯 Find Cars - Search for your perfect car"),
                BotCommand("account", "📊 My Account - View subscription & searches"),
                BotCommand("pricing", "💰 Pricing - See subscription plans"),
                BotCommand("help", "❓ Help - Learn how Car Scout works"),
                BotCommand("settings", "⚙️ Settings - Manage notifications & preferences")
            ]
            
            # Set the commands for the bot
            await self.application.bot.set_my_commands(commands)
            
            # Set the menu button to show commands
            menu_button = MenuButtonCommands()
            await self.application.bot.set_chat_menu_button(menu_button=menu_button)
            
            logger.info("Menu button and commands set up successfully")
            
        except Exception as e:
            logger.error(f"Failed to set up menu button: {e}")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Car Scout Bot...")
        
        # Set up menu button after initialization
        self.application.post_init = self.post_init
        self.application.run_polling()

if __name__ == "__main__":
    bot = CarScoutBot()
    bot.run()
