"""
Name: Nadine
Email: naestech@proton.me
Description: Script for generating and sending emails with information about sold-out shows. 
Formats venue and TikTok data into an HTML email body.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.utils.errorHandler import ErrorHandler
from dotenv import load_dotenv

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.errorHandler = ErrorHandler()
        self.smtpServer = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_PORT", 587))
        self.senderEmail = os.getenv("SENDER_EMAIL")
        self.receiverEmail = os.getenv("RECEIVER_EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")

    def sendEmail(self, subject, body):
        try:
            message = self._createEmail(subject, body)
            self._sendEmail(message)
        except Exception as e:
            self.errorHandler.handle_api_error(e, "Email Sending")

    def _createEmail(self, subject, body):
        message = MIMEMultipart()
        message["From"] = self.senderEmail
        message["To"] = self.receiverEmail
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))
        return message

    def _sendEmail(self, message):
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP(self.smtpServer, self.port) as server:
                server.starttls(context=context)
                server.login(self.senderEmail, self.password)
                server.sendmail(
                    self.senderEmail,
                    self.receiverEmail,
                    message.as_string()
                )
        except Exception as e:
            self.errorHandler.handle_api_error(e, "SMTP Operation")

    def generateEmailBody(self, venueResults, tikTokResults):
        body = """
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
            <h2>Here's your recap of artists who have sold out or are close to selling out their shows:</h2>
            <h3>Venue Updates:</h3>
        """
        
        for show in venueResults:
            body += f"""
            <div style="margin-bottom: 20px; padding: 10px; border-left: 4px solid #1DB954;">
                <strong>Artist:</strong> {show['artist']}<br>
                <strong>Venue:</strong> {show['location']}<br>
                <strong>Date:</strong> {show['date']}<br>
                <strong>Price:</strong> {show['price']}<br>
                <strong>Genre:</strong> {show['genre']}<br>
                <strong>Tickets:</strong> <a href="{show['tickets_link']}" target="_blank" rel="noreferrer nofollow noopener">Link</a>
            </div>
            """

        body += "<h3>TikTok Mentions:</h3>"
        
        for post in tikTokResults:
            body += f"""
            <div style="margin-bottom: 20px; padding: 10px; border-left: 4px solid #FF0050;">
                <strong>Creator:</strong> {post['username']}<br>
                <strong>Content:</strong> {post['post_content']}<br>
                <strong>Link:</strong> <a href="{post['video_url']}" target="_blank" rel="noreferrer nofollow noopener">Watch Video</a>
            </div>
            """
        
        body += """
            <hr>
            <p style="color: #666; font-size: 12px;">
                Powered by Encore | <a href="https://github.com/technaelogy/encore" target="_blank" rel="noreferrer nofollow noopener">GitHub</a><br>
                <em>Made with ♥ by technaelogy</em>
            </p>
        </div>
        """
        
        return body
