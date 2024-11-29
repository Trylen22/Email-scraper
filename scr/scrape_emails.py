import base64

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

            # Extract body
            body = ""
            if 'parts' in msg_payload:
                for part in msg_payload['parts']:
                    if part.get('mimeType') == 'text/plain':
                        body = part.get('body', {}).get('data', "")
                        break
            else:
                body = msg_payload.get('body', {}).get('data', "")

            # Decode body
            import base64
            body = base64.urlsafe_b64decode(body).decode('utf-8', errors='ignore')

            emails.append({
                "subject": subject,
                "from": sender,
                "body": body
            })

        return emails

    except Exception as e:
        print(f"An error occurred while fetching emails: {e}")
        return []
