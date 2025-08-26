def render_email_template( message=""):
    """
    Renders the email template with the provided body and subject.
    
    Args:
        body (str): The body of the email.
        subject (str): The subject of the email.
    
    Returns:
        str: The rendered HTML email template.
    """
    html = f"""\
        <html lang="en">
        <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <style>
            body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333333;
            background-color: #ffffff;
            }}
            .container {{
            max-width: 600px;
            margin: auto;
            padding: 20px;
            }}
            .logo {{
            text-align: center;
            margin-bottom: 20px;
            }}
            .logo img {{
            width: 150px;
            }}
            /* .content {{
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            }} */
            .content h2 {{
            color: #111111;
            }}
            .content p {{
            line-height: 1.6;
            }}
            .highlight {{
            font-weight: bold;
            }}
            a {{
            color: #007bff;
            text-decoration: none;
            }}
            .footer {{
            text-align: center;
            font-size: 14px;
            margin-top: 30px;
            color: #666;
            }}
            .social-icons {{
            margin-top: 10px;
            }}
            .social-icons img {{
            width: 24px;
            margin: 0 5px;
            vertical-align: middle;
            }}
            @media (max-width: 600px) {{
            .container {{
                padding: 15px;
            }}
            .content {{
                padding: 15px;
            }}
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <div class="logo">
            <img src="https://pycontg.pytogo.org/static/images/pycontogo.png" alt="PyCon TOGO 2025 Logo">
            </div>
            <div class="content">


           {message}

            <p><strong>Best regards,</strong></p>
        </div>

            <div class="footer">
            <!-- <img class="logo" src="static/images/pycontogo.png" alt="PyCon TOGO 2025 Logo"> -->
            <p><strong>Python Togo Community</strong><br>
            <a href="https://wwww.pytogo.org/">Python TOGO</a><br>
            Bd de la KARA, +22898273805 / +22892555987 / +22898776682, LOME</p>

            <div class="social-icons">
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn"></a>
                <a href="https://pytogo.org/discord"><img src="https://cdn-icons-png.flaticon.com/512/5968/5968756.png" alt="Discord"></a>
                <a href="https://github.com/pytogo-org"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub"></a>
                <a href="https://x.com/pytogo_org"><img src="https://cdn-icons-png.flaticon.com/512/733/733635.png" alt="X/Twitter"></a>
                <a href="https://www.youtube.com/@PythonTogo"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" alt="YouTube"></a>
                <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png" alt="Instagram"></a>
            </div>
            </div>
        </div>
        </body>
        </html>
    """
    return html



def render_sponsor_email(first_name="Pythonista"):
    html = f"""\
    <div style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6; padding: 20px;">

  <!-- English Section -->
  <h2 style="color: #1a73e8;">🤝 Thank You for Your Interest in Sponsoring PyCon Togo 2025</h2>
    
  <p>Dear <strong>{first_name}</strong>,</p>

  <p>We sincerely appreciate your interest in sponsoring <strong>PyCon Togo 2025</strong>. Your support helps us strengthen the Python and tech ecosystem in Togo.</p>

  <p>Our team has received your submission. One of our members will reach out to you shortly to discuss possible collaboration opportunities and finalize sponsorship arrangements.</p>

  <p>In the meantime, feel free to send us:</p>
  <ul style="padding-left: 20px;">
    <li>Your preferred sponsorship level or package</li>
    <li>Your brand/logo guidelines (if available)</li>
    <li>Any questions or expectations you may have</li>
  </ul>

  <p>We’re looking forward to partnering with you!</p>

  <p>Best regards,<br>
  The PyCon Togo 2025 Team<br>


  <hr style="margin: 40px 0; border: none; border-top: 1px solid #cccccc;">

  <!-- French Section -->
  <h2 style="color: #1a73e8;">🤝 Merci pour votre intérêt à sponsoriser PyCon Togo 2025</h2>

  <p>Cher·e <strong>{first_name}</strong>,</p>

  <p>Nous vous remercions sincèrement pour votre intérêt à sponsoriser <strong>PyCon Togo 2025</strong>. Votre soutien contribue au développement de l'écosystème Python et technologique au Togo.</p>

  <p>Nous avons bien reçu votre soumission. Un membre de notre équipe vous contactera sous peu pour discuter des opportunités de collaboration et finaliser les modalités de sponsoring.</p>

  <p>En attendant, vous pouvez déjà nous envoyer :</p>
  <ul style="padding-left: 20px;">
    <li>Le niveau ou le type de sponsoring souhaité</li>
    <li>Votre charte graphique ou logo (si disponible)</li>
    <li>Toute question ou attente spécifique que vous pourriez avoir</li>
  </ul>

  <p>Nous sommes impatients de collaborer avec vous !</p>

  <p>Cordialement,<br>
  L’équipe PyCon Togo 2025<br>


</div>
    """
    body = render_email_template(message=html)
    subject = "🤝 Thank You for Your Interest in Sponsoring PyCon Togo 2025"
    return body, subject

