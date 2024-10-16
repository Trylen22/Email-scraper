import imaplib
import email
from email.header import decode_header
import json

def scrape_emails():
    """Connects to the email server and retrieves raw email data."""
    # Define server and login details (configure in `config.py`)
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login("your_email@example.com", "your_password")
    server.select("inbox")
    
    # Search for all emails in the inbox
    status, messages = server.search(None, 'ALL')
    email_ids = messages[0].split()
    
    emails = []
    for email_id in email_ids[-10:]:  # Get the last 10 emails for example
        _, msg_data = server.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # Decode email content and append to emails list
                emails.append({
                    "subject": decode_header(msg["Subject"])[0][0],
                    "from": msg.get("From"),
                    "body": msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                })
    
    # Save raw data for backup
    with open("data/raw/raw_emails.json", "w") as file:
        json.dump(emails, file, indent=4)
    
    server.logout()
    return emails
