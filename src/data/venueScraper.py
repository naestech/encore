import requests
from bs4 import BeautifulSoup
from src.utils.errorHandler import ErrorHandler
from src.utils.decorators import retry_on_failure
import sqlite3

class VenueScraper:
    def __init__(self):
        self.errorHandler = ErrorHandler()
        self.dbPath = 'data/encore.db'

    @retry_on_failure(max_retries=3)
    def scrapeVenueData(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return self._processVenueData(soup, url)
        except Exception as e:
            self.errorHandler.handle_scraping_error(e, url)

    def _processVenueData(self, soup, url):
        try:
            soldOutShows = []
            soldOutItems = soup.find_all('a', class_='seetickets-buy-btn', 
                                       string=lambda text: text and 'sold out' in text.lower())

            for item in soldOutItems:
                show = item.find_parent('div', class_='mdc-card')
                if show:
                    showData = {
                        'product_name': show.find('p', class_='fs-18 bold mb-12 title').get_text(strip=True),
                        'artist': show.find('a', href=True).get_text(strip=True),
                        'date': show.find('p', class_='fs-18 bold mt-1r date').get_text(strip=True),
                        'location': show.find('p', class_='fs-12 venue').get_text(strip=True).replace('at ', ''),
                        'price': show.find('p', class_='fs-12 ages-price').get_text(strip=True),
                        'genre': show.find('p', class_='fs-12 genre').get_text(strip=True),
                        'tickets_link': item['href']
                    }
                    soldOutShows.append(showData)

            return soldOutShows
        except Exception as e:
            self.errorHandler.handle_scraping_error(e, url)
            return []

    def saveToDatabase(self, venueData):
        try:
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            # Your database insertion logic here
            conn.close()
        except Exception as e:
            self.errorHandler.handle_api_error(e, "Database Operation")
