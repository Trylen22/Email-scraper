import logging
from scrape_emails import scrape_emails
from process_emails import process_data
from summarize import generate_summary

# Set up logging to keep track of the process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    # Step 1: Scrape Emails
    logging.info("Scraping emails...")
    raw_emails = scrape_emails()
    
    # Step 2: Process Emails
    logging.info("Processing emails...")
    processed_data = process_data(raw_emails)
    
    # Step 3: Generate Summaries
    logging.info("Generating summary...")
    summary = generate_summary(processed_data)
    
    # Step 4: Save Summary
    logging.info("Saving summary...")
    with open("reports/daily_summary.txt", "w") as file:
        file.write(summary)
    
    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()
