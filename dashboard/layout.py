import patch
import dash_devices
from dash_devices.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components import * # Well justified

to_id = lambda x : x.lower().replace(' ', '_')

def mini(name):
    idn = to_id(name)
    return Div([name.title(), H6(id=f'{idn}_text')], id=f'{idn}', className="mini_container")

def create_elements(app, TELEM):
    elements = [Div([
        Div([Img(src=app.get_asset_url('asu_logo_alt.png'),
                 id="plotly-image",
                 style={
                     "height": "100px",
                     "width": "auto",
                     "margin-bottom": "25px",
                 },)], className="one-third column",),
        Div([Div([H3('PlantSitter',
                     style={"margin-bottom": "0px"},),
                  H5('Raspberry-Pi Based Live Agriculture Monitoring', style={"margin-top": "0px"}),
                  H6('By Lucas Saldyt', style={"margin-top": "0px"}),])],
            className="one-half column",
            id="title",),
        Div([H4('Hmm')],
            className="one-third column",
            id="button",), ],
    id="header",
    className="row flex-display",
    style={"margin-bottom": "25px"},),
Div([Div([H4('Settings'),
          dcc.Dropdown(id='plant_select',
              options=[dict(label='Agave',    value='Agave'),
                       dict(label='Rosemary', value='Rosemary')],
              multi=True,
              value=['Agave', 'Rosemary'],
              className="dcc_control",
          ),
          dcc.Dropdown(id='actuator',
              options=[dict(label='Pump', value='main'),
                       dict(label='L/R',  value='horizontal'),
                       dict(label='U/D',  value='vertical'),],
              value='main',
              className="dcc_control",
          ),
          Div(dcc.Input(id='input-on-submit', type='number', value=1.0)),
          html.Button('Submit', id='command', n_clicks=0)],
          className="pretty_container four columns",
          id="cross-filter-options",
        ),
    Div([Div([mini('Latency'),
              mini('Receive Rate'),
              mini('Plot Rate'),
              mini('Humidity'),
              mini('Light')],
              id="info-container",
              className="row container-display",),
         Div([dcc.Graph(id='plant_map')],
             id='plant_map_container',
             className="pretty_container",),],
            id="right-column",
            className="eight columns",), ],
    className="row flex-display",),
    Br()]

    for k in TELEM:
        elements.append(Div(f'{k.title()} Measurement'))
        elements.append(dcc.Graph(id=f'{k}_graph'))
    return Div(elements)
