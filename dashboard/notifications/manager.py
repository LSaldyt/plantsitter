
from .text  import TextClient
from .email import EmailClient

class NotificationManager:
    def __init__(self):
        try:
            self.text  = TextClient()
        except:
            print('Could not create Twilio text client. Check config.json')
        try:
            self.email = EmailClient()
        except:
            print('Could not create Google Email client. Check config.json, credentials.json, and token.json.')
