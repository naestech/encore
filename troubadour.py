from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Selenium with Brave browser
chrome_options = Options()
chrome_options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
webdriver_service = Service('/usr/local/bin/chromedriver')

# Initialize the webdriver
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Navigate to the Troubadour website
driver.get("https://troubadour.com/")

# Wait for the page to load
wait = WebDriverWait(driver, 60)  # increased wait time to 60 seconds
wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'list-view-item')]")))

# Simulate human-like scrolling to load all events
def human_like_scroll():
    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 200):  # scroll in steps of 200px
        driver.execute_script(f"window.scrollTo(0, {i});")
        time.sleep(0.1)  # wait for a short time to simulate human scrolling

human_like_scroll()

# Find all the show listings using XPath
shows = driver.find_elements(By.XPATH, "//div[contains(@class, 'list-view-item')]")

# Initialize a list to hold sold-out shows
sold_out_shows = []

# Loop through each show and check if it's sold out
for show in shows:
    try:
        # Scroll the show into view
        driver.execute_script("arguments[0].scrollIntoView();", show)
        time.sleep(0.5)

        # Check if the "Sold Out" text is present in the event's inner HTML
        if "sold out" in show.get_attribute("innerHTML").lower():
            title_element = show.find_element(By.XPATH, ".//h3[contains(@class, 'list-view-item-title')]")
            title = title_element.text.strip()
            date_element = show.find_element(By.XPATH, ".//p[contains(@class, 'list-view-item-date')]")
            date = date_element.text.strip()
            sold_out_shows.append({"title": title, "date": date})

    except Exception as e:
        print(f"Error processing a show: {e}")
        continue

# Quit the webdriver
driver.quit()

# Convert the list to a pandas dataframe for better output formatting
df = pd.DataFrame(sold_out_shows)

# Check if there are any sold-out shows and output them
if not df.empty:
    print("Sold-out shows:")
    print(df.to_string(index=False))
else:
    print("No sold-out shows found.")

# Print total number of shows scraped
print(f"\nTotal shows scraped: {len(shows)}")