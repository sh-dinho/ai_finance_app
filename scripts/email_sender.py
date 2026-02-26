import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_report_email(settings, report_text: str):
    cfg = settings.email.email

    sender = cfg.sender
    recipient = cfg.recipient
    password = cfg.app_password  # already expanded from .env
    smtp_server = cfg.smtp_server
    smtp_port = cfg.smtp_port
    use_ssl = cfg.use_ssl

    # If password missing, silently skip email
    if not password:
        print("[email] Skipped: EMAIL_APP_PASSWORD not set.")
        return

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "Your Daily Financial Intelligence Report"
    msg.attach(MIMEText(report_text, "plain"))

    try:
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)

        print("[email] Report sent successfully.")

    except Exception as e:
        print(f"[email] Failed to send email: {e}")
