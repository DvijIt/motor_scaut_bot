"""
Database models for Car Scout application
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """User model for storing Telegram user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    subscription_type = Column(String(20), default='free_trial')  # free_trial, basic, pro, premium
    subscription_expires = Column(DateTime)
    is_active = Column(Boolean, default=True)
    notifications_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    searches = relationship("SearchAlert", back_populates="user")
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username='{self.username}')>"

class SearchAlert(Base):
    """Model for storing user's car search alerts"""
    __tablename__ = 'search_alerts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(200))  # User-friendly name for the search
    brand = Column(String(50))
    min_price = Column(Integer)
    max_price = Column(Integer)
    location = Column(String(100))
    radius = Column(Integer)  # Search radius in km
    min_year = Column(Integer)
    max_mileage = Column(Integer)
    keywords = Column(Text)  # Additional keywords to search for
    is_active = Column(Boolean, default=True)
    last_check = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="searches")
    sent_listings = relationship("SentListing", back_populates="search_alert")
    
    def __repr__(self):
        return f"<SearchAlert(id={self.id}, brand='{self.brand}', user_id={self.user_id})>"

class CarListing(Base):
    """Model for storing scraped car listings"""
    __tablename__ = 'car_listings'
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String(100), unique=True, nullable=False)  # Kleinanzeigen ID
    title = Column(String(500))
    price = Column(Integer)
    location = Column(String(200))
    date_posted = Column(String(100))  # Original date string from website
    description = Column(Text)
    url = Column(String(500))
    image_url = Column(String(500))
    mileage = Column(String(50))
    year = Column(String(10))
    fuel_type = Column(String(50))
    is_available = Column(Boolean, default=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sent_listings = relationship("SentListing", back_populates="car_listing")
    
    def __repr__(self):
        return f"<CarListing(external_id='{self.external_id}', title='{self.title[:50]}')>"

class SentListing(Base):
    """Track which listings have been sent to which users"""
    __tablename__ = 'sent_listings'
    
    id = Column(Integer, primary_key=True)
    search_alert_id = Column(Integer, ForeignKey('search_alerts.id'), nullable=False)
    car_listing_id = Column(Integer, ForeignKey('car_listings.id'), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    search_alert = relationship("SearchAlert", back_populates="sent_listings")
    car_listing = relationship("CarListing", back_populates="sent_listings")
    
    def __repr__(self):
        return f"<SentListing(search_alert_id={self.search_alert_id}, car_listing_id={self.car_listing_id})>"

class DatabaseManager:
    """Database connection and session management"""
    
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///./car_scout.db')
        
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
        
    def get_or_create_user(self, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> User:
        """Get existing user or create new one"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.telegram_id == telegram_id).first()
            
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            
            return user
        finally:
            session.close()
    
    def create_search_alert(self, user_id: int, **kwargs) -> SearchAlert:
        """Create new search alert"""
        session = self.get_session()
        try:
            search_alert = SearchAlert(user_id=user_id, **kwargs)
            session.add(search_alert)
            session.commit()
            session.refresh(search_alert)
            return search_alert
        finally:
            session.close()
    
    def get_active_search_alerts(self) -> list:
        """Get all active search alerts"""
        session = self.get_session()
        try:
            return session.query(SearchAlert).filter(SearchAlert.is_active == True).all()
        finally:
            session.close()
    
    def save_car_listing(self, listing_data: dict) -> CarListing:
        """Save or update car listing"""
        session = self.get_session()
        try:
            existing = session.query(CarListing).filter(
                CarListing.external_id == listing_data['external_id']
            ).first()
            
            if existing:
                # Update last_seen timestamp
                existing.last_seen = datetime.utcnow()
                session.commit()
                return existing
            else:
                # Create new listing
                listing = CarListing(**listing_data)
                session.add(listing)
                session.commit()
                session.refresh(listing)
                return listing
        finally:
            session.close()
    
    def mark_listing_sent(self, search_alert_id: int, car_listing_id: int):
        """Mark that a listing has been sent to a user"""
        session = self.get_session()
        try:
            sent_listing = SentListing(
                search_alert_id=search_alert_id,
                car_listing_id=car_listing_id
            )
            session.add(sent_listing)
            session.commit()
        finally:
            session.close()
    
    def has_been_sent(self, search_alert_id: int, car_listing_id: int) -> bool:
        """Check if listing has already been sent to user"""
        session = self.get_session()
        try:
            sent = session.query(SentListing).filter(
                SentListing.search_alert_id == search_alert_id,
                SentListing.car_listing_id == car_listing_id
            ).first()
            return sent is not None
        finally:
            session.close()

# Create global database manager instance
db_manager = DatabaseManager()
