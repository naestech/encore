from bs4 import BeautifulSoup

# Load the HTML file
with open('troubadour.com.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Find all elements with the "Sold Out" status
sold_out_items = soup.find_all('a', class_='seetickets-buy-btn', string=lambda text: text and 'sold out' in text.lower())

# Debug: Print number of sold-out items found
print(f"Found {len(sold_out_items)} sold out items")

# Extract and print the details of each sold-out show
for item in sold_out_items:
    # Find the parent or relevant element for the whole show details
    show = item.find_parent('div', class_='mdc-card')  # Adjust this if needed based on actual structure

    if show:
        # Extract show details
        product_name = show.find('p', class_='fs-18 bold mb-12 title').get_text(strip=True)
        artist_link = show.find('a', href=True)
        artist = artist_link.get_text(strip=True) if artist_link else 'N/A'
        date = show.find('p', class_='fs-18 bold mt-1r date').get_text(strip=True)
        location = show.find('p', class_='fs-12 venue').get_text(strip=True)
        price = show.find('p', class_='fs-12 ages-price').get_text(strip=True)
        genre = show.find('p', class_='fs-12 genre').get_text(strip=True)
        share_event = show.find('a', class_='seetickets-social-share')
        tickets_link = show.find('a', class_='seetickets-buy-btn')

        # Print the details
        print(f"Troubadour Presents: {product_name}")
        print(f"Artist: {artist}")
        print(f"Date: {date}")
        print(f"Location: {location}")
        print(f"Price: {price}")
        print(f"Genre: {genre}")
        print(f"Share Event: {share_event['href'] if share_event else 'N/A'}")
        print(f"Tickets: {'Sold Out' if tickets_link and 'sold out' in tickets_link.get_text().lower() else 'Available'}")
        print("-" * 40)
