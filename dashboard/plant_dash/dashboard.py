import patch

import dash_devices
from dash_devices.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from threading import Timer

from websocket import create_connection
from datetime  import datetime
import logging as log

from utils.config import Config
from utils.mongo  import MongoDatabases

from .layout import create_elements

from .controller import Controller
from .monitor    import TELEM
from .sitter     import Sitter
from .tracker    import Tracker

from .settings_manager import SettingsManager

from plant_care.plant_scraper import PlantScraper

class PlantDash:
    def __init__(self, app):
        self.mongo      = MongoDatabases()
        self.config     = Config()
        self.app        = app
        self.connections = {k : None for k in self.config.connections}

        self.scraper = PlantScraper(self.mongo)

        self.controller = Controller(app, self.connections)
        self.sitter     = Sitter(app, self.connections, self.mongo)

        self.handlers = [self.controller, self.sitter]

        self.tracker    = Tracker(app, self.mongo)
        self.manager    = SettingsManager(app, self.mongo)

        self.app.layout = create_elements(app, TELEM)

        self.timer = None

        @self.app.callback_connect
        def func(client, connect):
            print(client, connect, len(app.clients))
            if connect and len(app.clients) == 1:
                self.loop()
            elif not connect and len(app.clients) == 0:
                self.timer.cancel()

    def ensure_connections(self):
        try:
            for name, conn in self.connections.items():
                if conn is None:
                    self.connections[name] = create_connection(f'ws://{self.config.plantsitter_ip}:{self.config.plantsitter_port}/{name}')
                    print(f'Connection to {name} successfully established!', flush=True)
                else:
                    pass
            return True
        except Exception as e:
            print(f'Unable to establish websocket connection ({e}), retrying..', flush=True)
            return False

    def iterate(self):
        for handler in self.handlers:
            handler.iterate(self.connections)

    def no_connection(self):
        for handler in self.handlers:
            handler.no_connection(self.connections)

    def loop(self):
        if self.ensure_connections():
            self.iterate()
            self.timer = Timer(self.config.sleep_normal, self.loop)
        else:
            self.no_connection()
            self.timer = Timer(self.config.sleep_no_connection, self.loop)
        self.timer.start()
