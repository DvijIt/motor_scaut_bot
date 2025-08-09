# 🚗 Motor Scout Bot - Docker Development Setup

This guide will help you get the Motor Scout Bot running in Docker with just one command.

## 🚀 Quick Start (One Command Setup)

1. **Clone and enter the project directory:**
   ```bash
   git clone <your-repo-url>
   cd motor-scaut-bot
   ```

2. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your TELEGRAM_BOT_TOKEN
   ```

3. **Start everything with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

That's it! The bot should be running and connected to a PostgreSQL database.

## 📋 What's Included

The Docker setup includes:

- **Motor Scout Bot**: The main Telegram bot application
- **PostgreSQL Database**: For storing user data and car listings
- **PgAdmin** (optional): Web-based database management interface
- **Volume Mounts**: For persistent data and development hot-reload

## 🛠️ Development Features

### Hot Reload Development
The source code is mounted as a volume, so changes to Python files will be reflected immediately without rebuilding the container.

### Database Access
- **Internal**: The bot connects to `db:5432` inside Docker network
- **External**: Connect from your local machine using `localhost:5432`
  - Username: `postgres`
  - Password: `password`
  - Database: `motor_scout_db`

### PgAdmin (Optional)
Access the database GUI at: http://localhost:8080
- Email: `admin@motorscout.com`
- Password: `admin`

To start with PgAdmin:
```bash
docker-compose --profile admin up --build
```

## 📝 Environment Variables

Copy `env.example` to `.env` and configure:

```env
# Required: Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Development mode (recommended for local development)
DEVELOPMENT=true

# Database URL (automatically configured for Docker)
DATABASE_URL=postgresql://postgres:password@localhost:5432/motor_scout_db
```

## 🐳 Docker Commands

### Basic Operations
```bash
# Start services
docker-compose up

# Start with rebuild
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes (⚠️ deletes database data)
docker-compose down -v
```

### Development Commands
```bash
# View logs
docker-compose logs -f bot

# Access bot container shell
docker-compose exec bot bash

# Access database shell
docker-compose exec db psql -U postgres -d motor_scout_db

# Rebuild just the bot
docker-compose build bot
```

### Database Operations
```bash
# Reset database (⚠️ deletes all data)
docker-compose down -v
docker-compose up -d db
docker-compose up bot

# Backup database
docker-compose exec db pg_dump -U postgres motor_scout_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres motor_scout_db < backup.sql
```

## 🔧 Troubleshooting

### Bot won't start
1. Check if `TELEGRAM_BOT_TOKEN` is set in `.env`
2. Check logs: `docker-compose logs bot`
3. Ensure database is healthy: `docker-compose ps`

### Database connection issues
1. Wait for database to be ready (health check takes ~30 seconds)
2. Check database logs: `docker-compose logs db`
3. Verify database URL in `.env`

### Permission issues
- On Linux, you might need to fix file permissions:
  ```bash
  sudo chown -R $USER:$USER logs/ data/
  ```

### Port conflicts
If port 5432 or 8080 are already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use different external port
```

## 📁 Project Structure

```
motor-scaut-bot/
├── docker-compose.yml     # Multi-service Docker setup
├── Dockerfile            # Bot container definition
├── .env                  # Environment variables (create from env.example)
├── env.example           # Environment template
├── database/
│   └── init.sql          # Database initialization
├── src/                  # Source code (mounted for hot reload)
├── logs/                 # Application logs (persistent)
└── data/                 # Application data (persistent)
```

## 🔄 Development Workflow

1. **Make code changes** in `src/` directory
2. **Changes are automatically reflected** (no rebuild needed)
3. **Check logs** with `docker-compose logs -f bot`
4. **Test via Telegram** by messaging your bot
5. **Access database** via PgAdmin or command line

## 🚀 Production Deployment

For production, modify `docker-compose.yml`:
1. Set `DEVELOPMENT=false` and `PRODUCTION=true`
2. Use secure database credentials
3. Remove PgAdmin service
4. Configure proper logging and monitoring

## 📞 Support

If you encounter issues:
1. Check this README
2. Review Docker logs
3. Ensure all environment variables are set
4. Try rebuilding containers: `docker-compose up --build`
