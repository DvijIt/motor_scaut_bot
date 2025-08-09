#!/usr/bin/env python3
"""
Test script for the Kleinanzeigen scraper
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.scraper.kleinanzeigen_scraper import KleinanzeigenScraper

def test_scraper():
    """Test the scraper functionality"""
    print("🔍 Testing Kleinanzeigen.de scraper...")
    
    scraper = KleinanzeigenScraper(delay_seconds=2)
    
    # Test different search scenarios
    test_cases = [
        {
            'name': 'BMW cars under €15,000 in Munich',
            'params': {
                'brand': 'bmw',
                'max_price': 15000,
                'location': 'München',
                'radius': 30
            }
        },
        {
            'name': 'Audi cars €10,000-€25,000',
            'params': {
                'brand': 'audi',
                'min_price': 10000,
                'max_price': 25000
            }
        },
        {
            'name': 'VW cars newer than 2015',
            'params': {
                'brand': 'volkswagen',
                'min_year': 2015
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"🎯 Test: {test_case['name']}")
        print('='*60)
        
        # Build search URL
        search_url = scraper.build_search_url(**test_case['params'])
        print(f"🔗 Search URL: {search_url}")
        
        # Scrape listings
        try:
            listings = scraper.scrape_listings(search_url, max_pages=1)
            print(f"✅ Found {len(listings)} listings")
            
            # Show first few listings
            for i, listing in enumerate(listings[:3], 1):
                print(f"\n{i}. {listing.title}")
                print(f"   💰 Price: €{listing.price:,}")
                print(f"   📍 Location: {listing.location}")
                print(f"   📅 Date: {listing.date}")
                if listing.mileage:
                    print(f"   🛣️ Mileage: {listing.mileage}")
                if listing.year:
                    print(f"   📅 Year: {listing.year}")
                print(f"   🔗 URL: {listing.url}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main test function"""
    try:
        test_scraper()
        print("\n✅ Scraper test completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    main()
