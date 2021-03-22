import patch
from utils.config import Config

from time import time, sleep
from pprint import pprint

import os


import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

import base64

# Email reference
# https://developers.google.com/gmail/api/guides/sending

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

class EmailClient:
    def __init__(self):
        self.config = Config()

        self.creds = self.ensure_credentials()
        self.service = build('gmail', 'v1', credentials=creds)

    def ensure_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds


    def email(self):
        message = MIMEText('Test')
        message['To']   = self.config.email
        message['From'] = self.config.email
        message['Subject'] = 'Subject'

        print(type(message.as_string()))
        body = {'raw' : base64.urlsafe_b64encode(message.as_string().encode('utf-8')).decode()}
        print(body)
        result = self.service.users().messages().send(userId=self.config.email, body=body).execute()
        print(result)
        print(dir(result))

if __name__ == '__main__':
    client = EmailClient()
    client.email()

