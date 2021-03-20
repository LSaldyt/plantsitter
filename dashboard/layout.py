import patch
import dash_devices
from dash_devices.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

def create_elements(app, TELEM):
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
                                dcc.Dropdown(
                                    id='actuator',
                                    options=[dict(label='Pump', value='main'),
                                             dict(label='L/R',  value='horizontal'),
                                             dict(label='U/D',  value='vertical'),
                                             ],
                                    value='main',
                                    className="dcc_control",
                                ),
                                html.Div(dcc.Input(id='input-on-submit', type='number', value=1.0)),
                                html.Button('Submit', id='command', n_clicks=0)
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
                                        html.Div(
                                            ['Humidity', html.H6(id='humidity_text')],
                                            id='humidity',
                                            className="mini_container",
                                        ),
                                        html.Div(
                                            ['Light', html.H6(id='light_text')],
                                            id='light',
                                            className="mini_container",
                                        ),
                                    ],
                                    id="info-container",
                                    className="row container-display",
                                ),
                                html.Div(
                                    [dcc.Graph(id='plant_map')],
                                    id='plant_map_container',
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
                ]

    for k in TELEM:
        elements.append(html.Div(f'{k.title()} Measurement'))
        elements.append(dcc.Graph(id=f'{k}_graph'))
    return html.Div(elements)
