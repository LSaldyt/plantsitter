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

def image(app, filename):
    return Img(src=app.get_asset_url(filename),
                 id=filename.split('.')[0],
                 style={
                     "height": "100px",
                     "width": "auto",
                     "margin-bottom": "25px"},)

# TODO: Add plantnet logo

def create_elements(app, TELEM):
    elements = [Div([
        Div([image(app, 'asu_logo_alt.png')], className="one-third column",),
        Div([Div([H3('PlantSitter',
                     style={"margin-bottom": "0px"},),
                  H5('Raspberry-Pi Based Live Agriculture Monitoring', style={"margin-top": "0px"}),
                  H6('By Lucas Saldyt', style={"margin-top": "0px"}),])],
            className="one-half column",
            id="title",),
        Div([image(app, 'pfaf_logo_bg.png')], className="one-third column",),
        ],
    id="header",
    className="row flex-display",
    style={"margin-bottom": "25px"},),
Div([Div([Div([H4('Plant Tracking'),
              dcc.Dropdown(id='plant_select',
                  options=[],
                  multi=True,
                  value=[],
                  className="dcc_control"),
              Div([H6('Name'), dcc.Input(id='plant_name', type='text', value='')]),
              Div([H6('X'), dcc.Input(id='x_coordinate', type='number', value=0.0, style={'width' : '20%'})]),
              Div([H6('Y'), dcc.Input(id='y_coordinate', type='number', value=0.0, style={'width' : '20%'})]),
               html.Button('Add', id='add_plant', n_clicks=0)
              ],
              className="pretty_container",
              id='settings',),
          Br(),
          Div([H4('Description'),
               Div([P('Fill in')], id='description')],
               className="pretty_container",
               id='description_container',),
          Br(),
          Div([H4('Control'),
               dcc.Dropdown(id='actuator',
                   options=[dict(label='Pump', value='main'),
                            dict(label='L/R',  value='horizontal'),
                            dict(label='U/D',  value='vertical'),],
                   value='main',
                   className="dcc_control",
               ),
               dcc.Input(id='input-on-submit', type='number', value=1.0),
               html.Button('Submit', id='command', n_clicks=0)],
               className="pretty_container",
               id='control',),
         ],
        id='settings_and_controls',
        className='four columns'),
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
            className="eight columns",),
    ],
    className="row flex-display",),
    Br()]

    for k in TELEM:
        elements.extend([
            Br(),
            Div(H3(f'{k.title()} Measurement'), className='twelve columns'),
            Div(dcc.Graph(id=f'{k}_graph'),
                className='pretty_container twelve columns',
                id=f'{k}_graph_container'),
            Br()])
    return Div(elements)
