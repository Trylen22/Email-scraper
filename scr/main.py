from authemail import authenticate_gmail
from scrape_emails import fetch_emails
from process_emails import process_data
from local_model import LocalModel

def main():
    # Step 1: Authenticate with Gmail
    service = authenticate_gmail()
    if not service:
        print("Failed to authenticate Gmail.")
        return

    # Step 2: Fetch raw emails
    raw_emails = fetch_emails(service, max_results=10)
    if not raw_emails:
        print("No emails fetched.")
        return

    print("Raw Emails:", raw_emails)  # Debugging output

    # Step 3: Process raw emails (clean data)
    processed_emails = process_data(raw_emails)
    if not processed_emails:
        print("No emails to process.")
        return

    print("Processed Emails:", processed_emails)  # Debugging output

    # Step 4: Summarize email content using Mistral
    model = LocalModel("mistral")  # Initialize the model
    for email in processed_emails:
        subject = email.get("subject", "No Subject")
        body = email.get("body", "")
        
        if body.strip():  # Only summarize if the body exists
            print(f"Summarizing email with subject: {subject}")
            summary = model.summarize(body)
            email["summary"] = summary  # Add the summary to the email dictionary
        else:
            email["summary"] = "No body content to summarize."

    # Step 5: Display summarized emails
    print("Summarized Emails:")
    for email in processed_emails:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Summary: {email['summary']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
