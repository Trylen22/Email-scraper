from bs4 import BeautifulSoup
import json

def process_data(raw_emails):
    """Processes and cleans raw email data."""
    processed_data = []
    for email in raw_emails:
        # Decode and clean email body
        raw_body = email.get("body", "")
        soup = BeautifulSoup(raw_body, "html.parser")
        plain_text_body = soup.get_text(strip=True)
        
        # Skip emails without meaningful content
        if not plain_text_body.strip():
            plain_text_body = "No meaningful content."

        # Add cleaned data to the processed list
        processed_data.append({
            "subject": email.get("subject", "No Subject"),
            "from": email.get("from", "Unknown Sender"),
            "body": plain_text_body
        })

    # Save processed data for future use
    with open("data/processed/processed_emails.json", "w") as file:
        json.dump(processed_data, file, indent=4)

    return processed_data
