import qrcode
import os
from reportlab.pdfgen import canvas
from PIL import Image

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
        
    # Redimensionnement et fusion du logo de Python Togo et du QR code
    logo = Image.open("Py.png").convert('RGBA') 
    img_width, img_height = img.size
    logo_size = int(img_width * 0.3)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    pos = ((img_width - logo_size) // 2, (img_height - logo_size) // 2)
    img.paste(logo, pos, mask=logo)
    img.resize((150, 150))
    img.save("img.png")
    
   # création du PDF
    width, height = 14.8, 10
    c = canvas.Canvas("ticket.pdf", pagesize=(width, height))
    c.setFont("Helvetica-Bold", 0.5)
    c.drawCentredString(7.2, 9, f"Ticket - PyCon Togo 2025")
    c.setFont("Helvetica", 0.3)
    c.drawString(1.2, 8, f"Name : {participant_name}")
    c.drawString(1.2, 7.3, f"Reference : {ticket_ref}")
    c.drawString(1.2, 6.6, f"Tshirt size : {tshirt_size}")
    c.drawString(1.2, 5.9, f"Group : {group}")
    c.setLineWidth(0.05)
    c.line(7.4, 8.4, 7.4, 5.6)
    c.drawImage("img.png", 10, 5, width=4, height=4)
    c.setLineWidth(0.05)
    c.line(1.2, 5, 13.5, 5)
    c.drawImage("logo2.png", 7.5, 2.8, width=2.7, height=1.7)
    c.drawImage("logo3.png", 10.5, 2.5, width=3.5, height=2.25)
    c.save()



import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from email.mime.image import MIMEImage

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

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('le_mail_expéditeur', 'code_appli_mail')
        smtp.send_message(msg)

participant_email = "luckyflesher1262@gmail.com"
participant_name = "tester 1"
participant_Tshirt_size = "L"
participant_group = "PyTogo"
ticket_ref = "TCK-2025-00042"

generate_qr_code_pdf(ticket_ref, participant_name, ticket_ref, participant_Tshirt_size, participant_group)
send_ticket_email(participant_name, participant_email)