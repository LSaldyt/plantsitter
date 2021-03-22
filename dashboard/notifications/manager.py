
from .text  import TextClient
from .email import EmailClient

class NotificationManager:
    def __init__(self):
        self.text  = TextClient()
        self.email = EmailClient()
