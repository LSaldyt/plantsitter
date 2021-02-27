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

def main():
    specification = dict(light=4, humidity=17, rain=18, moisture=27)
    sensors = initialize_sensors(specification)
    second = 0
    try:
        while True:
            print(f'Loop: {second}', flush=True)
            for k, v in sensors.items():
                print(f'Sensor {k} : {v.value}')
            sleep(1)
            second += 1
    finally:
        for sensor in sensors.values():
            sensor.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
