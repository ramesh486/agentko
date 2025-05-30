import smtplib
import email.utils
import os
from email.message import EmailMessage
import ssl

# Configuration - Load from environment variables
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
HOST = "smtp.email.us-ashburn-1.oci.oraclecloud.com"
PORT = 587
SENDER = 'support@aisol4biz.ai'
SENDERNAME = 'AIAGENTS4BIZ SUPPORT'

def send_simple_email(to, subject, body_text):
    """
    Send a simple text email
    :param to: Recipient email address
    :param subject: Email subject
    :param body_text: Plain text email content
    """
    # Create message container
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = to
    
    # Set plain text body
    msg.set_content(body_text)

    # Try to send the message
    try:
        with smtplib.SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER, to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Example usage
if __name__ == "__main__":
    # This would be called from your GitHub Actions workflow
    send_simple_email(
        to="recipient@example.com",
        subject="Simple Greeting",
        body_text="Hello Sir,\n\nHow are you?\n\nBest regards,\nYour Team"
    )
