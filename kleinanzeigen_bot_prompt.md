# Kleinanzeigen Car Search Telegram Bot - Development Prompt

You are an expert Python developer tasked with creating a sophisticated Telegram bot that searches for cars on Kleinanzeigen.de using web scraping techniques. This bot should provide users with a seamless experience for finding cars that match their specific criteria.

## Project Overview
Create a Telegram bot that allows users to search for cars on https://www.kleinanzeigen.de/s-autos/c216 with customizable filters, real-time notifications, and comprehensive car information display.

## Technical Stack Requirements
- **Language**: Python 3.8+
- **Bot Framework**: aiogram (latest version)
- **Web Scraping**: BeautifulSoup4 + requests
- **Database**: PostgreSQL with asyncpg
- **Additional**: asyncio for concurrent operations

## Core Features to Implement

### 1. User Interface Design
**Filter Configuration Menu:**
- Create intuitive inline keyboard menus for setting search parameters
- Implement parameter selection for:
  - Car brands and models
  - Year range (from/to)
  - Price range
  - Mileage range
  - Transmission type (Manual/Automatic)
  - Fuel type
  - Location radius
- Add functionality to paste pre-configured Kleinanzeigen URLs (e.g., `https://www.kleinanzeigen.de/s-autos/audi/c216+autos.marke_s:audi+autos.model_s:80`)
- Include "Save Filter" button after parameter selection

**Filter Management:**
- Display all saved filters with activate/deactivate toggles
- Show filter status (active/inactive) with visual indicators
- Allow editing and deletion of existing filters
- When activating a filter for the first time, populate "Recent Cars" with current matches

### 2. Data Presentation
**Car Listings Display:**
- Show cars published within the last 2 days in "Recent Cars" section
- Display car information in organized format:
  - Main car image (top view preferred)
  - Essential details matching filter criteria
  - Price with currency
  - Location and distance
  - Publication date
- Include "View on Website" button for each car
- Implement pagination for large result sets

**Car Detail View:**
- Comprehensive car profile with all available information
- Multiple images if available
- Detailed specifications
- Seller contact information (if available)
- Direct link to original listing

### 3. Web Scraping Implementation
**Parsing Engine:**
- Robust HTML parsing with error handling
- Support for dynamic content loading
- Implement retry mechanisms for failed requests
- Handle anti-bot measures (rate limiting, headers rotation)
- Process pagination automatically
- Extract and normalize all car data fields

**Data Management:**
- Parse and store all available filter options (brands, models, etc.)
- Implement data validation and cleaning
- Handle missing or malformed data gracefully
- Track price changes and notify users
- Remove outdated listings automatically

### 4. Database Schema
**Required Tables:**
```sql
-- Users table
users (user_id, username, first_name, created_at, is_active)

-- Search filters table
search_filters (id, user_id, name, parameters_json, is_active, created_at)

-- Cars table
cars (id, external_id, title, price, brand, model, year, mileage, location, url, images, details_json, first_seen, last_checked)

-- User notifications table
user_notifications (id, user_id, car_id, notification_type, sent_at)
```

### 5. Bot Workflow Implementation
**Command Structure:**
- `/start` - Welcome message and main menu
- `/filters` - Manage search filters
- `/recent` - View recent cars
- `/settings` - Bot preferences
- `/help` - Usage instructions

**Menu Navigation:**
- Main Menu → Filter Setup → Filter Management → Recent Cars
- Implement breadcrumb navigation
- Add "Back" and "Home" buttons consistently

### 6. Notification System
**Real-time Updates:**
- Check for new cars every 15-30 minutes
- Send notifications for new matches
- Price change alerts for existing cars
- Format notifications as compact car cards
- Allow users to configure notification preferences

### 7. Error Handling and Reliability
**Comprehensive Error Management:**
- Network connectivity issues
- Website structure changes
- Rate limiting responses
- Database connection failures
- Invalid user input
- Graceful degradation when services are unavailable

### 8. Payments
**Payment options:**
- Provide three options for payment processing services that offer subscription payments. Also provide a summary of why they would be a good option

**Logging and Monitoring:**
- Implement detailed logging for debugging
- Track parsing success rates
- Monitor bot performance metrics
- Set up health checks

## Development Guidelines

### Code Organization
- Use clean architecture principles
- Implement dependency injection
- Create separate modules for:
  - Bot handlers and keyboards
  - Web scraping logic
  - Database operations
  - Data models and schemas
  - Configuration management

### Performance Optimization
- Implement connection pooling for database
- Use caching for frequently accessed data
- Optimize database queries with proper indexing
- Implement concurrent processing for multiple users
- Rate limit requests to avoid blocking

### Security Considerations
- Validate all user inputs
- Implement request rate limiting
- Secure database connections
- Protect against SQL injection
- Handle sensitive data appropriately

## Deliverables Expected
1. Complete bot implementation with all specified features
2. Database setup scripts and migrations
3. Configuration files for deployment
4. Comprehensive error handling
5. Documentation for setup and usage
6. If you are not 90% sure on how to proceed, ask me some clarifying question

## Success Criteria
- Bot responds within 2 seconds to user interactions
- Successfully parses car data from Kleinanzeigen
- Handles at least 100 concurrent users
- Maintains 99% uptime
- Accurate filter matching and notifications
- User-friendly interface with intuitive navigation

## Additional Considerations
- Plan for potential website structure changes
- Implement fallback mechanisms for parsing failures
- Consider implementing data export functionality
- Add analytics for popular search terms
- Plan for scalability with increased user base

Begin development with a detailed analysis of the Kleinanzeigen website structure and create a robust foundation that can adapt to future changes.
