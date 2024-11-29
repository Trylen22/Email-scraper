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

# Placeholder for an HTML report generator (can be implemented later)
def generate_html_report(emails, output_file):
    """
    Generate an HTML report of the processed emails.
    
    Args:
        emails (list): A list of processed email dictionaries.
        output_file (str): The output file path for the HTML report.
    """
    print("HTML report generation is not yet implemented.")
