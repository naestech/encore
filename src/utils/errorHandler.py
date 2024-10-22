import logging
from datetime import datetime

class DataCollectionError(Exception):
    """Custom exception for data collection errors"""
    pass

class ErrorHandler:
    def __init__(self, logFile: str = "errorLogs.txt"):
        # Set up logging
        logging.basicConfig(
            filename=logFile,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, source: str) -> None:
        """Handle general errors"""
        error_msg = f"Error in {source}: {str(error)}"
        self.logger.error(error_msg)
        raise DataCollectionError(error_msg)

    def handle_api_error(self, error: Exception, source: str, retry_count: int = None) -> None:
        """Handle API-related errors"""
        error_msg = f"API Error from {source}: {str(error)}"
        if retry_count is not None:
            error_msg += f" (Attempt {retry_count})"
        
        self.logger.error(error_msg)
        raise DataCollectionError(error_msg)

    def handle_scraping_error(self, error: Exception, url: str) -> None:
        """Handle web scraping errors"""
        error_msg = f"Scraping Error for {url}: {str(error)}"
        self.logger.error(error_msg)
        raise DataCollectionError(error_msg)
