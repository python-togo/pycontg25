import os
from email.message import EmailMessage
from email.utils import formataddr
import smtplib
from dotenv import load_dotenv

from email_templates import render_sponsor_email

load_dotenv()




SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_SERVER_PORT = os.environ.get("SMTP_SERVER_PORT")


def send_email(subject, body, email_to):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = formataddr(('PyCon Togo Organizing Team', SENDER_EMAIL))
    msg['To'] = email_to

   
    full_message = body
    msg.add_alternative(full_message, subtype='html')

    
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SERVER_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        server.send_message(msg)
   

def send_sponsor_email(first_name="Pythonista", email_to="sponsor@example.com"):
    message, subject = render_sponsor_email(first_name=first_name)

    send_email(subject, message, email_to)
