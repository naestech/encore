"""
Name: Nadine
Email: naestech@proton.me
Description: Test script for the email functionality of the Encore project. 
Simulates TikTok and venue data to generate and send a test email.
"""

from src.data.tikTokScraper import TikTokScraper
from src.data.venueScraper import VenueScraper
from src.email.emailSender import EmailSender
from src.utils.logger import info_logger, error_logger, debug_logger

def test_email_functionality():
    tikTokScraper = TikTokScraper()
    venueScraper = VenueScraper()
    emailSender = EmailSender()

    # Simulate TikTok data
    tikTokResults = [
        {
            'username': 'testuser1',
            'post_content': 'Amazing sold out concert! #soldout',
            'post_time': 1629123456,
            'video_url': 'https://www.tiktok.com/test1'
        },
        {
            'username': 'testuser2',
            'post_content': 'Can\'t believe the show sold out so fast! #concert',
            'post_time': 1629234567,
            'video_url': 'https://www.tiktok.com/test2'
        }
    ]

    # Simulate venue data
    venueResults = [
        {
            'artist': 'Test Artist 1',
            'date': '2023-08-15',
            'location': 'Test Venue 1',
            'price': '$50',
            'genre': 'Test Genre 1',
            'tickets_link': 'https://testtickets.com/1'
        },
        {
            'artist': 'Test Artist 2',
            'date': '2023-08-20',
            'location': 'Test Venue 2',
            'price': '$75',
            'genre': 'Test Genre 2',
            'tickets_link': 'https://testtickets.com/2'
        }
    ]

    # Clean TikTok data
    cleanedTikTokResults = tikTokScraper.clean_tiktok_data(tikTokResults)

    # Generate email body
    body = emailSender.generateEmailBody(venueResults, cleanedTikTokResults)

    # Set email subject
    subject = "Encore: Test Email"

    # Send email
    emailSender.sendEmail(subject, body)
    info_logger.info("Test email sent successfully!")

if __name__ == "__main__":
    test_email_functionality()
