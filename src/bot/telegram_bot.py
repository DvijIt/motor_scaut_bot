"""
Telegram Bot for Car Scout Service
Handles user interactions, subscriptions, and alert sending
"""

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
    MenuButtonCommands,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


@dataclass
class MenuItem:
    """Represents a menu item with text and callback data"""

    text: str
    callback_data: str
    icon: str = ""


@dataclass
class MenuSection:
    """Represents a section of menu items"""

    items: List[MenuItem]
    title: str = ""


class MenuBuilder:
    """Responsible for building menu keyboards"""

    @staticmethod
    def create_keyboard(
        items: List[MenuItem], back_data: Optional[str] = None
    ) -> InlineKeyboardMarkup:
        """Create a keyboard with menu items and optional back button"""
        keyboard = []

        # Add menu items
        for item in items:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"{item.icon} {item.text}", callback_data=item.callback_data
                    )
                ]
            )

        # Add back button if specified
        if back_data:
            keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data=back_data)])

        return InlineKeyboardMarkup(keyboard)


class MenuContent:
    """Contains all menu content and text"""

    @staticmethod
    def get_welcome_text(user_name: str) -> str:
        return f"""
🚗 **Welcome to Car Scout, {user_name}!**

Find your perfect car deal on Kleinanzeigen.de with instant alerts! 🎯

**Choose what you want to do:**
        """

    @staticmethod
    def get_help_text() -> str:
        return """
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

    @staticmethod
    def get_pricing_text() -> str:
        return """
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

    @staticmethod
    def get_find_cars_text() -> str:
        return """
🎯 **Find Your Perfect Car**

Set up smart alerts to get notified when cars matching your criteria are posted on Kleinanzeigen.de!

**What do you want to do?**
        """

    @staticmethod
    def get_account_text() -> str:
        return """
📊 **My Account**

**Current Status:**
🔄 Subscription: Free Trial (6 days left)
🎯 Active Searches: 1 of 1 allowed
📱 Notifications: Enabled

**Account Actions:**
        """

    @staticmethod
    def get_how_it_works_text() -> str:
        return """
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

    @staticmethod
    def get_free_trial_text() -> str:
        return """
🎉 **Welcome to Your Free Trial!**

**You now have:**
✅ 7 days of free access
✅ 1 car search alert
✅ Instant notifications

**Next Step:**
Let's create your first car search! I'll ask you a few quick questions about what car you're looking for.

**Ready to start?**
        """

    @staticmethod
    def get_status_text() -> str:
        return """
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

    @staticmethod
    def get_settings_text() -> str:
        return """
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


class MenuStructure:
    """Defines the structure of all menus"""

    @staticmethod
    def get_main_menu() -> List[MenuItem]:
        return [
            MenuItem("Find Cars", "find_cars", "🎯"),
            MenuItem("My Account", "my_account", "📊"),
            MenuItem("Pricing", "pricing", "💰"),
            MenuItem("How it Works", "how_it_works", "❓"),
            MenuItem("Start Free Trial", "start_free_trial", "🆓"),
        ]

    @staticmethod
    def get_find_cars_menu() -> List[MenuItem]:
        return [
            MenuItem("Create New Search", "create_search", "➕"),
            MenuItem("My Active Searches", "my_searches", "📋"),
            MenuItem("Browse Recent Cars", "browse_cars", "🔍"),
        ]

    @staticmethod
    def get_account_menu() -> List[MenuItem]:
        return [
            MenuItem("Upgrade Plan", "pricing", "📈"),
            MenuItem("Settings", "account_settings", "⚙️"),
            MenuItem("View My Searches", "my_searches", "📋"),
            MenuItem("Usage Stats", "usage_stats", "📊"),
        ]

    @staticmethod
    def get_pricing_menu() -> List[MenuItem]:
        return [
            MenuItem("Start Free Trial", "start_free_trial", "🆓"),
            MenuItem("Basic €5", "plan_basic", "🥉"),
            MenuItem("Pro €10", "plan_pro", "🥈"),
            MenuItem("Premium €15", "plan_premium", "🥇"),
        ]

    @staticmethod
    def get_how_it_works_menu() -> List[MenuItem]:
        return []

    @staticmethod
    def get_help_menu() -> List[MenuItem]:
        return [
            MenuItem("Create First Search", "create_search", "🎯"),
            MenuItem("How it Works", "how_it_works", "❓"),
        ]

    @staticmethod
    def get_free_trial_menu() -> List[MenuItem]:
        return [
            MenuItem("Create My First Search", "create_search", "🚀"),
            MenuItem("See Example Search", "example_search", "📋"),
        ]

    @staticmethod
    def get_status_menu() -> List[MenuItem]:
        return [
            MenuItem("Add Search", "add_search", "➕"),
            MenuItem("Manage Alerts", "manage_alerts", "⚙️"),
            MenuItem("Upgrade Plan", "upgrade", "⬆️"),
        ]

    @staticmethod
    def get_settings_menu() -> List[MenuItem]:
        return [
            MenuItem("Notification Settings", "notifications", "🔔"),
            MenuItem("Change Location", "location", "🌍"),
            MenuItem("Billing Info", "billing", "💳"),
        ]


class MenuHandler(ABC):
    """Abstract base class for menu handlers"""

    def __init__(self, bot: "CarScoutBot"):
        self.bot = bot

    @abstractmethod
    async def handle(self, query, **kwargs) -> None:
        """Handle the menu action"""
        pass


class MainMenuHandler(MenuHandler):
    """Handles main menu display"""

    async def handle(self, query, **kwargs) -> None:
        user = query.from_user if hasattr(query, "from_user") else query.effective_user
        welcome_text = MenuContent.get_welcome_text(user.first_name)
        keyboard = MenuBuilder.create_keyboard(MenuStructure.get_main_menu())

        if hasattr(query, "edit_message_text"):
            await query.edit_message_text(
                welcome_text, reply_markup=keyboard, parse_mode="HTML"
            )
        else:
            await query.message.reply_html(welcome_text, reply_markup=keyboard)


class FindCarsMenuHandler(MenuHandler):
    """Handles find cars menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_find_cars_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_find_cars_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class AccountMenuHandler(MenuHandler):
    """Handles account menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_account_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_account_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class PricingMenuHandler(MenuHandler):
    """Handles pricing menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_pricing_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_pricing_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class HowItWorksHandler(MenuHandler):
    """Handles how it works menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_how_it_works_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_how_it_works_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class HelpMenuHandler(MenuHandler):
    """Handles help menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_help_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_help_menu(), back_data="back_to_main"
        )

        if hasattr(query, "edit_message_text"):
            await query.edit_message_text(
                text, reply_markup=keyboard, parse_mode="HTML"
            )
        else:
            await query.message.reply_html(text, reply_markup=keyboard)


