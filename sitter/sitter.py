from quart import Quart, websocket

from time    import sleep, time
from pprint  import pprint

from sensors import initialize_sensors
from system  import snapshot

import patch
from utils.influx  import SeriesDatabase

import asyncio

SPEC    = dict(probe=6)
SENSORS = initialize_sensors(SPEC)
LOCK    = asyncio.Lock()

app  = Quart(__name__)
conn = SeriesDatabase()

interval = 5

@app.websocket('/data')
async def datasocket():
    count = 0
    buff  = []
    while True:
        count += 1
        async with LOCK:
            plantdata = {k : v.value for k, v in SENSORS.items()}
            plantdata.update(snapshot())
            buff.append(plantdata)
            plantdata['timestamp'] = time()
            await websocket.send_json(plantdata)
        if count % interval == 0:
            pprint(buff)
            conn.insert(buff)
            del buff[:]

if __name__ == '__main__':
    app.run(host='0.0.0.0')
