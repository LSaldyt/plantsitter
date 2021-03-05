from multiprocessing import Process
from motor import Motor
from time import sleep

def _turn(motor, t, direction):
    motor.turn(abs(t), direction)

class Turret:
    def __init__(self, vertical, horizontal):
        self.vertical   = vertical
        self.horizontal = horizontal

    def turn(self, a, b):
        processes = []
        try:
            motors = [(self.vertical, a, a > 0), (self.horizontal, b, b > 0)]
            for args in motors:
                processes.append(Process(target=_turn, args=args))
            for p in processes:
                p.start()
        finally:
            for process in processes:
                process.join()

def main():
    horizontal = Motor(4, 17)
    vertical   = Motor(18, 27)
    turret = Turret(vertical, horizontal)

    # while True:
    #     # horizontal.turn(1)
    #     # horizontal.turn(1, False)
    #     vertical.turn(.25)
    #     sleep(1)
    #     vertical.turn(.25, False)
    #     sleep(1)
    # turret.turn(-1, 10)
    # turret.turn(-5, -5)

if __name__ == '__main__':
    main()
