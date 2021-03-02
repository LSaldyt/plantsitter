from quart import Quart, websocket

app = Quart(__name__)

from time    import sleep, time
from sensors import initialize_sensors

import asyncio

# SPEC    = dict(light=4, humidity=17, rain=18, moisture=27)
SPEC    = dict(probe=6)
SENSORS = initialize_sensors(SPEC)
LOCK    = asyncio.Lock()

@app.websocket('/data')
async def datasocket():
    while True:
        async with LOCK:
            plantdata = {k : v.value for k, v in SENSORS.items()}
            plantdata['timestamp'] = time()
            await websocket.send_json(plantdata)
            sleep(0.01)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
