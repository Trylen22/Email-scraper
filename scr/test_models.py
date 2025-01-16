"""
Model Testing Instructions:
1. Visit: https://ollama.ai/library
2. Find models under 3B parameters
3. Open terminal and run: ollama pull <model_name>
   Example models:
   - tinyllama (1.1B)
   - phi (1.3B)
   - neural-chat (1.3B)
   - mistral-openorca (3B)

Usage:
python test_models.py --model <model_name>
Example: python test_models.py --model tinyllama
"""

import argparse
import subprocess

# Mock emails for testing
TEST_EMAILS = [
    """
    Subject: Quiz 2 Deadline Issue
    Dear Prof. Smith,
    I hope this email finds you well. I wanted to let you know that the quiz 2 deadline for one of my classes has not been adhered to. 
    Instead of closing earlier as planned, it was only open until today. However, I have corrected this issue and if you have any questions 
    about WeBWork, please don't hesitate to ask me in person.
    Best regards,
    Student
    """,
    
    """
    Subject: Office Hours This Week
    Hi Professor,
    Will you still be holding office hours this Thursday at 2pm? I'd like to discuss some concepts from last week's lecture.
    Thanks,
    Student
    """,
    
    """
    Subject: Campus Event Newsletter
    Dear Students,
    Join us this weekend for the annual Spring Festival! There will be food, music, and activities from 12-4pm on the quad.
    Best,
    Student Activities
    """,

    """
    Subject: Study Group Formation - Physics 201
    Hi Classmates,
    I'm organizing a study group for our upcoming midterm in Physics 201. We'll meet in the library every Tuesday and Thursday from 3-5pm.
    If you're interested in joining, please let me know. We'll focus on problem-solving and reviewing lecture materials.
    Best,
    Sarah
    """,
    
    """
    Subject: Campus WiFi Maintenance Notice
    Dear Students,
    This is a notification that campus WiFi will undergo routine maintenance this Sunday from 2am-4am.
    No action is required on your part, and service interruption should be minimal.
    Regards,
    IT Services
    """,
    
    """
    Subject: Student Discount Available
    Hello Students!
    Just a friendly reminder that you can get 10% off at the campus bookstore this week by showing your student ID.
    Sale ends Friday!
    Thanks,
    Campus Bookstore
    """
]

def test_model(model_name, text):
    """Test a specific model with given text."""
    prompt = f"""MUST FOLLOW THIS EXACT FORMAT:
[PRIORITY] One clear sentence summary.

Examples of correct responses:
[HIGH] Quiz deadline has been changed and requires immediate attention.
[MEDIUM] Professor's office hours scheduled for Thursday at 2pm.
[LOW] Campus bookstore offering 10% student discount this week.

Rules:
1. First line must start with [HIGH], [MEDIUM], or [LOW]
2. Follow with exactly one sentence summary
3. No extra text or explanations

Email to analyze:
{text}

Remember: Reply using ONLY the format [PRIORITY] One sentence summary."""

    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            text=True,
            capture_output=True
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        return result.stdout.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Test different LLMs with mock emails")
    parser.add_argument("--model", type=str, required=True, help="Name of the Ollama model to test")
    args = parser.parse_args()

    print("\n" + "="*100)
    print(f"{'STARTING MODEL TESTING SESSION':^100}")
    print(f"{'Using model: ' + args.model:^100}")
    print("="*100 + "\n")
    
    for i, email in enumerate(TEST_EMAILS, 1):
        print(f"\nTEST EMAIL #{i}")
        print("─"*100)
        # Format email content with indentation
        formatted_email = "\n".join(f"    {line}" for line in email.strip().split('\n'))
        print(formatted_email)
        
        print("\nMODEL RESPONSE")
        print("─"*100)
        response = test_model(args.model, email)
        print(response)
        print("\n" + "="*100)

    print(f"\n{'TESTING SESSION COMPLETE':^100}")
    print("="*100 + "\n")

if __name__ == "__main__":
    main() 