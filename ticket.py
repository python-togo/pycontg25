import qrcode
import os
from reportlab.pdfgen import canvas
from PIL import Image
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.image import MIMEImage
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_SERVER_PORT = os.environ.get("SMTP_SERVER_PORT")

def generate_qr_code_pdf(data, participant_name, ticket_ref, tshirt_size, group):
    # création du QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    img.save("img.png")
        
    # sélection des logos
    base_dir = os.path.dirname(__file__)  # répertoire actuel
    logo = os.path.join(base_dir, "static", "images", "logo.png")
    logo2 = os.path.join(base_dir, "static", "images", "logo2.png")
    logo3 = os.path.join(base_dir, "static", "images", "logo3.png")    
    
    
   # création du PDF
    width, height = 14.8, 8
    c = canvas.Canvas("ticket.pdf", pagesize=(width, height))
    c.setFont("Helvetica-Bold", 0.5)
    c.drawCentredString(7.2, 7, f"Ticket - PyCon Togo 2025")
    c.setFont("Helvetica", 0.3)
    if(tshirt_size == ""):
        c.drawString(1.2, 6, f"Name : {participant_name}")
        c.drawString(1.2, 4.95, f"Reference : {ticket_ref}")
        c.drawString(1.2, 3.9, f"Company/Community : {group}")
    else:
        c.drawString(1.2, 6, f"Name : {participant_name}")
        c.drawString(1.2, 5.3, f"Reference : {ticket_ref}")
        c.drawString(1.2, 4.6, f"Tshirt size : {tshirt_size}")
        c.drawString(1.2, 3.9, f"Company/Community : {group}")
    c.setLineWidth(0.05)
    c.line(7.4, 6.4, 7.4, 3.5)
    c.drawImage("img.png", 10, 3, width=4, height=4)
    c.setLineWidth(0.05)
    c.line(1.2, 3, 13.5, 3)
    c.drawImage(logo, 1.2, 0.8, width=2.5, height=1.5)
    c.drawImage(logo2, 6.05, 0.8, width=2.7, height=1.5)
    c.drawImage(logo3, 10.5, 0.6, width=3, height=1.7)
    c.save()

def send_ticket_email(participant_name, participant_email):
    msg = EmailMessage()
    msg['Subject'] = f"🎫 Votre ticket pour le PyCon Togo 2025"
    msg['From'] = formataddr(('Togo Python Community', 'goldendragonslayer20@gmail.com'))
    msg['To'] = participant_email

    # corps du mail en HTML
    html = f"""
    <html>
        <body>
            <h2>Bonjour {participant_name},</h2>
            <p>Merci pour votre inscription au <strong>PyCon Togo 2025</strong> !</p>
            <p>Voici votre ticket ci-dessous. Présentez ce QR code à l’entrée :</p>
            <p>À bientôt !</p>
        </body>
    </html>
    """

    msg.set_content("Voici votre ticket pour l'événement. Veuillez utiliser un client mail compatible HTML pour voir le QR code.")
    msg.add_alternative(html, subtype='html')
    
    with open("ticket.pdf", 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename="PyconTicket2025.pdf")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SERVER_PORT) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        smtp.send_message(msg)