import patch
from utils.config import Config

from time import time, sleep
from pprint import pprint

from twilio.rest import Client

# Twilio SMS implementation is from their documentation:
# https://www.twilio.com/docs

class TextClient:
    def __init__(self):
        self.config = Config()
        self.client = Client(config.twilio_sid, config.twilio_token)

    def text(self, message='Hello World!'):
        message = self.client.messages.create(
                   body=message,
                   from_=self.config.from_number,
                   to=self.config.to_number)

if __name__ == '__main__':
    client = TextClient()
    client.text()
