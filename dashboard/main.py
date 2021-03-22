import patch

import dash_devices
from plant_dash.dashboard import PlantDash

app = dash_devices.Dash(__name__)

if __name__ == '__main__':
    PlantDash(app)
    app.run_server(debug=True, host='0.0.0.0', port=5000)
