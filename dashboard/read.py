from websocket import create_connection

ws = create_connection('ws://10.42.0.74:5000/data')
while True:
    print(ws.recv())
