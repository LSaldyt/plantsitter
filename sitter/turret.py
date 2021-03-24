from multiprocessing import Process
from motor import Motor
from time import sleep
from math import atan2, sin, cos, degrees, hypot, acos

# Motor Calibration = 1/(angle/seconds)
vertical_calibration   = 1/(80/15)
horizontal_calibration = 1/(90/5)

# Pump Calibration = emperical: water @ angle without splashing
# main.turn(0.9)  # 85 degrees
# main.turn(0.88) # 75 degrees
# main.turn(0.86) # 65 degrees
# main.turn(0.86) # 55 degrees
# main.turn(0.84) # 45 degrees
# main.turn(0.84) # 40 degrees
# main.turn(0.84) # 30 degrees
# main.turn(0.82) # 20 degrees
# main.turn(0.78) # 10 degrees
# main.turn(0.76) # 5 degrees
# main.turn(0.76) # 0 degrees

pump_calibration = {
        85 : 0.9,
        75 : 0.88,
        65 : 0.86,
        55 : 0.86,
        45 : 0.84,
        40 : 0.84,
        30 : 0.84,
        20 : 0.82,
        10 : 0.78,
        5  : 0.76,
        0  : 0.76,
    }

arm_length = 16.5 / 0.0393701 # Inches to mm

# Inverse Kinematics Work
# r = arm_length * cos(theta_v) 
# x, y = cos(theta_h) * r, sin(theta_h) * r

class Turret:
    def __init__(self):
        self.vertical   = Motor(18, 27)
        self.horizontal = Motor(4, 17)
        self.pump       = Motor(22, 23)

        self.theta_v, self.theta_h = 0.0, 0.0 # Track vertical/horizontal angles

    def inv_theta_h(self, x, y):
        radians = atan2(x, y)
        theta_h = degrees(radians)
        return theta_h

    def inv_theta_v(self, x, y):
        dist    = hypot(x, y)
        theta_v = acos(dist/arm_length) # dist / arm_length = cos(theta_v)
        theta_v = degrees(theta_v)
        return theta_v

    def up(self, angle):
        self.vertical.turn(abs(angle * vertical_calibration), angle < 0)
        self.theta_v += angle

    def turn(self, angle):
        self.horizontal.turn(abs(angle * horizontal_calibration), angle < 0)
        self.theta_h += angle

    def inverse(self, x, y):
        theta_h = self.inv_theta_h(x, y)
        theta_v = self.inv_theta_v(x, y)
        print(theta_h, theta_v)
        theta_h = theta_h - self.theta_h
        theta_v = theta_v - self.theta_v
        print(theta_h, theta_v)
        self.turn(theta_h)
        self.up(theta_v)

def main():
    turret = Turret()
    # turret.inverse(1, -1)
    # turret.inverse(arm_length, 0)
    print(arm_length)
    turret.inverse(0, arm_length)
    # turret.inverse(-arm_length, 0)

if __name__ == '__main__':
    main()