def render_email_attendees():
    html = f"""\
    <div style="font-family: Arial, sans-serif; color: #333333;; line-height: 1.6; padding: 20px;">

  <!-- Version française -->
  <p>Bonjour Participant·e,</p>

  <p>
    Nous vous remercions chaleureusement pour avoir rejoint la toute première <strong>PyCon Togo</strong> ! 
    Que ce soit <strong>en personne</strong> ou <strong>en ligne via notre live YouTube</strong>, 
    votre présence et vos échanges ont rendu cet événement spécial et enrichissant pour toute l’Afrique 
    (Nigeria, Togo, Bénin, Côte d’Ivoire, Ghana…).
  </p>

  <p>Pour continuer à nous améliorer et rester en contact, voici quelques ressources utiles :</p>
  <ul>
    <li><a href="https://pycontg.pytogo.org/feedback" style="color: #006400; text-decoration: underline;">Donnez votre feedback</a></li>
    <li><a href="https://www.youtube.com/live/sOAoUH0pZNU?si=Fk1i7dsn4HnQcbWb" style="color: #006400; text-decoration: underline;">Regardez l’événement à la demande</a></li>
    <li><a href="https://pycontg.pytogo.org/talents" style="color: #006400; text-decoration: underline;">Opportunités avec notre partenaire DigiJob</a></li>
  </ul>

  <p>
    Merci encore pour votre enthousiasme et votre soutien. Nous espérons vous retrouver lors de nos prochains événements !
  </p>

  <p>Cordialement,<br><strong>L’équipe PyCon Togo</strong></p>

  <hr style="border: 0; border-top: 1px solid #006400; margin: 20px 0;">

  <!-- English Version -->
  <p>Hello Participant,</p>

  <p>
    We sincerely thank you for joining the very first <strong>PyCon Togo</strong>! 
    Whether you participated <strong>in person</strong> or <strong>online via our YouTube live</strong>, 
    your presence and contributions made this event special and engaging across Africa 
    (Nigeria, Togo, Benin, Ivory Coast, Ghana…).
  </p>

  <p>To help us improve and stay connected, here are some useful resources:</p>
  <ul>
    <li><a href="https://pycontg.pytogo.org/feedback" style="color: #006400; text-decoration: underline;">Give your feedback</a></li>
    <li><a href="https://www.youtube.com/live/sOAoUH0pZNU?si=Fk1i7dsn4HnQcbWb" style="color: #006400; text-decoration: underline;">Watch the event on demand</a></li>
    <li><a href="https://pycontg.pytogo.org/talents" style="color: #006400; text-decoration: underline;">Opportunities with our partner DigiJob</a></li>
  </ul>

  <p>
    Thank you again for your enthusiasm and support. We hope to see you at our future events!
  </p>

  <p>Best regards,<br><strong>PyCon Togo Team</strong></p>

</div>
"""
    body = render_email_template(message=html)
    subject = "Merci pour votre participation à PyCon Togo 2025 / Thank you for joining PyCon Togo 2025"
    return body, subject