import os
from aiosmtplib import send
from email.message import EmailMessage

async def send_email(to, subject, body, attachment=None, filename=None):
    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    if attachment and filename:
        msg.add_attachment(attachment, maintype="application", subtype="octet-stream", filename=filename)

    await send(
        msg,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=os.getenv("EMAIL_USER"),
        password=os.getenv("EMAIL_PASS")
    )
