import json
from datetime import datetime
import re

def generate_json_report(emails, output_file):
    """Generate a JSON report of the processed emails."""
    report_data = {
        "report_generated_at": datetime.now().isoformat(),
        "email_count": len(emails),
        "emails": emails
    }
    
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        print(f"JSON report saved to {output_file}")
    except Exception as e:
        print(f"Error writing JSON report: {str(e)}")

def calculate_email_priority(email):
    """Calculate email priority using a multi-factor analysis system."""
    class EmailPriorityAnalyzer:
        def __init__(self):
            # Time-sensitive patterns with weights
            self.time_patterns = {
                r'\b(due|deadline)\s*(today|tomorrow|in\s*\d+\s*days?)': 10,
                r'\b(today|tomorrow)\b': 8,
                r'\b(this|next)\s*(week|monday|tuesday|wednesday|thursday|friday)\b': 6,
                r'\basap\b': 7,
                r'\bwithin\s*\d+\s*(day|hour|minute)s?\b': 8
            }
            
            # Sender importance patterns
            self.sender_patterns = {
                r'@.*\.(edu|ac\.[a-z]{2})$': 5,  # Academic email domains
                r'\b(professor|prof\.|dr\.|instructor|advisor)\b': 6,
                r'\b(dean|chairman|department|faculty)\b': 7,
                r'\b(registrar|bursar|financial\s*aid)\b': 8,
                r'(no-?reply|automated|system)': -2  # Lower priority for automated emails
            }
            
            # Content importance indicators
            self.content_weights = {
                'academic': {
                    'exam': 9, 'test': 8, 'quiz': 7, 'midterm': 9, 'final': 9,
                    'grade': 8, 'assignment': 7, 'homework': 6, 'project': 7,
                    'registration': 8, 'enroll': 7, 'withdraw': 8, 'drop': 7,
                    'thesis': 8, 'dissertation': 8, 'defense': 8,
                    'scholarship': 8, 'grant': 7, 'funding': 7
                },
                'administrative': {
                    'deadline': 8, 'required': 6, 'mandatory': 7, 'important': 6,
                    'payment': 8, 'tuition': 8, 'fee': 7, 'balance': 7,
                    'violation': 8, 'warning': 7, 'conduct': 7
                },
                'opportunities': {
                    'internship': 5, 'job': 5, 'position': 4, 'opportunity': 4,
                    'research': 6, 'assistant': 5, 'volunteer': 3
                },
                'engagement': {
                    'meeting': 4, 'event': 2, 'workshop': 3, 'seminar': 3,
                    'club': 2, 'social': 1, 'party': 1
                },
                'promotional': {
                    'offer': -3, 'discount': -3, 'sale': -3, 'subscribe': -4,
                    'upgrade': -3, 'premium': -3, 'limited time': -3, 'deal': -3
                }
            }

        def analyze_time_sensitivity(self, text):
            """Analyze time sensitivity in email content."""
            score = 0
            for pattern, weight in self.time_patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    score += weight
            return score

        def analyze_sender(self, sender):
            """Analyze importance based on sender information."""
            score = 0
            for pattern, weight in self.sender_patterns.items():
                if re.search(pattern, sender, re.IGNORECASE):
                    score += weight
            return score

        def analyze_content(self, text):
            """Analyze content importance using weighted keyword categories."""
            score = 0
            text_lower = text.lower()
            
            # Track matched categories to avoid double-counting
            category_matches = set()
            
            for category, keywords in self.content_weights.items():
                category_score = 0
                for keyword, weight in keywords.items():
                    if keyword in text_lower:
                        category_score += weight
                        category_matches.add(category)
                
                # Apply category-based multipliers
                if category in category_matches:
                    if category == 'academic':
                        category_score *= 1.2  # Boost academic content
                    elif category == 'promotional':
                        category_score *= 1.5  # Strengthen promotional penalties
                
                score += category_score
            
            return score

        def calculate_priority(self, email_data):
            """Calculate final priority score using all factors."""
            text = f"{email_data.get('subject', '')} {email_data.get('summary', '')}"
            sender = email_data.get('from', '')
            
            # Calculate individual scores
            time_score = self.analyze_time_sensitivity(text)
            sender_score = self.analyze_sender(sender)
            content_score = self.analyze_content(text)
            
            # Calculate total score with weights
            total_score = (
                time_score * 1.2 +    # Time sensitivity is important
                sender_score * 1.0 +   # Sender importance
                content_score * 1.1    # Content relevance
            )
            
            # Add logging for debugging
            print(f"\nPriority Analysis for: {email_data.get('subject', 'No Subject')}")
            print(f"From: {sender}")
            print(f"Time Score: {time_score:.2f}")
            print(f"Sender Score: {sender_score:.2f}")
            print(f"Content Score: {content_score:.2f}")
            print(f"Total Score: {total_score:.2f}")
            
            # Determine priority level with exact thresholds
            priority = (
                'HIGH' if total_score >= 25 else
                'MEDIUM' if total_score >= 10 else
                'LOW'
            )
            print(f"Final Priority: {priority}\n")
            
            return priority

    # Create a single analyzer instance for consistency
    analyzer = EmailPriorityAnalyzer()
    return analyzer.calculate_priority(email)

