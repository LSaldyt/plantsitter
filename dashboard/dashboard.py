import patch
from utils.config import Config

import dash_devices
from dash_devices.dependencies import Input, Output, State
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

        self.plants = []

        self.app.layout = create_elements(app, TELEM)

        @app.callback(None, [Input('command', 'n_clicks')],
                            [State('input-on-submit', 'value'),
                             State('actuator', 'value')
                                ])
        def command(n_clicks, value, actuator):
            self.command.send(json.dumps({actuator : value}))
            print(f'The input value was "{value}" and the button has been clicked {n_clicks} times')


        @app.callback(
                [Output('plant_map', 'figure'),
                 Output('plant_select', 'value'),
                 Output('plant_select', 'options')],
                [Input('add_plant', 'n_clicks')],
                [State('add_plant', 'value'),
                 State('plant_name', 'value'),
                 State('x_coordinate', 'value'),
                 State('y_coordinate', 'value'),
                 State('plant_select', 'value'),
                 State('plant_select', 'options')])
        def add_plant(n_clicks, button_value, plant_name, x, y, plant_vals, plant_options):
            print(f'Adding plant!!: {plant_name} ({x}, {y})')
            self.plants.append((plant_name, x, y))
            plant_vals.append(plant_name)
            plant_options.append({'label' : plant_name, 'value' : plant_name})
            fig = px.scatter(x=[p[1] for p in self.plants], y=[p[2] for p in self.plants], text=[p[0] for p in self.plants])
            fig.update_layout(title_text='Plant Locations')
            return fig, plant_vals, plant_options

        @self.app.callback_connect
        def func(client, connect):
            print(client, connect, len(app.clients))
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
                'receive_rate'    : {'children': [html.H6('Receive Rate:'), f'{rrate:.2f}hz']},
                'plot_rate'    : {'children': [html.H6('Plot Rate:'),    f'{prate:.2f}hz']},
                'light'    : {'children': [html.H6('Light:'),        f'{light:.2f}']},
                'humidity' : {'children': [html.H6('Humidity:'),     f'{humidity:.2f}hz']},
                **figures,
            })
            self.timer = Timer(0.05, self.communication_loop)
        else:
            no_conn = {k : {'children' : [html.H6('No Connection')]} for k in ['latency', 'receive_rate', 'plot_rate', 'light', 'humidity']}
            self.app.push_mods(no_conn)
            self.timer = Timer(1.00, self.communication_loop)
        self.timer.start()


if __name__ == '__main__':
    PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
