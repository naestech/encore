import logging
from datetime import datetime
from src.utils.logger import error_logger

class DataCollectionError(Exception):
    """Custom exception for data collection errors"""
    pass

class ErrorHandler:
    @staticmethod
    def handle_error(e, context):
        error_logger.error(f"Error in {context}: {str(e)}", exc_info=True)

    @staticmethod
    def handle_api_error(e, api_name):
        error_logger.error(f"API Error in {api_name}: {str(e)}", exc_info=True)

    @staticmethod
    def handle_scraping_error(e, url):
        error_logger.error(f"Scraping Error for URL {url}: {str(e)}", exc_info=True)
