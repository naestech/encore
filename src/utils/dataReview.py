"""
Name: Nadine
Email: naestech@proton.me
Description: Utility script to review recent data collected from TikTok and venues. 
Allows querying and displaying data from a specified number of days back.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from src.utils.logger import info_logger, error_logger, debug_logger

def review_recent_data(days_back=1):
    """Review data collected in the last N days"""
    # Connect to databases
    tiktok_conn = sqlite3.connect('data/tikTokData.db')
    venue_conn = sqlite3.connect('data/encore.db')
    
    # Get recent TikTok data
    tiktok_df = pd.read_sql_query("""
        SELECT * FROM videos 
        WHERE post_time > ?
    """, tiktok_conn, params=[int((datetime.now() - timedelta(days=days_back)).timestamp())])
    
    # Get recent venue data
    venue_df = pd.read_sql_query("""
        SELECT * FROM shows 
        WHERE date > date('now', ?)
    """, venue_conn, params=[f'-{days_back} days'])
    
    info_logger.info("\nRecent TikTok Data:")
    info_logger.info(tiktok_df.to_string())
    
    info_logger.info("\nRecent Venue Data:")
    info_logger.info(venue_df.to_string())
    
    # Close connections
    tiktok_conn.close()
    venue_conn.close()

if __name__ == "__main__":
    days = input("Enter number of days to review (default: 1): ") or 1
    review_recent_data(int(days))
