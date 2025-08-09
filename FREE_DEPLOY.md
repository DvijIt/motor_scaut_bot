# 🆓 FREE Deployment Guide

Deploy your Car Scout bot completely FREE using Render!

## 🚀 Render Free Deployment (Recommended)

### Step 1: Prepare Your Code
```bash
# Make sure your code is ready
git init
git add .
git commit -m "Initial commit"

# Push to GitHub (free account)
# Create new repo on github.com
git remote add origin https://github.com/yourusername/car-scout.git
git push -u origin main
```

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub (free)
3. Connect your GitHub repository

### Step 3: Deploy Bot
1. Click "New +" → "Web Service"
2. Connect your car-scout repository
3. Configure:
   - **Name**: `car-scout-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free

### Step 4: Add Database
1. Go to Dashboard → "New +" → "PostgreSQL"
2. **Name**: `car-scout-db`
3. **Plan**: Free
4. Copy the "Internal Database URL"

### Step 5: Set Environment Variables
In your web service settings, add:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://... (from step 4)
PRODUCTION=true
```

### Step 6: Deploy!
Click "Deploy" - your bot will be live in 3-5 minutes! 🎉

## 🆓 Alternative: Local + ngrok (For Testing)

Run locally but accessible worldwide:

```bash
# Install ngrok (free)
brew install ngrok  # macOS
# or download from ngrok.com

# Run your bot locally
python main.py &

# Expose to internet (free 2 hours sessions)
ngrok http 8000
```

## 💰 Free Tier Limits

| Platform | Free Hours | Database | Bandwidth | Sleep? |
|----------|------------|----------|-----------|---------|
| Render | 750/month | 1GB PostgreSQL | 100GB | After 15min idle |
| Railway | $5 credit | Included | Limited | No |
| PythonAnywhere | 24/month | Limited MySQL | 3GB | No |
| ngrok | 2h sessions | None | Unlimited | Manual restart |

## 🎯 Best FREE Strategy

### Phase 1: Development (Free)
- Local development: `python run_bot.py`
- Test with ngrok for external access
- Perfect for initial testing

### Phase 2: MVP Launch (Free)
- Deploy to Render (750 hours = 24/7 for 31 days)
- Free PostgreSQL database
- Test with real users

### Phase 3: Growth (€10-15/month)
- Upgrade to paid plan when you get customers
- Revenue should cover hosting costs quickly

## 🚀 Quick Start (5 minutes)

```bash
# 1. Upload to GitHub
git init
git add .
git commit -m "Car Scout Bot"
# Push to your GitHub repo

# 2. Deploy to Render
# - Go to render.com
# - Connect GitHub repo
# - Deploy!

# 3. Add bot token in Render dashboard
# 4. Your bot is LIVE! 🎉
```

## 💡 Pro Tips for FREE Usage

1. **Optimize for free limits**:
   - Check cars every 15-30 minutes (not every minute)
   - Use efficient database queries
   - Limit to 50-100 active users on free tier

2. **Prevent sleeping**:
   - Add a simple health check endpoint
   - Use UptimeRobot (free) to ping your service

3. **Monitor usage**:
   - Check Render dashboard for resource usage
   - Upgrade before hitting limits

Your car alert service can run completely FREE until you get paying customers! 🎯
