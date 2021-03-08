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

        elements = [html.Div(
                        [
                            html.Div(
                                [
                                    html.Img(
                                        src=app.get_asset_url('asu_logo_alt.png'),
                                        id="plotly-image",
                                        style={
                                            "height": "100px",
                                            "width": "auto",
                                            "margin-bottom": "25px",
                                        },
                                    )
                                ],
                                className="one-third column",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H3(
                                                'PlantSitter',
                                                style={"margin-bottom": "0px"},
                                            ),
                                            html.H5(
                                                'Raspberry-Pi Based Live Agriculture Monitoring', style={"margin-top": "0px"}
                                            ),
                                            html.H6(
                                                'By Lucas Saldyt', style={"margin-top": "0px"}
                                            ),

                                        ]
                                    )
                                ],
                                className="one-half column",
                                id="title",
                            ),
                            html.Div(
                                [
                                ],
                                className="one-third column",
                                id="button",
                            ),
                        ],
                        id="header",
                        className="row flex-display",
                        style={"margin-bottom": "25px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H4('Settings'),
                                    dcc.Dropdown(
                                        id='plant_select',
                                        options=[dict(label='Agave',    value='Agave'),
                                                 dict(label='Rosemary', value='Rosemary')],
                                        multi=True,
                                        value=['Agave', 'Rosemary'],
                                        className="dcc_control",
                                    ),
                                ],
                                className="pretty_container four columns",
                                id="cross-filter-options",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                [html.H6('Latency', id='latency_text')],
                                                id='latency',
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                [html.H6('Receive Rate', id='rrate_text')],
                                                id='rrate',
                                                className="mini_container",
                                            ),
                                            html.Div(
                                                ['Plotting Rate', html.H6(id='prate_text')],
                                                id='prate',
                                                className="mini_container",
                                            ),
                                        ],
                                        id="info-container",
                                        className="row container-display",
                                    ),
                                    html.Div(
                                        [dcc.Graph(id="count_graph")],
                                        id="countGraphContainer",
                                        className="pretty_container",
                                    ),
                                ],
                                id="right-column",
                                className="eight columns",
                            ),
                        ],
                        className="row flex-display",
                    ),
                    html.Br(),
                    html.Div(dcc.Input(id='input-on-submit', type='text')),
                    html.Button('Submit', id='command', n_clicks=0)
                    ]
        for k in TELEM:
            elements.append(html.Div(f'{k.title()} Measurement'))
            elements.append(dcc.Graph(id=f'{k}_graph'))
        self.app.layout = html.Div(elements)

        @app.callback(None, [dash_devices.dependencies.Input('command', 'n_clicks')],
                            [dash_devices.dependencies.State('input-on-submit', 'value')])
        def command(n_clicks, value):
            self.command.send(json.dumps({'pump' : 4.0}))
            print(f'The input value was "{value}" and the button has been clicked {n_clicks} times')

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

            while latency > LATENCY_THRESHOLD:
                telem = json.loads(self.ws.recv())
                self.update(telem)
                latency = (now - datetime.fromtimestamp(telem['timestamp'])).total_seconds()
            figures = self.plot()
            self.app.push_mods({
                'latency' : {'children': [html.H6('Latency:'),      f'{latency:.4f}s']},
                'rrate'   : {'children': [html.H6('Receive Rate:'), f'{rrate:.2f}hz']},
                'prate'   : {'children': [html.H6('Plot Rate:'),    f'{prate:.2f}hz']},
                **figures,
            })
            self.timer = Timer(0.01, self.communication_loop)
        else:
            self.app.push_mods({
                'latency' : {'children': [html.H6('No Connection')]},
                'rrate'   : {'children': [html.H6('No Connection')]},
                'prate'   : {'children': [html.H6('No Connection')]}})
            self.timer = Timer(1.00, self.communication_loop)
        self.timer.start()


if __name__ == '__main__':
    PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
