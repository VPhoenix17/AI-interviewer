import yagmail
import os
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

email_address = os.getenv("NO_REPLY_EMAIL_ADDRESS")
password = os.getenv("NO_REPLY_EMAIL_PASSWORD")

def send_email(subject, message, to_email):
    try:
        with yagmail.SMTP(email_address, password) as yag:
            yag.send(to=to_email, subject=subject, contents=message)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        
def send_email_with_attachment(subject, message, to_email, attachment):
    try:
        with yagmail.SMTP(email_address, password) as yag:
            yag.send(to=to_email, subject=subject, contents=message, attachments=attachment)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")