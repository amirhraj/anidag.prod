import smtplib, ssl
from email.mime.text import MIMEText

SMTP_HOST = "smtp.beget.com"
SMTP_PORT = 2525
SMTP_USER = "anidag@anidag.ru"
SMTP_PASS = "3gMsLRTbQjVSZkdqa5dOKrHy0XiCz-sx_"

to_email = "rrou37892@gmail.com"

msg = MIMEText("Hello! Test email from Beget SMTP", "plain", "utf-8")
msg["Subject"] = "Beget SMTP test"
msg["From"] = SMTP_USER
msg["To"] = to_email

with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls(context=ssl.create_default_context())
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASS)
    server.send_message(msg)
