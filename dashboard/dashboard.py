import patch
from utils.config import Config

import dash_devices
from dash_devices.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from threading import Timer

app = dash_devices.Dash(__name__)

from websocket import create_connection
from datetime  import datetime
from time      import time
from pprint    import pprint
import logging as log
import json

TELEM = ['light', 'humidity' ]
LATENCY_THRESHOLD = 0.05

from layout import create_elements

class PlantDash:
    def __init__(self, app):
        self.config = Config()
        self.app   = app
        self.initial = {k : [0.0] * 1000 for k in TELEM}
        self.timer = None
        self.ws    = None
        self.count = 0
        self.pcount = 0
        self.start = datetime.now()

        self.app.layout = create_elements(app, TELEM)

        @app.callback(None, [dash_devices.dependencies.Input('command', 'n_clicks')],
                            [dash_devices.dependencies.State('input-on-submit', 'value'),
                             dash_devices.dependencies.State('actuator', 'value')
                                ])
        def command(n_clicks, value, actuator):
            self.command.send(json.dumps({actuator : value}))
            print(f'The input value was "{value}" and the button has been clicked {n_clicks} times')

        @self.app.callback_connect
        def func(client, connect):
            print(client, connect, len(app.clients))
            self.app.push_mods({'plant_map' : {'figure' : px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])}})
            if connect and len(app.clients) == 1:
                self.start = datetime.now()
                self.communication_loop()
            elif not connect and len(app.clients) == 0:
                self.timer.cancel()

    def ensure_connection(self):
        try:
            if self.ws is None:
                self.ws = create_connection(f'ws://{self.config.plantsitter_ip}:{self.config.plantsitter_port}/data')
                self.command = create_connection(f'ws://{self.config.plantsitter_ip}:{self.config.plantsitter_port}/command')
                print(f'Connection successfully established!', flush=True)
            else:
                pass
            return True
        except Exception as e:
            self.ws = None
            self.command = None
            print(f'Unable to establish websocket connection ({e}), retrying..', flush=True)
            return False

    def plot(self):
        figures = dict()
        for k in TELEM:
            data = self.initial[k]
            figure = px.line({'Time' : [i for i in range(len(data))], k.title() : data},
                x='Time',
                y=k.title(),
                range_y=[0, 1]
            )
            figures[f'{k}_graph'] = {'figure' : figure}
        self.pcount += 1
        return figures

    def update(self, telem):
        for k in TELEM:
            data = self.initial[k]
            data.append(telem[k])
            data.pop(0)
            self.initial[k] = data
        self.count += 1

    def communication_loop(self):
        if self.ensure_connection():
            telem = json.loads(self.ws.recv())
            pprint(telem)
            self.update(telem)
            now     = datetime.now()
            latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
            duration = (now - self.start).total_seconds()
            rrate   = self.count / duration
            prate   = self.pcount / duration

            light    = telem['light']
            humidity = telem['humidity']

            while latency > LATENCY_THRESHOLD:
                telem = json.loads(self.ws.recv())
                self.update(telem)
                latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
            latency = max(0, latency)
            figures = self.plot()
            self.app.push_mods({
                'latency'  : {'children': [html.H6('Latency:'),      f'{latency:.4f}s']},
                'rrate'    : {'children': [html.H6('Receive Rate:'), f'{rrate:.2f}hz']},
                'prate'    : {'children': [html.H6('Plot Rate:'),    f'{prate:.2f}hz']},
                'light'    : {'children': [html.H6('Light:'),        f'{light:.2f}']},
                'humidity' : {'children': [html.H6('Humidity:'),     f'{humidity:.2f}hz']},
                **figures,
            })
            self.timer = Timer(0.01, self.communication_loop)
        else:
            no_conn = {k : {'children' : [html.H6('No Connection')]} for k in ['latency', 'rrate', 'prate', 'light', 'humidity']}
            self.app.push_mods(no_conn)
            self.timer = Timer(1.00, self.communication_loop)
        self.timer.start()


if __name__ == '__main__':
    PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
