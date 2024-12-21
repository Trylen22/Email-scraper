import json
from datetime import datetime

def generate_json_report(emails, output_file):
    """
    Generate a JSON report of the processed emails.

    Args:
        emails (list): A list of processed email dictionaries.
        output_file (str): The output file path for the JSON report.
    """
    report_data = {
        "report_generated_at": datetime.now().isoformat(),
        "email_count": len(emails),
        "emails": emails
    }
    
    try:
        with open(output_file, "w") as f:
            json.dump(report_data, f, indent=4)
        print(f"JSON report saved to {output_file}")
    except Exception as e:
        print(f"Error writing JSON report: {str(e)}")

def generate_html_report(processed_emails, output_file):
    """Generate a retro-styled HTML report with ASCII art."""
    
    # ASCII art for the header
    ascii_logo = r"""
    ______                _ __   _____                                
   / ____/___ ___  ____ _(_) /  / ___/______________ _____  ___  _____
  / __/ / __ `__ \/ __ `/ / /   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 / /___/ / / / / / /_/ / / /   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
/_____/_/ /_/ /_/\__,_/_/_/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                   /_/                  
    """

    # ASCII cat with raw string to handle backslashes
    ascii_cat = r"""
        /\_/\  
       ( o.o ) 
      > ^ <
    """

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Courier New', monospace;
                background-color: #0c0c0c;
                color: #cccccc;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
            }}
            .ascii-art {{
                white-space: pre;
                font-family: monospace;
                display: block;
                color: #ffffff;
                margin: 20px auto;
                font-size: 14px;
                line-height: 1.2;
                width: fit-content;
                padding: 0;
            }}
            .email-container {{
                border: 1px solid #333;
                margin: 20px 0;
                padding: 20px;
                background-color: #111;
            }}
            .subject {{
                color: #ffffff;
                font-weight: bold;
                font-size: 1.2em;
                border-bottom: 1px solid #333;
                padding-bottom: 5px;
            }}
            .from {{
                color: #888;
                margin: 10px 0;
            }}
            .summary {{
                margin-top: 15px;
                padding: 10px;
                background-color: #161616;
                border-left: 3px solid #333;
            }}
            .timestamp {{
                color: #666;
                text-align: center;
                margin-top: 40px;
                font-size: 0.8em;
            }}
            .email-count {{
                text-align: center;
                color: #fff;
                margin: 20px 0;
                font-size: 1.2em;
            }}
            .ascii-border {{
                color: #333;
                margin: 10px 0;
                white-space: pre;
                overflow: visible;
                width: auto;
            }}
            .links {{
                margin-top: 15px;
                color: #888;
            }}
            .links a {{
                color: #666;
                text-decoration: none;
            }}
            .links a:hover {{
                color: #fff;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="ascii-art">{ascii_logo}</div>
            <div class="ascii-art">{ascii_cat}</div>
        </div>
        
        <div class="email-count">
            📧 Processed {len(processed_emails)} Emails
        </div>
        
        <div class="ascii-border">{'='*105}</div>
    """
    
    for i, email in enumerate(processed_emails, 1):
        html += f"""
        <div class="email-container">
            <div class="subject">📨 {email['subject'] or 'No Subject'}</div>
            <div class="from">From: {email['from']}</div>
            <div class="summary">{email['summary']}</div>
            
            {f'''
            <div class="links">
                <div class="ascii-border">{'─'*40}</div>
                {'<br>'.join(f'• {url}' for url in email['urls'])}
            </div>
            ''' if 'urls' in email and email['urls'] else ''}
        </div>
        """
    
    html += f"""
        <div class="timestamp">
            Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w') as f:
        f.write(html)

def generate_text_report(processed_emails, output_file):
    """Generate a human-readable text report of email summaries."""
    with open(output_file, 'w') as f:
        f.write("\n" + "="*105 + "\n")
        f.write("                                               EMAIL SUMMARY REPORT                                               \n")
        f.write("="*105 + "\n\n")
        
        for i, email in enumerate(processed_emails, 1):
            f.write(f"📧 Email {i}/{len(processed_emails)}\n")
            f.write("─"*105 + "\n")
            f.write(f"From    : {email['from']}\n")
            f.write(f"Subject : {email['subject']}\n")
            f.write("\nSummary:\n")
            f.write("─"*40 + "\n")
            # Wrap summary text at 100 characters instead of 80
            summary_lines = [email['summary'][i:i+100] for i in range(0, len(email['summary']), 100)]
            for line in summary_lines:
                f.write(f"{line}\n")
            
            if 'urls' in email and email['urls']:
                f.write("\nLinks Found:\n")
                f.write("─"*40 + "\n")
                for url in email['urls']:
                    f.write(f"• {url}\n")
            
            f.write("\n" + "="*105 + "\n\n")
