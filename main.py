import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# load environment variables from a .env file
load_dotenv()

# email configuration from environment variables
smtp_server = os.getenv("SMTP_SERVER")
port = int(os.getenv("SMTP_PORT", 465))  # default to 465 if not set
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

def create_email(subject, body):
    # create the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # attach the body with the msg instance
    message.attach(MIMEText(body, "plain"))

    return message

def send_email(message):
    # create a secure SSL context
    context = ssl.create_default_context()

    # send email
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("email sent successfully!")
    except Exception as e:
        print(f"error: {e}")

def compile_and_send_email():
    # test data to simulate the artist data
    subject = "Test: Weekly Unsigned Artists Update"
    body = "This is a test email to verify the script works.\n\n"

    # simulated artist data for testing purposes
    artist_data = (
        "1. Test Artist A - Test Venue X\n"
        "2. Test Artist B - Test Venue Y\n"
        "3. Test Artist C - Test Venue Z\n"
    )
    body += artist_data

    # create and send the email
    email_message = create_email(subject, body)
    send_email(email_message)

# directly call the function to test sending the email
compile_and_send_email()
