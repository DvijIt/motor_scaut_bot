"""
Web scraper for Kleinanzeigen.de car listings
Respects robots.txt and implements proper delays
"""

import time
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from dataclasses import dataclass
from typing import List, Optional
import re

logger = logging.getLogger(__name__)

@dataclass
class CarListing:
    """Data class for car listing information"""
    id: str
    title: str
    price: int
    location: str
    date: str
    description: str
    url: str
    image_url: Optional[str] = None
    mileage: Optional[str] = None
    year: Optional[str] = None
    fuel_type: Optional[str] = None

class KleinanzeigenScraper:
    """Scraper for Kleinanzeigen.de car listings"""
    
    BASE_URL = "https://www.kleinanzeigen.de"
    CARS_SECTION = "/s-autos/c216"
    
    def __init__(self, delay_seconds: int = 3):
        """
        Initialize the scraper
        
        Args:
            delay_seconds: Delay between requests to be respectful
        """
        self.delay = delay_seconds
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def build_search_url(self, 
                        brand: Optional[str] = None,
                        min_price: Optional[int] = None,
                        max_price: Optional[int] = None,
                        location: Optional[str] = None,
                        radius: Optional[int] = None,
                        min_year: Optional[int] = None,
                        max_mileage: Optional[int] = None) -> str:
        """
        Build search URL with filters
        
        Args:
            brand: Car brand (e.g., 'bmw', 'audi', 'volkswagen')
            min_price: Minimum price in EUR
            max_price: Maximum price in EUR
            location: City or postal code
            radius: Search radius in km
            min_year: Minimum year of manufacture
            max_mileage: Maximum mileage in km
            
        Returns:
            Complete search URL
        """
        url = f"{self.BASE_URL}{self.CARS_SECTION}"
        params = []
        
        if brand:
            # Map common brands to their Kleinanzeigen category IDs
            brand_mapping = {
                'audi': 'c216l2705',
                'bmw': 'c216l2707', 
                'mercedes': 'c216l2715',
                'volkswagen': 'c216l2727',
                'vw': 'c216l2727',
                'opel': 'c216l2720',
                'ford': 'c216l2711',
                'toyota': 'c216l2725',
                'renault': 'c216l2722',
                'peugeot': 'c216l2721'
            }
            
            brand_lower = brand.lower()
            if brand_lower in brand_mapping:
                url = f"{self.BASE_URL}/s-autos/{brand_lower}/{brand_mapping[brand_lower]}"
        
        # Add price filters
        if min_price:
            params.append(f"priceFrom={min_price}")
        if max_price:
            params.append(f"priceTo={max_price}")
            
        # Add location filter
        if location:
            params.append(f"locationStr={location}")
        if radius:
            params.append(f"radius={radius}")
            
        # Add other filters
        if min_year:
            params.append(f"yearFrom={min_year}")
        if max_mileage:
            params.append(f"mileageTo={max_mileage}")
        
        # Sort by newest first
        params.append("sortingField=SORTING_DATE")
        
        if params:
            url += "?" + "&".join(params)
            
        return url
    
    def scrape_listings(self, search_url: str, max_pages: int = 3) -> List[CarListing]:
        """
        Scrape car listings from search results
        
        Args:
            search_url: URL to scrape
            max_pages: Maximum number of pages to scrape
            
        Returns:
            List of CarListing objects
        """
        listings = []
        
        for page in range(1, max_pages + 1):
            logger.info(f"Scraping page {page}")
            
            page_url = f"{search_url}&pageNum={page}" if page > 1 else search_url
            
            try:
                # Respectful delay
                time.sleep(self.delay)
                
                response = self.session.get(page_url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find listing containers
                article_elements = soup.find_all('article', class_='aditem')
                
                if not article_elements:
                    logger.info(f"No more listings found on page {page}")
                    break
                
                for article in article_elements:
                    listing = self._parse_listing(article)
                    if listing:
                        listings.append(listing)
                
                logger.info(f"Found {len(article_elements)} listings on page {page}")
                
            except requests.RequestException as e:
                logger.error(f"Error scraping page {page}: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error on page {page}: {e}")
                break
        
        logger.info(f"Total listings scraped: {len(listings)}")
        return listings
    
    def _parse_listing(self, article) -> Optional[CarListing]:
        """
        Parse a single listing from HTML element
        
        Args:
            article: BeautifulSoup article element
            
        Returns:
            CarListing object or None if parsing fails
        """
        try:
            # Get listing ID
            listing_id = article.get('data-adid', '')
            
            # Get title and URL
            title_element = article.find('h2', class_='text-module-begin')
            if not title_element:
                return None
                
            title_link = title_element.find('a')
            if not title_link:
                return None
                
            title = title_link.get_text(strip=True)
            relative_url = title_link.get('href', '')
            full_url = urljoin(self.BASE_URL, relative_url)
            
            # Get price
            price_element = article.find('p', class_='aditem-main--middle--price-shipping--price')
            price = 0
            if price_element:
                price_text = price_element.get_text(strip=True)
                # Extract numeric price
                price_match = re.search(r'(\\d{1,3}(?:\\.\\d{3})*)', price_text.replace('.', ''))
                if price_match:
                    price = int(price_match.group(1).replace('.', ''))
            
            # Get location
            location_element = article.find('div', class_='aditem-main--top--left')
            location = "Unknown"
            if location_element:
                location_text = location_element.get_text(strip=True)
                # Location is typically after the date
                location_parts = location_text.split('\\n')
                if len(location_parts) > 1:
                    location = location_parts[-1].strip()
            
            # Get date
            date_element = article.find('div', class_='aditem-main--top--right')
            date = "Unknown"
            if date_element:
                date = date_element.get_text(strip=True)
            
            # Get description (if available in listing preview)
            description_element = article.find('p', class_='aditem-main--middle--description')
            description = ""
            if description_element:
                description = description_element.get_text(strip=True)
            
            # Get image URL
            image_element = article.find('img')
            image_url = None
            if image_element:
                image_url = image_element.get('src') or image_element.get('data-src')
                if image_url and not image_url.startswith('http'):
                    image_url = urljoin(self.BASE_URL, image_url)
            
            # Parse additional details from title/description
            mileage = self._extract_mileage(title + " " + description)
            year = self._extract_year(title + " " + description)
            fuel_type = self._extract_fuel_type(title + " " + description)
            
            return CarListing(
                id=listing_id,
                title=title,
                price=price,
                location=location,
                date=date,
                description=description,
                url=full_url,
                image_url=image_url,
                mileage=mileage,
                year=year,
                fuel_type=fuel_type
            )
            
        except Exception as e:
            logger.error(f"Error parsing listing: {e}")
            return None
    
    def _extract_mileage(self, text: str) -> Optional[str]:
        """Extract mileage from text"""
        # Look for patterns like "120.000 km", "120000km", "120k km"
        patterns = [
            r'(\\d{1,3}(?:\\.\\d{3})*)\\s*km',
            r'(\\d{1,3})k\\s*km',
            r'(\\d{3,6})\\s*km'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _extract_year(self, text: str) -> Optional[str]:
        """Extract year from text"""
        # Look for 4-digit years from 1980 to current year + 1
        import datetime
        current_year = datetime.datetime.now().year
        pattern = r'\\b(19[8-9]\\d|20[0-2]\\d)\\b'
        
        match = re.search(pattern, text)
        if match:
            year = int(match.group(1))
            if 1980 <= year <= current_year + 1:
                return str(year)
        return None
    
    def _extract_fuel_type(self, text: str) -> Optional[str]:
        """Extract fuel type from text"""
        fuel_types = [
            'benzin', 'diesel', 'elektro', 'hybrid', 'lpg', 'cng', 'erdgas'
        ]
        
        text_lower = text.lower()
        for fuel_type in fuel_types:
            if fuel_type in text_lower:
                return fuel_type.capitalize()
        return None
    
    def get_detailed_listing(self, listing_url: str) -> Optional[dict]:
        """
        Get detailed information from a specific listing page
        
        Args:
            listing_url: URL of the specific listing
            
        Returns:
            Dictionary with detailed listing information
        """
        try:
            time.sleep(self.delay)
            
            response = self.session.get(listing_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {}
            
            # Get full description
            description_element = soup.find('p', id='viewad-description-text')
            if description_element:
                details['full_description'] = description_element.get_text(strip=True)
            
            # Get seller information
            seller_element = soup.find('div', id='viewad-contact')
            if seller_element:
                seller_name = seller_element.find('span', class_='iconlist-text')
                if seller_name:
                    details['seller_name'] = seller_name.get_text(strip=True)
            
            # Get additional images
            image_elements = soup.find_all('img', class_='galleryimage-element')
            if image_elements:
                details['image_urls'] = [
                    urljoin(self.BASE_URL, img.get('src', ''))
                    for img in image_elements
                ]
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting detailed listing from {listing_url}: {e}")
            return None

def main():
    """Test the scraper"""
    scraper = KleinanzeigenScraper(delay_seconds=2)
    
    # Test search for BMW cars under 20000€ in Munich
    search_url = scraper.build_search_url(
        brand='bmw',
        max_price=20000,
        location='München',
        radius=50
    )
    
    print(f"Search URL: {search_url}")
    
    listings = scraper.scrape_listings(search_url, max_pages=1)
    
    print(f"\\nFound {len(listings)} listings:")
    for i, listing in enumerate(listings[:5], 1):  # Show first 5
        print(f"\\n{i}. {listing.title}")
        print(f"   Price: €{listing.price:,}")
        print(f"   Location: {listing.location}")
        print(f"   Date: {listing.date}")
        print(f"   URL: {listing.url}")
        if listing.mileage:
            print(f"   Mileage: {listing.mileage}")
        if listing.year:
            print(f"   Year: {listing.year}")

if __name__ == "__main__":
    main()
