from gpiozero import LightSensor
from time import sleep

import sys

def initialize_sensors(specification):
    sensors = dict()
    for k, v in specification.items():
        print(f'Creating sensor "{k}" = GPIO({v})')
        sensor = LightSensor(v)
        print(f'Initial value: {sensor.value}')
        sensors[k] = sensor
    return sensors


if __name__ == '__main__':
    sys.exit(main())
