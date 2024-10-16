try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    print("All imports succeeded.")
except ImportError as e:
    print(f"Import failed: {e}")
