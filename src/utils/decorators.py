import time
from functools import wraps
from typing import Callable
from src.utils.errorHandler import ErrorHandler

def retry_on_failure(max_retries: int = 3, delay: int = 5):
    """Decorator to retry failed API calls"""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            error_handler = ErrorHandler()
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:  # Last attempt
                        error_handler.handle_api_error(e, func.__name__, attempt + 1)
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
