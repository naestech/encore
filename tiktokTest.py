import os
import time
import json
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')

# Initialize the Apify client
client = ApifyClient(APIFY_API_TOKEN)

def save_to_file(video_data, filename='tiktok_data.txt'):
    print("Saving to file:", video_data)  # Debugging: Print the data being saved
    with open(filename, 'a') as file:
        file.write(json.dumps(video_data) + '\n')
    print("Data written to file.")

def run_tiktok_extractor(query):
    actor_id = 'clockworks~free-tiktok-scraper'
    input_data = {
        "excludePinnedPosts": False,
        "resultsPerPage": 5,  # Limit to 5 videos for testing
        "searchQueries": [query],
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
        "shouldDownloadSubtitles": False,
        "shouldDownloadVideos": False
    }

    # Start the actor
    run = client.actor(actor_id).call(run_input=input_data)
    run_id = run['id']
    print(f'Actor started with run ID: {run_id}')

    # Polling to check the run status
    start_time = time.time()
    timeout = 600  # 10 minutes timeout

    while True:
        run_status = client.run(run_id).get()
        print(f'Current status: {run_status["status"]}')  # Log the current status

        if run_status['status'] in ['SUCCEEDED', 'FAILED', 'TIMEOUT']:
            break

        if time.time() - start_time > timeout:
            print('Timeout reached while waiting for actor to finish.')
            break

        time.sleep(15)  # Wait for 15 seconds before checking again

    if run_status['status'] == 'SUCCEEDED':
        dataset_id = run_status['defaultDatasetId']
        return fetch_dataset_items(dataset_id)
    else:
        print('Actor run failed, timed out, or did not start properly.')
        print(f'Final status: {run_status}')
        return None

def fetch_dataset_items(dataset_id):
    items = client.dataset(dataset_id).list_items()
    return items.items  # Access the items attribute of the ListPage object

if __name__ == '__main__':
    queries = ["sold out concert", "sold out show"]
    for query in queries:
        print(f'Fetching videos for query: "{query}"')
        results = run_tiktok_extractor(query)
        if results:
            for video_data in results:  # Process all videos
                print("Video Data:", video_data)  # Debugging: Print the video data structure
                video_info = {
                    'id': video_data['id'],
                    'username': video_data.get('authorMeta', {}).get('name', 'N/A'),
                    'post_content': video_data.get('text', 'N/A'),
                    'post_time': video_data.get('createTime', 'N/A'),
                    'video_url': video_data.get('webVideoUrl', 'N/A'),
                    'source': 'TikTok'
                }
                print("Formatted Video Data:", video_info)
                save_to_file(video_info)
        else:
            print("No results found or an error occurred.")

    print("Data extraction and insertion complete.")