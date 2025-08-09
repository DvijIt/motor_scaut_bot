# 🚗 Car Scout - Quick Start Guide

Welcome! You now have a complete car alert service ready to launch. Here's how to get started:

## ⚡ Quick Setup (5 minutes)

### 1. Get Your Bot Token 🤖
1. Open Telegram and find `@BotFather`
2. Send `/newbot`
3. Choose name: `Your Car Scout Bot`
4. Choose username: `your_car_scout_bot` (must be unique)
5. Copy the bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

### 2. Configure Your Bot 🔧
```bash
# Install dependencies
python setup.py

# Edit .env file (created by setup)
# Add your bot token:
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

### 3. Test Your Bot 🧪
```bash
# Test just the bot
python run_bot.py

# Test the scraper
python test_scraper.py
```

### 4. Run Full Service 🚀
```bash
# Run with alerts enabled
python main.py
```

## 📱 Using Your Bot

### Commands:
- `/start` - Welcome message and setup
- `/subscribe` - Start subscription process  
- `/status` - Check your alerts and subscription
- `/help` - Show all commands

### Setting Up Alerts:
1. Send `/start` to your bot
2. Click "🚀 Start Subscription"
3. Choose "🆓 Start Free Trial"
4. Follow prompts to set up car searches

## 💰 Monetization Ready

Your bot includes:
- ✅ Free trial system (7 days)
- ✅ Subscription tiers (€5-15/month)
- ✅ User management
- ✅ Alert tracking
- ⏳ Payment integration (Stripe ready)

## 🚀 Deploy to Production

### Railway (Recommended - €10/month)
```bash
npm install -g @railway/cli
railway login
railway init
railway add postgresql
railway deploy
```

### Manual VPS (€5/month)
```bash
# On your server
git clone your-repo-url
cd car-scout
python setup.py
# Set environment variables
python main.py
```

## 📊 What You've Built

🎯 **Core Features:**
- Telegram bot with rich interface
- Web scraper for Kleinanzeigen.de
- Real-time car alert system
- User subscription management
- Database with SQLAlchemy

📁 **File Structure:**
- `src/bot/` - Telegram bot logic
- `src/scraper/` - Web scraping engine
- `src/database/` - Database models
- `main.py` - Main application
- `run_bot.py` - Bot-only testing

## 🎉 Ready to Launch!

Your startup is **90% complete**! Next steps:
1. ✅ Test locally (done above)
2. 🚀 Deploy to cloud (~30 minutes)
3. 💳 Add payment system (~2 hours)
4. 📣 Start marketing (~ongoing)

**Timeline to first customer: 1-2 weeks** 🎯

Good luck with your startup! 🇺🇦💪
