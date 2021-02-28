from websocket import create_connection
from pprint import pprint
from config import Config

if __name__ == '__main__':
    config = Config()
    ws = create_connection(f'ws://{config.plantsitter_ip}:{config.plantsitter_port}/data')
    while True:
        pprint(ws.recv())
