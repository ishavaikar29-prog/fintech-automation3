# email_sender.py

import os
import smtplib
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

from utils.error_handler import log_error


def send_email_with_attachments(
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    to_email: str,
    subject: str,
    body: str,
    attachments: List[str],
) -> None:
    """Send an email with multiple attachments."""
    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Attach all files if they exist
    for fpath in attachments:
        if not fpath or not os.path.exists(fpath):
            continue

        part = MIMEBase("application", "octet-stream")
        with open(fpath, "rb") as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(fpath)}"
        )

        msg.attach(part)

    try:
        print("Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")

    except Exception as e:
        log_error("EMAIL SEND FAILED", e)
        print("Email sending error. Check error.log")

