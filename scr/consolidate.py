import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticates and returns the Gmail service object."""
    creds = None
    # Check if `token.json` already exists (for storing access and refresh tokens)
    if os.path.exists('token.json'):
        print("Loading credentials from token.json...")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no valid credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("No valid credentials found. Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)  # Ensure port matches your registered redirect URIs
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the Gmail service object
        service = build('gmail', 'v1', credentials=creds)
        print("Gmail API service created successfully")
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def list_messages(service, user_id='me', max_results=5):
    """List the latest messages in the user's inbox."""
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = response.get('messages', [])

        if not messages:
            print("No messages found.")
            return

        print(f"Found {len(messages)} messages:")
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            msg_snippet = msg.get('snippet', '')
            msg_subject = next(
                (header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'),
                "No Subject"
            )
            print(f"Subject: {msg_subject}")
            print(f"Snippet: {msg_snippet}\n")
            print("-" * 50)
    except Exception as error:
        print(f"An error occurred: {error}")

def main():
    # Authenticate and get the Gmail service object
    service = authenticate_gmail()
    if service:
        # Fetch and display the latest emails
        list_messages(service)
    else:
        print("Failed to connect to Gmail.")

if __name__ == '__main__':
    main()
