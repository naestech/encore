import os
import smtplib
import ssl
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

def compile_and_send_email():
    # Email subject
    subject = "Test: Weekly Unsigned Artists Update"

    # Introduction paragraph
    body = """
    <h2>Here's your recap of artists who have sold out or are close to selling out their shows:</h2>
    """

    # Simulated artist and venue data for testing purposes
    artists = [
        {
            "name": "Test Artist A",
            "streaming_links": "<a href='#'>Spotify</a> | <a href='#'>Apple Music</a>",
            "social_links": "<a href='#'>Instagram</a> | <a href='#'>Tiktok</a>",
            "venue_name": "Test Venue X",
            "venue_location": "New York, NY",
            "capacity_percent": "95%"
        },
        {
            "name": "Test Artist B",
            "streaming_links": "<a href='#'>Spotify</a> | <a href='#'>Apple Music</a>",
            "social_links": "<a href='#'>Instagram</a> | <a href='#'>Tiktok</a>",
            "venue_name": "Test Venue Y",
            "venue_location": "Los Angeles, CA",
            "capacity_percent": "98%"
        },
        {
            "name": "Test Artist C",
            "streaming_links": "<a href='#'>Spotify</a> | <a href='#'>Apple Music</a>",
            "social_links": "<a href='#'>Instagram</a> | <a href='#'>Tiktok</a>",
            "venue_name": "Test Venue Z",
            "venue_location": "Chicago, IL",
            "capacity_percent": "100%"
        }
    ]

    # Building the artist section
    for artist in artists:
        body += f"""
        <h3>{artist['name']}</h3>
        <p>
            <strong>Streaming Links:</strong> {artist['streaming_links']}<br>
            <strong>Social Media:</strong> {artist['social_links']}<br>
            <strong>Venue:</strong> {artist['venue_name']} - {artist['venue_location']}<br>
            <strong>Capacity:</strong> {artist['capacity_percent']}
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

# Directly call the function to test sending the email
compile_and_send_email()

