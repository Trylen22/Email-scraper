import argparse
from authemail import authenticate_gmail
from scrape_emails import fetch_emails
from process_emails import process_data
from report_generator import generate_json_report
from ascii_art import display_welcome_message, show_progress_bar, goodbye_message  # Corrected imports
from local_model import LocalModel

def main():
    # Display welcome message with ASCII art
    display_welcome_message()

    # Command-line arguments
    parser = argparse.ArgumentParser(description="Email Scraper CLI")
    parser.add_argument("--max-emails", type=int, default=5, help="Maximum number of emails to fetch (default: 5)")
    parser.add_argument("--output-file", type=str, default="email_report.json", help="Output file for the report")
    parser.add_argument("--query", type=str, default="", help="Optional query to filter emails")
    args = parser.parse_args()

    # Extract arguments
    max_emails = args.max_emails
    output_file = args.output_file
    query = args.query

    # Step 1: Authenticate Gmail
    service = authenticate_gmail()
    if not service:
        print("Failed to authenticate Gmail.")
        goodbye_message()
        return

    # Step 2: Fetch raw emails
    raw_emails = fetch_emails(service, max_results=max_emails,)
    if not raw_emails:
        print("No emails fetched.")
        goodbye_message()
        return

    # Step 3: Process raw emails
    processed_emails = process_data(raw_emails)
    if not processed_emails:
        print("No emails to process.")
        goodbye_message()
        return

    # Step 4: Summarize emails using the model
    model = LocalModel("mistral")
    for email in processed_emails:
        subject = email.get("subject", "No Subject")
        body = email.get("body", "")
        if body.strip():
            print(f"Summarizing email with subject: {subject}")
            email["summary"] = model.summarize(body)
        else:
            email["summary"] = "No body content to summarize."

    # Show progress bar for processing emails
    show_progress_bar(total_steps=5, task="Generating report...")

    # Step 5: Generate the report
    generate_json_report(processed_emails, output_file)

    # Step 6: Display a goodbye message
    goodbye_message()

if __name__ == "__main__":
    main()
