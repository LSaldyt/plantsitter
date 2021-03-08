
import patch
import json
from utils.config import Config
from websocket import create_connection

from time import time, sleep
from pprint import pprint

if __name__ == '__main__':
    config = Config()
    data = create_connection(f'ws://{config.plantsitter_ip}:{config.plantsitter_port}/data')
    command = create_connection(f'ws://{config.plantsitter_ip}:{config.plantsitter_port}/command')
    count = 0
    start = time()
    while True:
        # pprint(data.recv())
        command.send(json.dumps({'pump' : 4.0}))
        break
        sleep(1)
        count += 1
        end = time()
        print(f'{count/(end-start):.2f} hz')
