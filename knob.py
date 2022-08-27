from adafruit_seesaw import seesaw, rotaryio
#from adafruit_seesaw import digitalio as sdio

RESOLUTION = 5  # Only change on every nth position.

class Knob():
    def __init__(self, seesaw):
        self.seesaw = seesaw
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print(f"Found product {seesaw_product}")
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = 0
        self.last_change = 0

    def update(self):
        position = -self.encoder.position

        if position > self.last_position:
            # print(f"Position increased to: {position}, diff {position - self.last_position}")
            if ((position - self.last_change) > RESOLUTION):
                self.last_change = position
                change = position - self.last_position
            else:
                change = None
            self.last_position = position
            print(f"Wheel change: {change}")
            return change

            
        elif position < self.last_position:
            # print(f"Position decreased to: {position}, diff {self.last_position - position}")
            if ((self.last_change - position) > RESOLUTION):
                self.last_change = position
                change = position - self.last_position
            else:
                change = None
            self.last_position = position
            print(f"Wheel change: {change}")
            return change
