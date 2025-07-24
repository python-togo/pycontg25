




import os
from email.message import EmailMessage
from email.utils import formataddr
import smtplib
from dotenv import load_dotenv

load_dotenv()




SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_SERVER_PORT = os.environ.get("SMTP_SERVER_PORT")
API_ROOT = os.environ.get("API_ROOT", "http://127.0.0.1:8080/api")

def send_email(subject, body, email_to):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = formataddr(('PyCon Togo Organizing Team', SENDER_EMAIL))
    msg['To'] = email_to

   
    full_message = render_email_template(message=message)
    msg.add_alternative(full_message, subtype='html')

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SERVER_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Ticket email sent to {participant_email} the ticket is available at {ticket_url}")
    except Exception as e:
        print(f"Failed to send ticket email to {participant_email}: {e}")