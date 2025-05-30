import smtplib
import email.utils
import os
import argparse
from email.message import EmailMessage
import ssl

# Configuration
SMTP_SERVER = "smtp.email.us-ashburn-1.oci.oraclecloud.com"
SMTP_PORT = 587
SENDER_EMAIL = 'rameshkrishnan@ebizoncloud.com'
SENDER_NAME = 'AIAGENTS4BIZ SUPPORT'

def send_email(to_email, subject, body):
    """
    Send email via OCI SMTP
    """
    try:
        # Create message
        msg = EmailMessage()
        msg['From'] = email.utils.formataddr((SENDER_NAME, SENDER_EMAIL))
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.set_content(body)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
            server.send_message(msg)
        
        print(f"Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send emails via OCI SMTP')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--body', required=True, help='Email body content')
    
    args = parser.parse_args()
    send_email(args.to, args.subject, args.body)
