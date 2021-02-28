from config import Config

config = Config()

import dash_devices
from dash_devices.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from threading import Timer

app = dash_devices.Dash(__name__)

from websocket import create_connection
import json

class Example:
    def __init__(self, app):
        self.app   = app
        self.data  = [0.5] * 100
        self.timer = None
        self.ws    = None
        self.count = 0

        self.app.layout = html.Div([
            html.Div("Light Levels"),
            dcc.Graph(id='light_graph'),
        ])

        @self.app.callback_connect
        def func(client, connect):
            print(client, connect, len(app.clients))
            if connect and len(app.clients) == 1:
                self.timer_callback()
            elif not connect and len(app.clients) == 0:
                self.timer.cancel()

    def timer_callback(self):
        if self.ws is None:
            self.ws = create_connection('ws://10.42.0.74:5000/data')
        data = json.loads(self.ws.recv())
        # data = {'light' : 0.2}
        print(data)
        print('***', self.count)

        self.data.append(data['light'])
        # self.data.pop(0)

        figure = px.line(
            dict(Time=[i for i in range(len(self.data))], Light=self.data),
            x='Time',
            y='Light',
            range_y=[-10, 10]
        )

        self.app.push_mods({
            'light_graph': {'figure': figure},
            'progress':    {'value': str(self.count)}
        })

        self.count += 1;
        # if self.count > 10:
        #     self.count = 0
        # self.timer = Timer(.5, self.timer_callback)
        self.timer = Timer(0.01, self.timer_callback)
        self.timer.start()


if __name__ == '__main__':
    Example(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
