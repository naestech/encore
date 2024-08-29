#uses ticketmaster's api to output sold out concerts

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# set up your api credentials and base url
consumer_key = os.getenv('TICKETMASTER_CONSUMER_KEY')
consumer_secret = os.getenv('TICKETMASTER_CONSUMER_SECRET')
base_url = 'https://app.ticketmaster.com/discovery/v2/'

print("starting script...")

# step 1: get all music events (concerts) in the us
query_params = {
    'countryCode': 'US',
    'classificationName': 'music',  # filter for music events
    'size': 5,  # limit to 5 events per page for testing purposes
    'locale': 'en-us'
}

# use pagination to get all events
events = []
page = 0

while True:
    query_params['page'] = page
    response = requests.get(f'{base_url}events', params=query_params, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print("response status code:", response.status_code)
    data = response.json()

    if '_embedded' not in data:
        print("no events found or issue with response.")
        break  # no more events or issue with the response
    
    events_fetched = data['_embedded']['events']
    events.extend(events_fetched)
    
    print(f"page {page}: fetched {len(events_fetched)} music events.")

    if page >= data['page']['totalPages'] - 1:
        print("reached the last page of events.")
        break
    
    page += 1

print(f"total music events fetched: {len(events)}")

# step 2: check each event for sold-out status
sold_out_events = []

for event in events:
    event_id = event['id']
    print(f"checking event: {event['name']} (id: {event_id})")

    event_response = requests.get(f'{base_url}events/{event_id}', auth=HTTPBasicAuth(consumer_key, consumer_secret))
    print("event response status:", event_response.status_code)
    event_data = event_response.json()
    
    # sometimes inventory info might not be present
    inventory = event_data.get('inventory', None)
    
    if inventory is None:
        print(f"no inventory info available for event: {event['name']}")
        continue  # skip this event

    remaining_tickets = inventory.get('remaining', 0)
    print(f"remaining tickets: {remaining_tickets}")

    if remaining_tickets == 0:
        sold_out_events.append({
            'name': event['name'],
            'date': event['dates']['start']['localDate'],
            'venue': event['_embedded']['venues'][0]['name'],
            'location': event['_embedded']['venues'][0]['city']['name']
        })

# step 3: print out the sold-out events
if sold_out_events:
    print(f"found {len(sold_out_events)} sold-out music events:")
    for sold_out_event in sold_out_events:
        print(f"{sold_out_event['name']} on {sold_out_event['date']} at {sold_out_event['venue']} in {sold_out_event['location']} is sold out.")
else:
    print("no sold-out music events found.")
