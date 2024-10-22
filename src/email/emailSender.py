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