class FreeTrialHandler(MenuHandler):
    """Handles free trial flow"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_free_trial_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_free_trial_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class StatusMenuHandler(MenuHandler):
    """Handles status menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_status_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_status_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class SettingsMenuHandler(MenuHandler):
    """Handles settings menu"""

    async def handle(self, query, **kwargs) -> None:
        text = MenuContent.get_settings_text()
        keyboard = MenuBuilder.create_keyboard(
            MenuStructure.get_settings_menu(), back_data="back_to_main"
        )
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="HTML")


class PlanSelectionHandler(MenuHandler):
    """Handles plan selection"""

    async def handle(self, query, plan_type: str, **kwargs) -> None:
        plan_info = {
            "basic": {"name": "Basic", "price": "€5", "features": "3 search filters"},
            "pro": {
                "name": "Pro",
                "price": "€10",
                "features": "10 search filters + priority alerts",
            },
            "premium": {
                "name": "Premium",
                "price": "€15",
                "features": "Unlimited filters + premium support",
            },
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
            [
                InlineKeyboardButton(
                    "🆓 Start Free Trial Instead", callback_data="start_free_trial"
                )
            ],
            [
                InlineKeyboardButton("🔙 Back to Plans", callback_data="pricing"),
                InlineKeyboardButton("🏠 Main Menu", callback_data="back_to_main"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class SearchFlowHandler(MenuHandler):
    """Handles search creation flow"""

    async def handle(self, query, **kwargs) -> None:
        await query.edit_message_text(
            "🎯 **Create New Car Search**\n\n"
            "I'll help you set up a new car alert. "
            "Please send me the car brand you're looking for (e.g., BMW, Audi, Volkswagen):",
            parse_mode="HTML",
        )


class MySearchesHandler(MenuHandler):
    """Handles my searches display"""

    async def handle(self, query, **kwargs) -> None:
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
            [InlineKeyboardButton("🔙 Back", callback_data="find_cars")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class BrowseCarsHandler(MenuHandler):
    """Handles browsing recent cars"""

    async def handle(self, query, **kwargs) -> None:
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
            [
                InlineKeyboardButton(
                    "🎯 Create Search Alert", callback_data="create_search"
                )
            ],
            [InlineKeyboardButton("🔄 Refresh Results", callback_data="browse_cars")],
            [InlineKeyboardButton("� Back", callback_data="find_cars")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class AccountSettingsHandler(MenuHandler):
    """Handles account settings"""

    async def handle(self, query, **kwargs) -> None:
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
            [
                InlineKeyboardButton(
                    "🔔 Notification Settings", callback_data="notification_settings"
                )
            ],
            [
                InlineKeyboardButton(
                    "🌍 Location Settings", callback_data="location_settings"
                )
            ],
            [InlineKeyboardButton("� Back to Account", callback_data="my_account")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class UsageStatsHandler(MenuHandler):
    """Handles usage statistics display"""

    async def handle(self, query, **kwargs) -> None:
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
            [InlineKeyboardButton("🔙 Back to Account", callback_data="my_account")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class ExampleSearchHandler(MenuHandler):
    """Handles example search display"""

    async def handle(self, query, **kwargs) -> None:
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
            [
                InlineKeyboardButton(
                    "🚀 Create Similar Search", callback_data="create_search"
                )
            ],
            [
                InlineKeyboardButton(
                    "📋 See Another Example", callback_data="example_search_2"
                )
            ],
            [InlineKeyboardButton("� Back", callback_data="start_free_trial")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="HTML"
        )


class MenuHandlerFactory:
    """Factory for creating menu handlers"""

    def __init__(self, bot: "CarScoutBot"):
        self.bot = bot
        self._handlers = {
            "main_menu": MainMenuHandler(bot),
            "find_cars": FindCarsMenuHandler(bot),
            "my_account": AccountMenuHandler(bot),
            "pricing": PricingMenuHandler(bot),
            "help": HelpMenuHandler(bot),
            "start_free_trial": FreeTrialHandler(bot),
            "status": StatusMenuHandler(bot),
            "settings": SettingsMenuHandler(bot),
            "create_search": SearchFlowHandler(bot),
            "my_searches": MySearchesHandler(bot),
            "browse_cars": BrowseCarsHandler(bot),
            "account_settings": AccountSettingsHandler(bot),
            "usage_stats": UsageStatsHandler(bot),
            "example_search": ExampleSearchHandler(bot),
            "how_it_works": HowItWorksHandler(bot),
        }

    def get_handler(self, action: str) -> Optional[MenuHandler]:
        """Get handler for specific action"""
        return self._handlers.get(action)

    def get_plan_handler(self) -> PlanSelectionHandler:
        """Get plan selection handler"""
        return PlanSelectionHandler(self.bot)


class CarScoutBot:
    """Main bot class implementing SOLID principles"""

    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

        self.application = ApplicationBuilder().token(self.token).build()
        self.menu_factory = MenuHandlerFactory(self)
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up all bot command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("find", self.find_command))
        self.application.add_handler(CommandHandler("account", self.account_command))
        self.application.add_handler(CommandHandler("pricing", self.pricing_command))
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
        await self.menu_factory.get_handler("main_menu").handle(update)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await self.menu_factory.get_handler("help").handle(update)

    async def find_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /find command"""
        await self.menu_factory.get_handler("find_cars").handle(update)

    async def account_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /account command"""
        await self.menu_factory.get_handler("my_account").handle(update)

    async def pricing_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pricing command"""
        await self.menu_factory.get_handler("pricing").handle(update)

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        await self.menu_factory.get_handler("status").handle(update)

    async def settings_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle /settings command"""
        await self.menu_factory.get_handler("settings").handle(update)

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks with unified routing"""
        query = update.callback_query
        await query.answer()

        data = query.data

        # Handle navigation
        if data == "back_to_main":
            await self.menu_factory.get_handler("main_menu").handle(query)
            return

        # Handle plan selections
        if data.startswith("plan_"):
            plan_type = data.replace("plan_", "")
            await self.menu_factory.get_plan_handler().handle(
                query, plan_type=plan_type
            )
            return

        # Handle other actions
        handler = self.menu_factory.get_handler(data)
        if handler:
            await handler.handle(query)
        else:
            await query.edit_message_text("Unknown action. Please try again.")
            await self.menu_factory.get_handler("main_menu").handle(query)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        response = (
            "Thanks for your message! 👋\n\n"
            "Use /help to see available commands or /start to get started with car alerts!"
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
                parse_mode="Markdown",
                disable_web_page_preview=False,
            )

            logger.info(f"Car alert sent to user {user_id}")

        except Exception as e:
            logger.error(f"Failed to send alert to user {user_id}: {e}")

    async def post_init(self, application):
        """Set up menu button after bot starts"""
        await self._setup_menu_button_direct()

    async def _setup_menu_button_direct(self):
        """Set up the persistent menu button with bot commands"""
        try:
            commands = [
                BotCommand("start", "🏠 Main Menu - Get started with Car Scout"),
                BotCommand("find", "🎯 Find Cars - Search for your perfect car"),
                BotCommand("account", "📊 My Account - View subscription & searches"),
                BotCommand("pricing", "💰 Pricing - See subscription plans"),
                BotCommand("help", "❓ Help - Learn how Car Scout works"),
                BotCommand(
                    "settings", "⚙️ Settings - Manage notifications & preferences"
                ),
            ]

            await self.application.bot.set_my_commands(commands)

            menu_button = MenuButtonCommands()
            await self.application.bot.set_chat_menu_button(menu_button=menu_button)

            logger.info("Menu button and commands set up successfully")

        except Exception as e:
            logger.error(f"Failed to set up menu button: {e}")

    def run(self):
        """Start the bot"""
        logger.info("Starting Car Scout Bot...")

        self.application.post_init = self.post_init
        self.application.run_polling()


if __name__ == "__main__":
    bot = CarScoutBot()
    bot.run()
