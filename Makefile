# Motor Scout Bot - Development Makefile
# Use: make <command>

.PHONY: help setup start stop restart logs shell db-shell clean rebuild test

# Default target
help:
	@echo "🚗 Motor Scout Bot - Available Commands:"
	@echo ""
	@echo "  🚀 Quick Start:"
	@echo "    make setup     - Set up environment and start everything"
	@echo "    make start     - Start all services"
	@echo "    make stop      - Stop all services"
	@echo ""
	@echo "  🛠️  Development:"
	@echo "    make logs      - Show bot logs"
	@echo "    make shell     - Access bot container shell"
	@echo "    make restart   - Restart bot service"
	@echo "    make rebuild   - Rebuild and restart all services"
	@echo ""
	@echo "  🗄️  Database:"
	@echo "    make db-shell  - Access database shell"
	@echo "    make db-admin  - Start with PgAdmin interface"
	@echo "    make db-reset  - Reset database (⚠️  deletes all data)"
	@echo ""
	@echo "  🧹 Cleanup:"
	@echo "    make clean     - Stop and remove containers"
	@echo "    make clean-all - Stop and remove everything including volumes"

# Setup environment and start services
setup:
	@echo "🔧 Setting up Motor Scout Bot..."
	@if [ ! -f .env ]; then \
		echo "📋 Creating .env file from template..."; \
		cp env.example .env; \
		echo "⚠️  Please edit .env and add your TELEGRAM_BOT_TOKEN"; \
		echo "📝 Then run: make start"; \
	else \
		echo "✅ .env file already exists"; \
		echo "🚀 Starting services..."; \
		docker-compose up --build -d; \
		echo "🎉 Services started! Check logs with: make logs"; \
	fi

# Start services
start:
	@echo "🚀 Starting Motor Scout Bot services..."
	docker-compose up -d
	@echo "✅ Services started! Use 'make logs' to view output"

# Stop services
stop:
	@echo "🛑 Stopping Motor Scout Bot services..."
	docker-compose down
	@echo "✅ Services stopped"

# Restart just the bot service
restart:
	@echo "🔄 Restarting bot service..."
	docker-compose restart bot
	@echo "✅ Bot restarted"

# Show logs
logs:
	@echo "📋 Showing bot logs (Ctrl+C to exit)..."
	docker-compose logs -f bot

# Access bot container shell
shell:
	@echo "🐚 Accessing bot container shell..."
	docker-compose exec bot bash

# Access database shell
db-shell:
	@echo "🗄️  Accessing database shell..."
	docker-compose exec db psql -U postgres -d motor_scout_db

# Start with PgAdmin
db-admin:
	@echo "🗄️  Starting services with PgAdmin..."
	docker-compose --profile admin up -d
	@echo "🌐 PgAdmin available at: http://localhost:8080"
	@echo "📧 Email: admin@motorscout.com"
	@echo "🔑 Password: admin"

# Reset database
db-reset:
	@echo "⚠️  This will delete ALL database data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "🗄️  Resetting database..."
	docker-compose down
	docker volume rm motor-scaut-bot_postgres_data 2>/dev/null || true
	docker-compose up -d
	@echo "✅ Database reset complete"

# Clean up containers
clean:
	@echo "🧹 Cleaning up containers..."
	docker-compose down --remove-orphans
	@echo "✅ Containers cleaned"

# Clean up everything including volumes
clean-all:
	@echo "⚠️  This will delete ALL data including database!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	@echo "🧹 Cleaning up everything..."
	docker-compose down -v --remove-orphans
	docker system prune -f
	@echo "✅ Everything cleaned"

# Rebuild everything
rebuild:
	@echo "🔨 Rebuilding all services..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ Rebuild complete"

# Test the setup
test:
	@echo "🧪 Testing setup..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file missing. Run 'make setup' first"; \
		exit 1; \
	fi
	@if ! docker-compose ps | grep -q "Up"; then \
		echo "❌ Services not running. Run 'make start' first"; \
		exit 1; \
	fi
	@echo "✅ Basic setup looks good!"
	@echo "📋 Check logs with: make logs"

# Development shortcuts
dev: start logs
prod: setup
