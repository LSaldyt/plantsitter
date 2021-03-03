from quart import Quart, websocket

from time    import sleep, time
from pprint  import pprint

from sensors import initialize_sensors
from system  import snapshot

import patch
from utils.influx  import SeriesDatabase

import asyncio

PROBES = [6, 13, 19, 26, 16, 21, 12, 5]
SPEC    = {f'moisture_{i}' : p for i, p in enumerate(PROBES)}
SPEC.update(dict(light=25, humidity=24))
SENSORS = initialize_sensors(SPEC)
LOCK    = asyncio.Lock()

conn = SeriesDatabase()

database_interval = 100
system_interval   = 10
@app.websocket('/data')
async def datasocket():
    count = 0
    buff  = []
    while True:
        count += 1
        async with LOCK:
            plantdata = {k : v.value for k, v in SENSORS.items()}
        if count % system_interval == 0:
            plantdata.update(snapshot())
        plantdata['timestamp'] = time()
        # time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        buff.append(plantdata)
        await websocket.send_json(plantdata)
        if count % database_interval == 0:
            conn.insert(buff)
            del buff[:]
        print(f'{count}\r', end='')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
