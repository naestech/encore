import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up your API credentials and base URL
consumer_key = os.getenv('TICKETMASTER_CONSUMER_KEY')
consumer_secret = os.getenv('TICKETMASTER_CONSUMER_SECRET')
base_url = 'https://app.ticketmaster.com/discovery/v2/'

def test_ticketmaster_api():
    query_params = {
        'apikey': consumer_key,
        'countryCode': 'US',
        'classificationName': 'music',
        'size': 1  # Limit to 1 event for testing purposes
    }

    response = requests.get(f'{base_url}events', params=query_params)
    print("Response status code:", response.status_code)
    print("Response content:", response.json())

if __name__ == "__main__":
    test_ticketmaster_api()