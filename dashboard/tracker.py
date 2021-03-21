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

class Tracker:
    def __init__(self, app):
        self.config = Config()
        self.app    = app

        self.plants = []

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
            if n_clicks > 0:
                print(f'Adding plant!!: {plant_name} ({x}, {y})')
                self.plants.append((plant_name, x, y))
                plant_vals.append(plant_name)
                plant_options.append({'label' : plant_name, 'value' : plant_name})
                fig = px.scatter(x=[p[1] for p in self.plants], y=[p[2] for p in self.plants], text=[p[0] for p in self.plants])
                fig.update_layout(title_text='Plant Locations')
                return fig, plant_vals, plant_options
            else:
                return {'data' : []}, plant_vals, plant_options

