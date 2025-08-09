# 🖥️ VPS Setup Guide for Car Scout Bot

Complete guide to deploy your bot on a VPS (Recommended: Hetzner)

## 🎯 Best VPS Choice: Hetzner Cloud

### Why Hetzner?
- **Location**: Frankfurt, Germany (perfect for targeting German customers)
- **Price**: €3.29/month for CX11 (1 vCPU, 2GB RAM, 20GB SSD)
- **Network**: Excellent connectivity to German websites
- **GDPR**: Compliant for EU customers
- **Support**: Good documentation and support

## 📋 Step-by-Step VPS Setup

### Step 1: Create Hetzner Account
1. Go to [hetzner.com](https://www.hetzner.com/cloud)
2. Sign up (accepts international cards)
3. Verify your account

### Step 2: Create Server
1. **Server Type**: CX11 (€3.29/month)
2. **Location**: Falkenstein or Frankfurt (both in Germany)
3. **Image**: Ubuntu 22.04 LTS
4. **SSH Key**: Add your SSH public key
5. **Name**: car-scout-bot
6. Click "Create & Buy"

### Step 3: Connect to Your Server
```bash
# SSH into your server (replace IP with yours)
ssh root@YOUR_SERVER_IP

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install python3 python3-pip python3-venv git postgresql postgresql-contrib nginx -y
```

### Step 4: Setup Application
```bash
# Clone your repository
git clone https://github.com/DvijIt/motor_scaut_bot.git
cd motor_scaut_bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Setup Database
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE carscout;
CREATE USER botuser WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE carscout TO botuser;
\q
```

### Step 6: Configure Environment
```bash
# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://botuser:your_secure_password@localhost/carscout
PRODUCTION=true
HOST=0.0.0.0
PORT=8000
EOF
```

### Step 7: Setup Systemd Service
```bash
# Create service file
cat > /etc/systemd/system/car-scout.service << EOF
[Unit]
Description=Car Scout Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/motor_scaut_bot
Environment=PATH=/root/motor_scaut_bot/venv/bin
ExecStart=/root/motor_scaut_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable car-scout
systemctl start car-scout

# Check status
systemctl status car-scout
```

### Step 8: Setup Nginx (Optional - for webhooks)
```bash
# Create nginx config
cat > /etc/nginx/sites-available/car-scout << EOF
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/car-scout /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 9: Setup Firewall
```bash
# Configure UFW firewall
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## 🔧 Management Commands

```bash
# Check bot status
systemctl status car-scout

# View logs
journalctl -u car-scout -f

# Restart bot
systemctl restart car-scout

# Update code
cd /root/motor_scaut_bot
git pull
systemctl restart car-scout

# Monitor resources
htop
df -h
free -h
```

## 💰 Alternative VPS Providers

### DigitalOcean (Frankfurt)
- **Price**: $4/month
- **Specs**: 1GB RAM, 25GB SSD
- **Bonus**: $200 credit for new users
- **Setup**: Similar to Hetzner

### Vultr (Frankfurt)
- **Price**: $3.50/month  
- **Specs**: 1GB RAM, 25GB SSD
- **Good**: Fast deployment

### OVH (France)
- **Price**: €3.50/month
- **Specs**: 2GB RAM, 20GB SSD
- **Location**: Closer to Germany

## 🎯 Total Monthly Costs

| Component | Hetzner | DigitalOcean | Vultr |
|-----------|---------|--------------|--------|
| VPS | €3.29 | €3.70 | €3.20 |
| Domain (optional) | €1 | €1 | €1 |
| **Total** | **€4.29** | **€4.70** | **€4.20** |

## 🚀 Why VPS vs Free Hosting?

| Feature | VPS | Free Hosting |
|---------|-----|--------------|
| **Uptime** | 99.9% | 99% (sleeps) |
| **Performance** | Dedicated resources | Shared/limited |
| **Control** | Full root access | Limited |
| **Scalability** | Easy to upgrade | Limited |
| **Cost** | €3-5/month | Free |

## 🎯 Recommendation

**Start with**: Hetzner CX11 (€3.29/month)
**Upgrade to**: CX21 (€5.83/month) when you get 50+ users
**Scale to**: Multiple servers when you get 500+ users

Your bot will be lightning fast for German customers! 🇩🇪⚡
