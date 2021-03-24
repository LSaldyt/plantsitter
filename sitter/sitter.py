from quart import Quart, websocket
from multiprocessing import Process

from time    import sleep, time
from pprint  import pprint

from sensors import initialize_sensors
from system  import snapshot

import patch
from utils.influx  import SeriesDatabase

import asyncio

from motor import Motor

app = Quart(__name__)

PROBES = [6, 13, 19, 26, 16, 21, 12, 5]
SPEC    = {f'moisture_{i}' : p for i, p in enumerate(PROBES)}
SPEC.update(dict(light=25, humidity=24))
SENSORS = initialize_sensors(SPEC)
LOCK    = asyncio.Lock()

conn = SeriesDatabase()

database_interval = 100
system_interval   = 10

main = Motor(22, 23)
vertical   = Motor(18, 27)
horizontal = Motor(4, 17)

async def capture(i):
    async with LOCK:
        plantdata = {k : v.value for k, v in SENSORS.items()}
    if i % system_interval == 0:
        plantdata.update(snapshot())
    plantdata['timestamp'] = time()
    # time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
    return plantdata

@app.websocket('/data')
async def datasocket():
    count = 0
    while True:
        count += 1
        await websocket.send_json(await capture(count))

@app.websocket('/command')
async def commandsocket():
    while True:
        data = await websocket.receive_json()
        if 'main' in data:
            main.turn(abs(data['main']), data['main'] > 0)
        elif 'horizontal' in data:
            horizontal.turn(abs(data['horizontal']), data['horizontal'] > 0)
        elif 'vertical' in data:
            vertical.turn(abs(data['vertical']), data['vertical'] > 0)
        print(data, flush=True)

async def serializer():
    count = 0
    buff  = []
    while True:
        count += 1
        plantdata = await capture(count)
        buff.append(plantdata)
        if count % database_interval == 0:
            conn.insert(buff)
            del buff[:]
            print(f'Inserted Database Entry {count // database_interval}', flush=True)
            await asyncio.sleep(10.0)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
            asyncio.gather(
                app.run_task(host='0.0.0.0'),
                serializer()
                )
            )
