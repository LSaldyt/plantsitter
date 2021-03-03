from motor import Motor
from time import sleep

def main():
    main = Motor(22, 23)
    sleep(3)
    while True:
        main.turn(1)
        main.turn(3, False)

if __name__ == '__main__':
    main()
