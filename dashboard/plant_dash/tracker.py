import patch

import dash_devices
from dash_devices.dependencies import Input, Output, State
from dash_html_components import P
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
from threading import Timer

from websocket import create_connection
from datetime  import datetime
from time      import time
from pprint    import pprint
import logging as log
import json

from utils.config import Config

from plant_care.plant_scraper import PlantScraper

class Tracker:
    def __init__(self, app, mongo):
        self.config = Config()
        self.app    = app
        self.mongo  = mongo
        self.scraper = PlantScraper(mongo)

        @app.callback(None,
                [Input('remove_plant', 'n_clicks')],
                [State('remove_plant', 'value'),
                 State('plant_name', 'value'),
                 State('x_coordinate', 'value'),
                 State('y_coordinate', 'value'),
                 State('sensor_id', 'value')])
        def remove_plant(n_clicks, button_value, plant_name, x, y, sensor):
            if n_clicks > 0:
                print(f'Removing plant!!: {plant_name} ({x}, {y})')
                self.mongo.plants.list.remove(
                    dict(name=plant_name, x=x, y=y),
                    dict(justOne=True))

        @app.callback(Output('plant_map', 'figure'),
                [Input('add_plant', 'n_clicks')],
                [State('add_plant', 'value'),
                 State('plant_name', 'value'),
                 State('x_coordinate', 'value'),
                 State('y_coordinate', 'value'),
                 State('sensor_id', 'value')])
        def add_plant(n_clicks, button_value, plant_name, x, y, sensor):
            if n_clicks > 0:
                print(f'Adding plant!!: {plant_name} ({x}, {y})')
                n = self.mongo.plants.list.count()
                self.mongo.plants.list.insert_one(dict(name=plant_name, x=x, y=y, sensor=sensor, n=n))
            else:
                pass
            x = []
            y = []
            text = []
            for entry in self.mongo.plants.list.find():
                text.append(entry['name'])
                x.append(entry['x'])
                y.append(entry['y'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, text=text, mode='markers+text', marker=dict(size=30, color='rgba(111, 168, 50, 0.5)')))
            fig.update_layout(title_text='Plant Locations')
            return fig

        @app.callback(Output('description', 'children'),
                      [Input('add_plant', 'n_clicks')],
                      [State('add_plant', 'value'),
                       State('plant_name', 'value'),
                       State('x_coordinate', 'value'),
                       State('y_coordinate', 'value')])
        def update_description(n_clicks, button_value, plant_name, x, y):
            if n_clicks > 0:
                entry = self.scraper.get(plant_name)
                return P(entry['summary'])
            else:
                return P('When new plants are added, wikipedia entries about them will appear here')
