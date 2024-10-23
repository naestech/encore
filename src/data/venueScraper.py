"""
Name: Nadine
Email: naestech@proton.me
Description: Script for scraping venue websites to collect information about sold-out shows. 
Processes HTML data to extract relevant show details.
"""

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
                    title_element = show.find('p', class_='fs-18 bold mb-12 title')
                    artist = title_element.find('a').get_text(strip=True) if title_element else 'Unknown Artist'
                    showData = {
                        'product_name': title_element.get_text(strip=True) if title_element else 'Unknown Show',
                        'artist': artist,
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

    def save_to_database(self, venue_data):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT,
                date TEXT,
                location TEXT,
                price TEXT,
                genre TEXT,
                tickets_link TEXT
            )
        ''')

        # Insert data
        for show in venue_data:
            cursor.execute('''
                INSERT INTO shows (artist, date, location, price, genre, tickets_link)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                show['artist'],
                show['date'],
                show['location'],
                show['price'],
                show['genre'],
                show['tickets_link']
            ))

        conn.commit()
        conn.close()
