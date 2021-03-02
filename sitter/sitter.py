from quart import Quart, websocket

app = Quart(__name__)

from time    import sleep, time
from pprint  import pprint

from sensors import initialize_sensors
from influx  import SeriesDatabase
from system  import snapshot

import asyncio

# SPEC    = dict(light=4, humidity=17, rain=18, moisture=27)
SPEC    = dict(probe=6)
SENSORS = initialize_sensors(SPEC)
LOCK    = asyncio.Lock()

# time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),

conn = SeriesDatabase()
#conn.insert(dict(temp=70))
# print(conn.get('temp'))

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
