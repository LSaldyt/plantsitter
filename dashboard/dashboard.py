import requests, json
import dash

class Config():
    def __init__(self, filename='config.json'):
        with open(filename, 'r') as config_json:
            self.config = json.load(config_json)

    def __getattr__(self, name):
        try:
            return self.config[name]
        except KeyError:
            return object.__getattr__(self, name)

config = Config()
print(requests.get(f'http://{config.plantsitter_ip}:{config.plantsitter_port}/'))
