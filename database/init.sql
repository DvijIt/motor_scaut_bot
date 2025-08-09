-- Motor Scout Bot Database Initialization Script
-- This script is automatically executed when the PostgreSQL container starts

-- Create database if it doesn't exist (this line might be redundant since Docker creates the DB)
-- CREATE DATABASE IF NOT EXISTS motor_scout_db;

-- Set timezone to UTC
SET timezone = 'UTC';

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Note: The actual tables are created by SQLAlchemy in the Python application
-- This file can be used for additional database setup like:
-- - Creating indexes
-- - Setting up roles and permissions
-- - Inserting initial data

-- Example: Create index for faster lookups (uncomment if needed)
-- CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
-- CREATE INDEX IF NOT EXISTS idx_car_listings_external_id ON car_listings(external_id);
-- CREATE INDEX IF NOT EXISTS idx_search_alerts_user_id ON search_alerts(user_id);

-- Insert default data (uncomment and modify as needed)
-- INSERT INTO users (telegram_id, username, first_name, subscription_type, is_active, notifications_enabled)
-- VALUES (123456789, 'test_user', 'Test', 'free_trial', true, true)
-- ON CONFLICT (telegram_id) DO NOTHING;

COMMIT;
