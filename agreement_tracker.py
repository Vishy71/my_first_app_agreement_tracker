import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# Create email
msg = EmailMessage()
msg['Subject'] = 'Test Email'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg.set_content('This is a test email from Agreement Tracker app.')

# Send email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print(f"Email sent successfully to {EMAIL_ADDRESS}")
except Exception as e:
    print(f"Failed to send email to {EMAIL_ADDRESS}: {e}")