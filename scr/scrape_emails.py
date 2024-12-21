import base64
import re

def extract_urls(text):
    """Extract URLs from text and replace them with placeholders.
    
    This function significantly improves model processing performance by removing long URLs
    from the text. Testing showed a ~70% reduction in processing time (from 26s to 8s)
    when using URL extraction.
    """
    # URL pattern matching common URL formats
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Find all URLs
    urls = re.findall(url_pattern, text)
    
    # Replace URLs with placeholders and create clean text
    clean_text = text
    for i, url in enumerate(urls):
        clean_text = clean_text.replace(url, f'<link{i+1}>')
    
    return clean_text, urls

def fetch_emails(service, user_id='me', max_results=10):
    """Fetches emails using Gmail API."""
    try:
        # Retrieve message IDs
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = response.get('messages', [])
        
        if not messages:
            print("No messages found.")
            return []

        emails = []
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            msg_payload = msg.get('payload', {})
            headers = msg_payload.get('headers', [])

            # Extract subject and sender from headers
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), "No Subject")
            sender = next((header['value'] for header in headers if header['name'] == 'From'), "Unknown Sender")

            # Extract body with better encoding handling
            body = ""
            if 'parts' in msg_payload:
                for part in msg_payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        body = part.get('body', {}).get('data', "")
                        break
            else:
                body = msg_payload.get('body', {}).get('data', "")

            # Decode body with error handling
            try:
                if body:
                    # First decode base64
                    body_bytes = base64.urlsafe_b64decode(body)
                    # Try UTF-8 first
                    try:
                        body = body_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Fallback to more lenient encoding
                        body = body_bytes.decode('latin-1')
                else:
                    body = "No meaningful content."
            except Exception as e:
                print(f"Error decoding email body: {e}")
                body = "Error decoding content."

            # Clean the strings to remove problematic characters
            subject = ''.join(char for char in subject if ord(char) < 65536)
            sender = ''.join(char for char in sender if ord(char) < 65536)
            body = ''.join(char for char in body if ord(char) < 65536)

            # Extract and clean URLs from body
            clean_body, urls = extract_urls(body)

            emails.append({
                "subject": subject,
                "from": sender,
                "body": clean_body,
                "urls": urls  # Store the extracted URLs separately
            })

        return emails

    except Exception as e:
        print(f"An error occurred while fetching emails: {e}")
        return []
