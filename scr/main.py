#!/usr/bin/env python3
"""
Email Scraper - Main Application
-------------------------------
A sophisticated email processing system that fetches, analyzes, and generates
priority-based reports for student emails.

Author: Your Name
Version: 1.0.0
"""

import argparse
import time
from pathlib import Path
import platform
import subprocess
import os
import re
import webbrowser

# Local imports
from authemail import authenticate_gmail
from scrape_emails import fetch_emails
from process_emails import process_data
from report_generator import (
    generate_json_report,
    generate_html_report,
    generate_text_report
)
from ascii_art import (
    display_welcome_message,
    show_progress_bar,
    goodbye_message
)
from local_model import LocalModel


def open_file(filepath: Path) -> None:
    """Open a file with the default system application."""
    filepath = Path(filepath)
    if not filepath.exists():
        print(f"Error: File {filepath} not found!")
        return
    
    system = platform.system()
    try:
        if system == 'Darwin':       # macOS
            subprocess.run(['open', filepath])
        elif system == 'Windows':    # Windows
            os.startfile(filepath)
        else:                        # Linux
            subprocess.run(['xdg-open', filepath])
    except Exception as e:
        print(f"Error opening file: {e}")


def process_emails_with_model(processed_emails: list, model: LocalModel, debug: bool, clean_response: bool) -> None:
    """Process emails using the language model for summarization."""
    total_emails = len(processed_emails)
    for index, email in enumerate(processed_emails, 1):
        summary_start = time.time()
        subject = email.get("subject", "No Subject")
        body = email.get("body", "")
        
        if body.strip():
            print(f"\nSummarizing email [{index}/{total_emails}] - Subject: {subject}")
            summary = model.summarize(body)
            
            if clean_response:
                summary = re.sub(r'<think>.*?</think>', '', summary, flags=re.DOTALL)
                summary = '\n'.join(line for line in summary.split('\n') if line.strip())
                
            email["summary"] = summary
            
            if debug:
                print(f"Single email summary time: {time.time() - summary_start:.2f} seconds")
        else:
            email["summary"] = "No body content to summarize."


def generate_report(format_type: str, processed_emails: list, output_file: str) -> None:
    """Generate and display the report in the specified format."""
    if format_type == 'json':
        generate_json_report(processed_emails, output_file)
        print(f"\nJSON report saved to: {output_file}")
    elif format_type == 'html':
        generate_html_report(processed_emails, output_file)
        print(f"\nOpening HTML report in your browser...")
        webbrowser.open(f"file://{Path(output_file).absolute()}")
    else:  # text format
        generate_text_report(processed_emails, output_file)
        print(f"\nOpening text report...")
        open_file(output_file)


def main() -> None:
    """Main execution function for the email scraper application."""
    # Create reports directory if it doesn't exist
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)

    # Start total execution timer
    total_start_time = time.time()
    
    # Display welcome message
    display_welcome_message()

    # Parse command line arguments
    args = parse_arguments()

    # Set default output file if not specified
    if not args.output_file:
        args.output_file = str(reports_dir / f"email_report.{args.format}")
    else:
        args.output_file = str(reports_dir / Path(args.output_file).name)

    def debug_print(*print_args, **kwargs):
        if args.debug:
            print(*print_args, **kwargs)

    # Extract and validate arguments
    max_emails = max(1, min(args.max_emails, 50))
    query = args.query

    # Step 1: Authenticate Gmail
    auth_start = time.time()
    service = authenticate_gmail()
    auth_time = time.time() - auth_start
    debug_print(f"\nAuthentication time: {auth_time:.2f} seconds")
    
    if not service:
        print("Failed to authenticate Gmail.")
        goodbye_message()
        return

    # Step 2: Fetch raw emails
    fetch_start = time.time()
    raw_emails = fetch_emails(service, max_results=max_emails)
    fetch_time = time.time() - fetch_start
    debug_print(f"Email fetching time: {fetch_time:.2f} seconds")
    
    if not raw_emails:
        print("No emails fetched.")
        goodbye_message()
        return

    # Step 3: Process raw emails
    process_start = time.time()
    processed_emails = process_data(raw_emails)
    process_time = time.time() - process_start
    debug_print(f"Email processing time: {process_time:.2f} seconds")
    
    if not processed_emails:
        print("No emails to process.")
        goodbye_message()
        return

    # Step 4: Summarize emails using the model
    model = LocalModel("deepseek-r1:1.5b")
    summarize_start = time.time()
    process_emails_with_model(processed_emails, model, args.debug, args.r1)
    summarize_time = time.time() - summarize_start
    debug_print(f"\nTotal summarization time: {summarize_time:.2f} seconds")

    # Show progress bar for report generation
    show_progress_bar(total_steps=5, task="Generating report...")

    # Step 5: Generate and display the report
    report_start = time.time()
    generate_report(args.format, processed_emails, args.output_file)
    report_time = time.time() - report_start
    debug_print(f"Report generation time: {report_time:.2f} seconds")

    # Calculate and display total execution time
    total_time = time.time() - total_start_time
    
    if args.debug:
        debug_print(f"\nTotal execution time: {total_time:.2f} seconds")
        debug_print("\nTime breakdown:")
        debug_print(f"{'Authentication:':<20} {auth_time:>6.2f}s ({(auth_time/total_time)*100:>5.1f}%)")
        debug_print(f"{'Fetching:':<20} {fetch_time:>6.2f}s ({(fetch_time/total_time)*100:>5.1f}%)")
        debug_print(f"{'Processing:':<20} {process_time:>6.2f}s ({(process_time/total_time)*100:>5.1f}%)")
        debug_print(f"{'Summarization:':<20} {summarize_time:>6.2f}s ({(summarize_time/total_time)*100:>5.1f}%)")
        debug_print(f"{'Report Generation:':<20} {report_time:>6.2f}s ({(report_time/total_time)*100:>5.1f}%)")

    # Step 6: Display goodbye message
    goodbye_message()


def parse_arguments() -> argparse.Namespace:
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description="Email Scraper CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--max-emails",
        type=int,
        default=5,
        help="Maximum number of emails to fetch"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        choices=['json', 'html', 'text'],
        default='html',
        help="Output format"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file path (default: based on format)"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Optional query to filter emails"
    )
    
    parser.add_argument(
        "--r1",
        action="store_true",
        help="Clean model responses by removing thinking process"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help=argparse.SUPPRESS  # Hidden debug flag
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    main()