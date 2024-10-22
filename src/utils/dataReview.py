import sqlite3
import pandas as pd
from datetime import datetime, timedelta

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
    
    print("\nRecent TikTok Data:")
    print(tiktok_df.to_string())
    
    print("\nRecent Venue Data:")
    print(venue_df.to_string())
    
    # Close connections
    tiktok_conn.close()
    venue_conn.close()

if __name__ == "__main__":
    days = input("Enter number of days to review (default: 1): ") or 1
    review_recent_data(int(days))
