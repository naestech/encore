#scrapes troubadour's website to output sold out events

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# Navigate to the Troubadour website
driver.get("https://troubadour.com/")

# Wait until the page is fully loaded
wait = WebDriverWait(driver, 20)  # Increased wait time
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the body tag to ensure the page is loaded

# Wait until the featured events are loaded
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "seetickets-list-event-container")))

# Find all the featured events
events = driver.find_elements(By.CLASS_NAME, "seetickets-list-event-container")

sold_out_events = []

# Iterate through the events to find which ones are sold out
for event in events:
    try:
        # Get the text of the link/button that typically says "Tickets" or "Sold Out"
        ticket_status = event.find_element(By.CLASS_NAME, "seetickets-buy-btn").text.strip()

        if "sold out" in ticket_status.lower():
            # Extracting event details
            title = event.find_element(By.CLASS_NAME, "title").text.strip()
            date = event.find_element(By.CLASS_NAME, "date").text.strip()
            headliners = event.find_element(By.CLASS_NAME, "headliners").text.strip()
            supporting_talent = event.find_element(By.CLASS_NAME, "supporting-talent").text.strip()
            venue = event.find_element(By.CLASS_NAME, "venue").text.strip()
            ages_price = event.find_element(By.CLASS_NAME, "ages-price").text.strip()
            genre = event.find_element(By.CLASS_NAME, "genre").text.strip()

            # Store the event details in the sold_out_events list
            sold_out_events.append({
                "title": title,
                "date": date,
                "headliners": headliners,
                "supporting_talent": supporting_talent,
                "venue": venue,
                "ages_price": ages_price,
                "genre": genre,
                "status": "Sold Out"
            })
    except Exception as e:
        print(f"An error occurred while processing an event: {e}")
        continue

# Close the browser
driver.quit()

# Output the sold-out events
if sold_out_events:
    print("Sold-out events:")
    for event in sold_out_events:
        print(event)
else:
    print("No sold-out events found.")
