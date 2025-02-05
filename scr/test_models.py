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
import re

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

class StudentPrioritySystem:
    def __init__(self):
        # Define priority weights for different categories
        self.priority_weights = {
            'HIGH': {
                'deadlines': 10,    # Assignment due dates, exam dates
                'grades': 10,       # Grade releases, grade changes
                'exams': 10,        # Tests, midterms, finals
                'urgent': 8,        # Time-sensitive matters
                'registration': 8,  # Course registration, drop deadlines
            },
            'MEDIUM': {
                'assignments': 6,   # Homework, projects
                'office_hours': 5,  # Professor/TA office hours
                'study_group': 5,   # Study sessions
                'class_changes': 5, # Room changes, time changes
                'materials': 4,     # Course materials, readings
            },
            'LOW': {
                'events': 2,        # Campus events, club meetings
                'announcements': 1, # General announcements
                'optional': 1,      # Optional activities
            }
        }

        # Keywords associated with each category [ can change for updated student priorities ]
        self.keyword_mapping = {
            'deadlines': ['due', 'deadline', 'submit', 'submission'],
            'grades': ['grade', 'score', 'result', 'marks', 'gpa'],
            'exams': ['exam', 'test', 'quiz', 'midterm', 'final', 'assessment'],
            'urgent': ['urgent', 'immediate', 'asap', 'important'],
            'registration': ['register', 'enrollment', 'drop', 'add/drop'],
            'assignments': ['assignment', 'homework', 'project', 'paper', 'essay'],
            'office_hours': ['office hours', 'consultation', 'meeting'],
            'study_group': ['study group', 'study session', 'group work'],
            'class_changes': ['room change', 'reschedule', 'canceled', 'postponed'],
            'materials': ['textbook', 'reading', 'material', 'slides', 'notes'],
            'events': ['event', 'seminar', 'workshop', 'club'],
            'announcements': ['announce', 'inform', 'notice'],
            'optional': ['optional', 'voluntary', 'extra credit']
        }

    def calculate_priority(self, email_text: str) -> tuple[str, float]:
        email_text = email_text.lower()
        max_score = 0
        total_score = 0
        
        # Calculate score based on keyword matches
        for category, keywords in self.keyword_mapping.items():
            for keyword in keywords:
                if keyword in email_text:
                    # Find which priority level this category belongs to
                    for priority, categories in self.priority_weights.items():
                        if category in categories:
                            score = categories[category]
                            total_score += score
                            max_score = max(max_score, score)

        # Determine priority based on highest matching score
        if max_score >= 8:
            return 'HIGH', total_score
        elif max_score >= 4:
            return 'MEDIUM', total_score
        else:
            return 'LOW', total_score

def test_model(model_name, text):
    """Test a specific model with given text using automated student priorities."""
    priority_system = StudentPrioritySystem()
    suggested_priority, score = priority_system.calculate_priority(text)
    
    prompt = f"""SYSTEM: You are an email classifier for a student. Analyze this email considering student priorities.
The system suggests this is a [{suggested_priority}] priority email.

Provide a structured response:
1. Priority Level: [HIGH], [MEDIUM], or [LOW]
2. Summary: Brief factual summary of the main point
3. Key Details: Important information from the email
4. Action Items: Any required actions or responses

Email:
{text}"""

    try:
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        # Clean up the response by removing the thinking section
        response = result.stdout.strip()
        
        # Remove everything between <think> tags (including the tags)
        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        
        # Remove any extra blank lines that might remain
        cleaned_response = '\n'.join(line for line in cleaned_response.split('\n') if line.strip())
        
        return cleaned_response
    
    except subprocess.TimeoutExpired:
        return "Error: Model response timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Test different LLMs with mock emails")
    parser.add_argument("--model", type=str, required=True, help="Name of the Ollama model to test")
    parser.add_argument("--sort", action="store_true", help="Sort emails by priority and relevance")
    args = parser.parse_args()

    priority_system = StudentPrioritySystem()
    results = []
    
    print("\n" + "="*100)
    print(f"{'STARTING MODEL TESTING SESSION':^100}")
    print(f"{'Using model: ' + args.model:^100}")
    print("="*100 + "\n")
    
    for i, email in enumerate(TEST_EMAILS, 1):
        priority, score = priority_system.calculate_priority(email)
        response = test_model(args.model, email)
        results.append((priority, score, i, email, response))
    
    if args.sort:
        # Sort first by priority level, then by score within each priority
        priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
        sorted_results = sorted(results, 
                              key=lambda x: (priority_order.get(x[0], 3), -x[1]))
        
        # Display sorted results
        for priority, score, i, email, response in sorted_results:
            print(f"\nPRIORITY: [{priority}] (Relevance Score: {score:.1f}) - EMAIL #{i}")
            print("─"*100)
            # Format email content with indentation
            formatted_email = "\n".join(f"    {line}" for line in email.strip().split('\n'))
            print(formatted_email)
            
            print("\nMODEL RESPONSE")
            print("─"*100)
            print(response)
            print("\n" + "="*100)

    print(f"\n{'TESTING SESSION COMPLETE':^100}")
    print("="*100 + "\n")

if __name__ == "__main__":
    main() 