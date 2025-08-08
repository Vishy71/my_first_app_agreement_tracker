import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

to_email = "yourtestemail@example.com"
subject = "Test Email"
body = "This is a test email using dotenv!"

# Compose email
message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = to_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

# Send email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(message)
        print(f"Reminder sent to {to_email}")
except Exception as e:
    print(f"Failed to send email to {to_email}: {e}")