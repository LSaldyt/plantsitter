from gpiozero import OutputDevice
from time import sleep

class Relay(OutputDevice):
    def __init__(self, pin, active_high=True):
        super(Relay, self).__init__(pin, active_high)

class Motor:
    def __init__(self, forward_pin, backward_pin):
        self.forward_relay  = Relay(forward_pin)
        self.backward_relay = Relay(backward_pin)

    def turn(self, t, forward=True):
        if forward:
            relay = self.forward_relay
        else:
            relay = self.backward_relay
        relay.on()
        sleep(t)
        relay.off()
