import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Logger setup
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create loggers
error_logger = setup_logger('error_logger', 'logs/error.log', level=logging.ERROR)
info_logger = setup_logger('info_logger', 'logs/info.log', level=logging.INFO)
debug_logger = setup_logger('debug_logger', 'logs/debug.log', level=logging.DEBUG)

