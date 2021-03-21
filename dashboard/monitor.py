import patch

import dash_devices
from dash_devices.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from threading import Timer

from websocket import create_connection
from datetime  import datetime
from time      import time
from pprint    import pprint
import logging as log
import json

from utils.config import Config

TELEM = ['light', 'humidity' ]
LATENCY_THRESHOLD = 0.05

class Monitor:
    def __init__(self, app, connections):
        self.config = Config()
        self.app = app
        self.initial = {k : [0.0] * 1000 for k in TELEM}
        self.count = 0
        self.pcount = 0
        self.start = datetime.now()

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

    def iterate(self, connections):
        conn = connections['data']
        telem = json.loads(conn.recv())
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
            telem = json.loads(conn.recv())
            self.update(telem)
            latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
        latency = max(0, latency)
        figures = self.plot()
        self.app.push_mods({
            'latency'  : {'children': [html.H6('Latency:'),      f'{latency:.4f}s']},
            'receive_rate'    : {'children': [html.H6('Receive Rate:'), f'{rrate:.2f}hz']},
            'plot_rate'    : {'children': [html.H6('Plot Rate:'),    f'{prate:.2f}hz']},
            'light'    : {'children': [html.H6('Light:'),        f'{light:.2f}']},
            'humidity' : {'children': [html.H6('Humidity:'),     f'{humidity:.2f}hz']},
            **figures,
        })

    def no_connection(self, connections):
        no_conn = {k : {'children' : [html.H6('No Connection')]} for k in ['latency', 'receive_rate', 'plot_rate', 'light', 'humidity']}
        self.app.push_mods(no_conn)
