from motor import Motor
from time import sleep

def main():
    main = Motor(22, 23)
    horizontal = Motor(18, 27)
    vertical   = Motor(4, 17)

    main.turn(4.0)
    # horizontal.turn(7.0, False)
    # main.turn(4.0)
    # vertical.turn(0.5)
    # main.turn(4.0)
    # horizontal.turn(5.0, False)
    # main.turn(4.0)
    # vertical.turn(0.5, False)
    # horizontal.turn(13.0)

    # horizontal.turn(3.0)
    # 1/0

    # main.turn(3.0)
    # vertical.turn(0.6, False)
    # main.turn(3.0)
    # vertical.turn(i * 0.025, False)
    # vertical.turn(0.6)
    # main.turn(3.75)
    # sleep(3)

    # main.turn(0.2)
    # sleep(0.3)
    # main.turn(0.4)

    # vertical.turn(1.0)
    # vertical.turn(0.5, False)
    # main.turn(1.0)

    # for i in range(30):
    #     print(i, flush=True)
    #     main.turn(0.05 * i)
    #     sleep(2)

    #vertical.turn(1.5)
    # vertical.turn(0.75, False)
    # for i in range(20):
    #     # vertical.turn(i * 0.05, False)
    #     vertical.turn(i * 0.025)
    #     main.turn(0.45)

    #     # main.turn(0.4 + 0.025 * i)
    #     sleep(3)

    # vertical.turn(0.1)
    #vertical.turn(0.25, False)
    # for i in range(30):
    # for i in [16, 17, 18, 19, 20, 21]:
    #     print(i, i * 0.025, flush=True)
    #     main.turn(i * 0.025)
    #     sleep(3)

    # while True:
    #     main.turn(0.35)
    #     horizontal.turn(14, False)
    #     main.turn(0.35)
    #     horizontal.turn(14)
    #     sleep(0.5)



    #     # sleep(1)
    #     # print(i, flush=True)
    #     # sleep(1)

    #     # horizontal.turn(1, False)
    #     # print(i, flush=True)
    #     # sleep(1)
    #     # horizontal.turn(14)
    #     # break
    #     # sleep(1)
    #     # vertical.turn(.25)
    #     # sleep(1)
    #     # vertical.turn(.25, False)
    #     # sleep(1)
    #     # main.turn(0.1)
    #     # sleep(1)
    #     # main.turn(0.1, False)
    #     # sleep(5)

if __name__ == '__main__':
    main()
