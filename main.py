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
    message.attach(MIMEText(body, "plain"))

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
    # Test data to simulate the artist data
    subject = "Test: Weekly Unsigned Artists Update"
    body = "This is a test email to verify the script works.\n\n"

    # Simulated artist data for testing purposes
    artist_data = (
        "1. Test Artist A - Test Venue X\n"
        "2. Test Artist B - Test Venue Y\n"
        "3. Test Artist C - Test Venue Z\n"
    )
    body += artist_data

    # Create and send the email
    email_message = create_email(subject, body)
    send_email(email_message)

# Directly call the function to test sending the email
compile_and_send_email()
