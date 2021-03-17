import patch
from utils.config import Config

from time import time, sleep
from pprint import pprint

import os
from twilio.rest import Client

if __name__ == '__main__':
    config = Config()
    client = Client(config.twilio_sid, config.twilio_token)
    message = client.messages.create(
               body='Hello!',
               from_=config.from_number,
               to=config.to_number)
    print(message.sid)

