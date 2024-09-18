import sqlite3
import json

# Define the path to the text file and the database file
text_file_path = 'tiktok_data.txt'
database_file_path = 'tiktok_data.db'

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_file_path)
cursor = conn.cursor()

# Create the table if it doesn't exist
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
conn.commit()

# Read the JSON lines from the text file and insert them into the database
with open(text_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        video_data = json.loads(line.strip())
        print("Inserting data:", video_data)  # Debugging: Print the data being inserted
        cursor.execute('''
            INSERT OR IGNORE INTO videos (id, username, post_content, post_time, video_url, source)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            video_data['id'],
            video_data['username'],
            video_data['post_content'],
            video_data['post_time'],
            video_data['video_url'],
            video_data['source']
        ))
        conn.commit()

# Close the database connection
conn.close()

print("Data has been successfully inserted into the database.")
