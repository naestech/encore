import sys
import requests
from bs4 import BeautifulSoup
from src.data.venueScraper import VenueScraper
from src.utils.errorHandler import ErrorHandler

def test_venue(url: str, verbose: bool = True):
    """Test scraping for a single venue"""
    scraper = VenueScraper()
    error_handler = ErrorHandler()
    
    try:
        print(f"\nTesting venue: {url}")
        print("1. Testing basic connection...")
        
        # Test with different headers and verify=False for SSL issues
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, verify=False)
        print(f"Status Code: {response.status_code}")
        
        if verbose:
            print("\nResponse Headers:")
            for key, value in response.headers.items():
                print(f"{key}: {value}")
        
        if response.status_code == 200:
            print("\n2. Testing HTML parsing...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Print the first few lines of HTML for debugging
            if verbose:
                print("\nFirst 200 characters of HTML:")
                print(response.text[:200])
            
            print("\n3. Testing data extraction...")
            shows = scraper.scrapeVenueData(url)
            
            if shows:
                print(f"\nFound {len(shows)} shows:")
                for show in shows:
                    print("\nShow Details:")
                    for key, value in show.items():
                        print(f"{key}: {value}")
            else:
                print("No shows found")
                
    except Exception as e:
        error_handler.handle_error(e, f"Venue Test - {url}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.utils.venueTest <venue_url>")
        sys.exit(1)
    
    test_venue(sys.argv[1])
