import patch

import dash_devices
from dash_devices.dependencies import Input, Output, State
from dash_html_components import P
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

from plant_care.plant_scraper import PlantScraper

class Tracker:
    def __init__(self, app, mongo):
        self.config = Config()
        self.app    = app
        self.mongo  = mongo
        self.scraper = PlantScraper(mongo)

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
                self.mongo.plants.list.insert_one(dict(name=plant_name, x=x, y=y))
                plant_vals.append(plant_name)
                plant_options.append({'label' : plant_name, 'value' : plant_name})
            else:
                for entry in self.mongo.plants.list.find():
                    name = entry['name']
                    plant_options.append({'label' : name, 'value' : name})
            x = []
            y = []
            text = []
            for entry in self.mongo.plants.list.find():
                text.append(entry['name'])
                x.append(entry['x'])
                y.append(entry['y'])
            fig = px.scatter(x=x, y=y, text=text)
            fig.update_layout(title_text='Plant Locations')
            return fig, plant_vals, plant_options

        @app.callback(
                [Output('description', 'children')],
                [Input('add_plant', 'n_clicks')],
                [State('add_plant', 'value'),
                 State('plant_name', 'value'),
                 State('x_coordinate', 'value'),
                 State('y_coordinate', 'value'),
                 State('plant_select', 'value'),
                 State('plant_select', 'options')])
        def add_plant(n_clicks, button_value, plant_name, x, y, plant_vals, plant_options):
            if n_clicks > 0:
                entry = self.scraper.get(plant_name)
                return [P(entry['summary'])]
            else:
                return [P('When new plants are added, wikipedia entries about them will appear here')]
