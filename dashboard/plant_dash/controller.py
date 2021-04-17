import patch

import dash_devices
from dash_devices.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

import logging as log
import json

from utils.config import Config

from .connection import Connection

class Controller(Connection):
    def __init__(self, app, connections):
        self.connections = connections

        @app.callback(None, [Input('command', 'n_clicks')],
                            [State('input-on-submit', 'value'),
                             State('actuator', 'value')
                                ])
        def command(n_clicks, value, actuator):
            command = self.connections.get('command', None)
            if command is not None:
                log.info(f'Sent: {actuator} {value}')
                command.send(json.dumps({actuator : value}))
            else:
                log.info(f'Cannot send command: No connection!')

    def iterate(self, connections):
        pass

    def no_connection(self, connections):
        pass
