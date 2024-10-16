import json

def process_data(raw_emails):
    """Processes and cleans raw email data."""
    # Example: Remove unnecessary whitespace, handle encoding issues, etc.
    processed_data = []
    for email in raw_emails:
        cleaned_body = email["body"].strip().replace("\n", " ")
        processed_data.append({
            "subject": email["subject"],
            "from": email["from"],
            "body": cleaned_body
        })
    
    # Save processed data for future use
    with open("data/processed/processed_emails.json", "w") as file:
        json.dump(processed_data, file, indent=4)
    
    return processed_data
