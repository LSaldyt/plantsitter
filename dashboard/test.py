from websocket import create_connection
from pprint import pprint
from config import Config

from time import time

if __name__ == '__main__':
    config = Config()
    ws = create_connection(f'ws://{config.plantsitter_ip}:{config.plantsitter_port}/data')
    count = 0
    start = time()
    while True:
        pprint(ws.recv())
        count += 1
        end = time()
        print(f'{count/(end-start):.2f} hz')
