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
import json

# TELEM = ['light', 'humidity' , 'rain', 'moisture']
TELEM = ['light']
LATENCY_THRESHOLD = 0.05

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

        elements = [html.H1('Plantsitter'),
                    html.Br(), html.Div(id='latency', children=['Latency: 0s']),
                    html.Br(), html.Div(id='rrate', children=['Receive Rate: 0hz']),
                    html.Br(), html.Div(id='prate', children=['Plot Rate: 0hz']),
                    html.Br()
                    ]
        for k in TELEM:
            elements.append(html.Div(f'{k.title()} Measurement'))
            elements.append(dcc.Graph(id=f'{k}_graph'))
        self.app.layout = html.Div(elements)

        @self.app.callback_connect
        def func(client, connect):
            print(client, connect, len(app.clients))
            if connect and len(app.clients) == 1:
                self.start = datetime.now()
                self.timer_callback()
            elif not connect and len(app.clients) == 0:
                self.timer.cancel()

    def initialize(self):
        self.ws = create_connection(f'ws://{self.config.plantsitter_ip}:{self.config.plantsitter_port}/data')

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

    def timer_callback(self):
        if self.ws is None:
            self.initialize()
        telem = json.loads(self.ws.recv())
        self.update(telem)
        now     = datetime.now()
        latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
        duration = (now - self.start).total_seconds()
        rrate   = self.count / duration
        prate   = self.pcount / duration

        while latency > LATENCY_THRESHOLD:
            telem = json.loads(self.ws.recv())
            self.update(telem)
            latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
        figures = self.plot()
        self.app.push_mods({
            'latency' : {'children' : f'Latency: {latency:.4f}s'},
            'rrate'   : {'children' : f'Receive Rate: {rrate:.2f}hz'},
            'prate'   : {'children' : f'Plot Rate: {prate:.2f}hz'},
            **figures,
        })

        self.timer = Timer(0.01, self.timer_callback)
        self.timer.start()


if __name__ == '__main__':
    PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
