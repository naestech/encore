import os
import re
import requests
import smtplib
import ssl
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Email configuration from environment variables
smtp_server = os.getenv("SMTP_SERVER")
port = int(os.getenv("SMTP_PORT", 587))  # Default to 587 if not set
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

def sanitize_filename(url):
    # Remove the protocol (http:// or https://)
    url = re.sub(r'^https?://', '', url)
    # Replace invalid filename characters with underscores
    return re.sub(r'[^\w\-_\. ]', '_', url)

def save_website_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')
        html_content = soup.prettify()

        filename = sanitize_filename(url) + '.html'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"HTML content saved to {filename}")
        return filename

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def find_sold_out_shows(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all elements with the "Sold Out" status
    sold_out_items = soup.find_all('a', class_='seetickets-buy-btn', string=lambda text: text and 'sold out' in text.lower())

    # Debug: Print number of sold-out items found
    print(f"Found {len(sold_out_items)} sold out items")

    sold_out_shows = []

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
            location = show.find('p', class_='fs-12 venue').get_text(strip=True).replace('at ', '')
            price = show.find('p', class_='fs-12 ages-price').get_text(strip=True) if show.find('p', class_='fs-12 ages-price') else 'N/A'
            genre = show.find('p', class_='fs-12 genre').get_text(strip=True)
            tickets_link = show.find('a', class_='seetickets-buy-btn')['href']

            sold_out_shows.append({
                "product_name": product_name,
                "artist": artist,
                "date": date,
                "location": location,
                "price": price,
                "genre": genre,
                "tickets_link": tickets_link
            })

    return sold_out_shows

def create_email(subject, body):
    # Create the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body with the message instance
    message.attach(MIMEText(body, "html"))  # Changed to HTML for better formatting

    return message

def send_email(message):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Send email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

def compile_and_send_email(sold_out_shows):
    # Email subject
    subject = "Weekly Unsigned Artists Update"

    # Introduction paragraph
    body = """
    <h2>Here's your recap of artists who have sold out or are close to selling out their shows:</h2>
    """

    # Building the artist section
    for show in sold_out_shows:
        body += f"""
        <p>
            <strong>Artist:</strong> {show['product_name']}<br>
            <strong>Date:</strong> {show['date']}<br>
            <strong>Location:</strong> {show['location']}<br>
            <strong>Price:</strong> {show['price']}<br>
            <strong>Genre:</strong> {show['genre']}<br>
            <strong>Event Link:</strong> <a href="{show['tickets_link']}">Link</a>
        </p>
        <hr>
        """

    # Footer
    body += """
    <footer>
        <p>Powered by Encore | <a href="https://github.com/your-github-repo">GitHub</a></p>
        <p>Made with ♥ by Technaelogy</p>
        <p><a href="https://instagram.com/your_instagram">Instagram</a> | <a href="https://substack.com/your_substack">Substack</a></p>
    </footer>
    """

    # Create and send the email
    email_message = create_email(subject, body)
    send_email(email_message)

if __name__ == "__main__":
    url = input("Enter the website URL: ")
    html_file = save_website_html(url)
    if html_file:
        sold_out_shows = find_sold_out_shows(html_file)
        if sold_out_shows:
            compile_and_send_email(sold_out_shows)
        else:
            print("No sold-out shows found.")
