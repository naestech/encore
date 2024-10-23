"""
Name: Nadine
Email: naestech@proton.me
Description: Script for scraping TikTok data related to sold-out concerts and shows. 
Uses the Apify API to extract relevant TikTok posts and saves them to a database.
"""

import os
import time
import sqlite3
from apify_client import ApifyClient
from dotenv import load_dotenv
from src.utils.errorHandler import ErrorHandler
from src.utils.decorators import retry_on_failure
from src.utils.logger import info_logger, error_logger, debug_logger

class TikTokScraper:
    def __init__(self):
        load_dotenv()
        self.apiToken = os.getenv('APIFY_API_TOKEN')
        self.client = ApifyClient(self.apiToken)
        self.errorHandler = ErrorHandler()
        self.dbPath = 'data/tiktokData.db'

    @retry_on_failure(max_retries=3)
    def runTikTokExtractor(self, query):
        try:
            actorId = 'clockworks~free-tiktok-scraper'
            inputData = {
                "excludePinnedPosts": False,
                "resultsPerPage": 1,
                "searchQueries": [query],
                "shouldDownloadCovers": False,
                "shouldDownloadSlideshowImages": False,
                "shouldDownloadSubtitles": False,
                "shouldDownloadVideos": False
            }

            run = self.client.actor(actorId).call(run_input=inputData)
            return self._processRun(run)
        except Exception as e:
            self.errorHandler.handle_api_error(e, f"TikTok API - {query}")

    def _processRun(self, run):
        try:
            datasetId = run['defaultDatasetId']
            items = self.client.dataset(datasetId).list_items()
            return items.items
        except Exception as e:
            self.errorHandler.handle_api_error(e, "TikTok Dataset Processing")

    def saveToDatabase(self, videoData):
        try:
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                username TEXT,
                post_content TEXT,
                post_time INTEGER,
                video_url TEXT,
                source TEXT
            )
            ''')
            
            # Format the video data
            formattedData = {
                'id': videoData['id'],
                'username': videoData.get('authorMeta', {}).get('name', 'N/A'),
                'post_content': videoData.get('text', 'N/A'),
                'post_time': videoData.get('createTime', 'N/A'),
                'video_url': videoData.get('webVideoUrl', 'N/A'),
                'source': 'TikTok'
            }
            
            debug_logger.debug(f"Inserting data: {formattedData}")
            
            cursor.execute('''
                INSERT OR IGNORE INTO videos (id, username, post_content, post_time, video_url, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                formattedData['id'],
                formattedData['username'],
                formattedData['post_content'],
                formattedData['post_time'],
                formattedData['video_url'],
                formattedData['source']
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            self.errorHandler.handle_api_error(e, "Database Operation")

    def clean_tiktok_data(self, tiktok_data):
        cleaned_data = []
        for post in tiktok_data:
            if self._is_relevant(post['post_content']):
                cleaned_post = {
                    'username': post['username'],
                    'post_content': self._sanitize_content(post['post_content']),
                    'post_time': post['post_time'],
                    'video_url': post['video_url']
                }
                cleaned_data.append(cleaned_post)
        return cleaned_data

    def _is_relevant(self, content):
        keywords = ['sold out', 'concert', 'show', 'tour']
        return any(keyword in content.lower() for keyword in keywords)

    def _sanitize_content(self, content):
        # Remove any potentially problematic characters or shorten if too long
        return content[:200] if len(content) > 200 else content

if __name__ == '__main__':
    scraper = TikTokScraper()
    queries = ["sold out concert", "sold out show"]
    
    for query in queries:
        info_logger.info(f'Fetching videos for query: "{query}"')
        results = scraper.runTikTokExtractor(query)
        
        if results:
            for videoData in results:
                debug_logger.debug(f"Video Data: {videoData}")
                scraper.saveToDatabase(videoData)
        else:
            info_logger.info("No results found or an error occurred.")

    info_logger.info("Data extraction and insertion complete.")
