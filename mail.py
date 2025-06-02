import smtplib
import email.utils
import os
import argparse
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

# Configuration
SMTP_SERVER = "smtp.email.us-ashburn-1.oci.oraclecloud.com"
SMTP_PORT = 587
SENDER_EMAIL = 'support@aisol4biz.ai'
SENDER_NAME = 'AIAGENTS4BIZ SUPPORT'

def send_email(to_email, subject, body, attachment_path=None):
    """
    Send email via OCI SMTP with optional attachment
    """
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = email.utils.formataddr((SENDER_NAME, SENDER_EMAIL))
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body text
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                part = MIMEApplication(
                    file.read(),
                    Name=os.path.basename(attachment_path)
                )
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
            print(f"Attachment {attachment_path} added to email")
        elif attachment_path:
            print(f"Warning: Attachment file {attachment_path} not found")
        
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
    parser.add_argument('--attachment', help='Path to attachment file')
    
    args = parser.parse_args()
    send_email(args.to, args.subject, args.body, args.attachment)
