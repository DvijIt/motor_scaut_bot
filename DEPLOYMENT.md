# 🚀 Car Scout Deployment Guide

This guide explains how to deploy your Car Scout bot to various cloud platforms.

## 🎯 Deployment Options

### 1. Railway (Recommended) 🚂
**Cost**: ~€10-15/month  
**Pros**: Easy setup, PostgreSQL included, automatic deployments

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add postgresql
railway deploy
```

**Environment Variables to Set:**
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://...  # Railway provides this
PRODUCTION=true
```

### 2. Heroku 🟣
**Cost**: ~€7-12/month  
**Pros**: Popular platform, good documentation

```bash
# Install Heroku CLI and deploy
heroku create car-scout-app
heroku addons:create heroku-postgresql:mini
heroku config:set TELEGRAM_BOT_TOKEN=your_token
git push heroku main
```

### 3. DigitalOcean App Platform 🌊
**Cost**: ~€12-20/month  
**Pros**: Good performance, managed database

1. Connect GitHub repository
2. Choose Python app
3. Add managed PostgreSQL database
4. Set environment variables
5. Deploy

### 4. VPS (Self-hosted) 💻
**Cost**: ~€5-10/month  
**Pros**: Full control, cheapest option

```bash
# On your VPS (Ubuntu/Debian)
git clone https://github.com/yourusername/car-scout.git
cd car-scout
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up systemd service
sudo cp car-scout.service /etc/systemd/system/
sudo systemctl enable car-scout
sudo systemctl start car-scout
```

## 📋 Pre-deployment Checklist

- [ ] Set up Telegram bot with @BotFather
- [ ] Configure environment variables
- [ ] Test locally with `python run_bot.py`
- [ ] Choose deployment platform
- [ ] Set up database (PostgreSQL recommended for production)
- [ ] Configure domain (optional but recommended)
- [ ] Set up monitoring/logging

## 🔐 Security

- Never commit `.env` file to git
- Use environment variables for all secrets
- Enable HTTPS for webhook mode (if using webhooks)
- Regularly update dependencies

## 📊 Monitoring

Add these tools for production monitoring:
- **Sentry** - Error tracking
- **Uptime Robot** - Service monitoring  
- **Railway/Heroku logs** - Application logs

## 💰 Cost Breakdown

| Service | Monthly Cost | Users Supported |
|---------|-------------|-----------------|
| Railway | €10-15 | 100-500 |
| Heroku | €7-12 | 50-300 |
| DigitalOcean | €12-20 | 200-1000 |
| VPS | €5-10 | 50-500 |

## 🚀 Quick Deploy to Railway

1. Fork this repository on GitHub
2. Connect to Railway: [railway.app](https://railway.app)
3. Select "Deploy from GitHub repo"
4. Add PostgreSQL service
5. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `PRODUCTION=true`
6. Deploy!

Your bot will be live in 2-3 minutes! 🎉
