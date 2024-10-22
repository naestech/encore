import os
import time
import sqlite3
from apify_client import ApifyClient
from dotenv import load_dotenv
from src.utils.errorHandler import ErrorHandler
from src.utils.decorators import retry_on_failure

class TikTokScraper:
    def __init__(self):
        load_dotenv()
        self.apiToken = os.getenv('APIFY_API_TOKEN')
        self.client = ApifyClient(self.apiToken)
        self.errorHandler = ErrorHandler()
        self.dbPath = 'data/tikTokData.db'

    @retry_on_failure(max_retries=3)
    def runTikTokExtractor(self, query):
        try:
            actorId = 'clockworks~free-tiktok-scraper'
            inputData = {
                "excludePinnedPosts": False,
                "resultsPerPage": 5,
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
            
            print("Inserting data:", formattedData)  # Debugging
            
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

if __name__ == '__main__':
    scraper = TikTokScraper()
    queries = ["sold out concert", "sold out show"]
    
    for query in queries:
        print(f'Fetching videos for query: "{query}"')
        results = scraper.runTikTokExtractor(query)
        
        if results:
            for videoData in results:
                print("Video Data:", videoData)  # Debugging
                scraper.saveToDatabase(videoData)
        else:
            print("No results found or an error occurred.")

    print("Data extraction and insertion complete.")