def generate_html_report(processed_emails, output_file):
    """Generate a retro-styled HTML report with ASCII art and priority-based grouping."""
    
    # Group emails by priority using the new algorithm
    priority_groups = {
        'HIGH': [],
        'MEDIUM': [],
        'LOW': []
    }
    
    for email in processed_emails:
        priority = calculate_email_priority(email)
        priority_groups[priority].append(email)

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
        <meta charset="utf-8">
        <style>
            :root {{
                --main-bg: #000000;
                --secondary-bg: #0a0a0a;
                --card-bg: #111111;
                --rose-pink: #FF69B4;
                --rose-pink-dim: #cc5490;
                --text-primary: #FF69B4;
                --text-secondary: #cc5490;
                --priority-high: #ff1493;    /* Deep pink */
                --priority-medium: #db7093;  /* Pale violet red */
                --priority-low: #ffb6c1;     /* Light pink */
            }}
            
            body {{
                font-family: 'Courier New', monospace;
                background-color: var(--main-bg);
                color: var(--text-secondary);
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }}
            
            .header {{
                text-align: center;
                margin-bottom: 40px;
                background-color: var(--main-bg);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(255, 105, 180, 0.1);
                border: 1px solid var(--text-secondary);
            }}
            
            .ascii-art {{
                white-space: pre;
                font-family: monospace;
                display: block;
                color: var(--text-primary);
                margin: 20px auto;
                font-size: 14px;
                line-height: 1.2;
                text-shadow: 0 0 10px rgba(255, 105, 180, 0.3);
            }}
            
            .priority-section {{
                flex: 1;
                background-color: var(--card-bg);
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(255, 105, 180, 0.1);
                overflow: hidden;
                transition: all 0.3s ease;
                border: 1px solid var(--text-secondary);
            }}
            
            .priority-section:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(255, 105, 180, 0.2);
            }}
            
            .high-priority .priority-header {{
                background-color: var(--priority-high);
                color: var(--main-bg);
            }}
            
            .medium-priority .priority-header {{
                background-color: var(--priority-medium);
                color: var(--main-bg);
            }}
            
            .low-priority .priority-header {{
                background-color: var(--priority-low);
                color: var(--main-bg);
            }}
            
            .email-container {{
                margin: 10px;
                padding: 15px;
                background-color: var(--secondary-bg);
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.2s ease;
                border-left: 3px solid var(--text-secondary);
            }}
            
            .email-container:hover {{
                transform: translateX(5px);
                background-color: var(--card-bg);
                border-left-color: var(--text-primary);
            }}
            
            .subject {{
                color: var(--text-primary);
                font-weight: bold;
                margin-bottom: 10px;
                padding-bottom: 5px;
                border-bottom: 1px solid var(--text-secondary);
            }}
            
            .from {{
                color: #888;
                font-size: 0.9em;
                margin-bottom: 15px;
                padding-left: 10px;
            }}
            
            .summary {{
                color: var(--text-secondary);
                line-height: 1.4;
                padding: 10px;
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 3px;
            }}
            
            .email-link {{
                color: var(--text-primary);
                text-decoration: none;
                border-bottom: 1px dotted var(--text-primary);
            }}
            
            .email-link:hover {{
                opacity: 0.8;
            }}
            
            .terminal-line {{
                color: var(--text-primary);
                margin: 10px 0;
                opacity: 0.8;
            }}
            
            .terminal-line::before {{
                content: ">";
                margin-right: 10px;
                color: var(--text-primary);
            }}
            
            .email-count {{
                text-align: center;
                color: var(--text-primary);
                margin: 20px 0;
                font-size: 1.2em;
                text-shadow: 0 0 10px rgba(255, 105, 180, 0.3);
            }}
            
            ::-webkit-scrollbar {{
                width: 8px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: var(--secondary-bg);
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: var(--text-secondary);
                border-radius: 4px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: var(--text-primary);
            }}
            
            .priority-container {{
                display: flex;
                justify-content: space-between;
                gap: 20px;
                margin: 30px 0;
            }}
            .priority-header {{
                padding: 15px;
                font-weight: bold;
                text-align: center;
                cursor: pointer;
                user-select: none;
                position: relative;
                border-bottom: 2px solid #222;
            }}
            .priority-header::after {{
                content: '▼';
                position: absolute;
                right: 15px;
                transition: transform 0.3s ease;
            }}
            .priority-section.expanded .priority-header::after {{
                transform: rotate(180deg);
            }}
            .email-list {{
                max-height: 0;
                overflow: hidden;
                transition: max-height 0.5s ease;
            }}
            .priority-section.expanded .email-list {{
                max-height: 600px;
                overflow-y: auto;
            }}
            .email-container.expanded .summary {{
                display: block;
            }}
        </style>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                document.querySelectorAll('.priority-header').forEach(header => {{
                    header.addEventListener('click', function() {{
                        const section = this.parentElement;
                        section.classList.toggle('expanded');
                    }});
                }});

                document.querySelectorAll('.email-container').forEach(container => {{
                    container.addEventListener('click', function(e) {{
                        if (!e.target.closest('.summary')) {{
                            this.classList.toggle('expanded');
                        }}
                    }});
                }});
            }});
        </script>
    </head>
    <body>
        <div class="header">
            <div class="ascii-art">{ascii_logo}</div>
            <div class="ascii-art">{ascii_cat}</div>
        </div>
        
        <div class="email-count">
            >> Processed {len(processed_emails)} Emails
        </div>
        
        <div class="terminal-line">System initialized...</div>
        <div class="terminal-line">Sorting by priority...</div>
        
        <div class="priority-container">
    """
    
    # Add priority sections
    for priority in ['HIGH', 'MEDIUM', 'LOW']:
        emails = priority_groups[priority]
        html += f"""
            <div class="priority-section {priority.lower()}-priority">
                <div class="priority-header">{priority} Priority ({len(emails)})</div>
                <div class="email-list">
        """
        
        for email in emails:
            html += f"""
                    <div class="email-container">
                        <div class="subject">>> {email['subject'] or 'No Subject'}</div>
                        <div class="from">From: {email['from']}</div>
                        <div class="summary">
                            {email['summary'].replace('[', '<span class="email-link">[').replace(']', ']</span>')}
                        </div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

def generate_text_report(processed_emails, output_file):
    """Generate a human-readable text report of email summaries."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n" + "="*105 + "\n")
        f.write("                                               EMAIL SUMMARY REPORT                                               \n")
        f.write("="*105 + "\n\n")
        
        for i, email in enumerate(processed_emails, 1):
            f.write(f">> Email {i}/{len(processed_emails)}\n")
            f.write("─"*105 + "\n")
            f.write(f"From    : {email['from']}\n")
            f.write(f"Subject : {email['subject']}\n")
            f.write("\nSummary:\n")
            f.write("─"*40 + "\n")
            summary_lines = [email['summary'][i:i+100] for i in range(0, len(email['summary']), 100)]
            for line in summary_lines:
                f.write(f"{line}\n")
            
            f.write("\n" + "="*105 + "\n\n")
