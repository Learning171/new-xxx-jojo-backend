import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException


def send_password_reset_email(email: str, reset_link: str):
    email_config = {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "smtp_username": "shanpm171@gmail.com",
        "smtp_password": "bcstirxzlernpcts",
        "sender_email": "shanpm171@gmail.com",
    }

    subject = "Password Reset"
    body = f"Click the following link to reset your password: {reset_link}"

    msg = MIMEMultipart()
    msg["From"] = email_config["sender_email"]
    msg["To"] = email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(
            email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(email_config["smtp_username"], email_config["smtp_password"])

            server.sendmail(email_config["sender_email"], email, msg.as_string())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send password reset email. Error: {str(e)}",
        )
