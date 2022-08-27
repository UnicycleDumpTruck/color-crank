"""A ColorPath is a group of three toggle switches, an illuminated pushbutton
switch, and a NeoPixel strip. ColorPaths are fed hand wheel position chnages
and the LEDs respond depending on how their pushbutton and toggles are set.
"""

import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp23017 import MCP23017
from adafruit_debouncer import Debouncer

i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)

class ColorPath():
    """Group of three switches, one illum pushbutton, one LED strip."""
    def __init__(self, sw1_pin: int, sw2_pin: int, sw3_pin: int, ipb_pin: int, led_pin, num_pixels: int):
        sw1_pin = mcp.get_pin(sw1_pin)
        sw2_pin = mcp.get_pin(sw2_pin)
        sw3_pin = mcp.get_pin(sw3_pin)
        ipb_pin = mcp.get_pin(ipb_pin)
        sw1_pin.direction = Direction.INPUT
        sw2_pin.direction = Direction.INPUT
        sw3_pin.direction = Direction.INPUT
        ipb_pin.direction = Direction.INPUT
        sw1_pin.pull = Pull.UP
        sw2_pin.pull = Pull.UP
        sw3_pin.pull = Pull.UP
        ipb_pin.pull = Pull.UP
        self.sw_red = Debouncer(sw1_pin)
        self.sw_green = Debouncer(sw2_pin)
        self.sw_blue = Debouncer(sw3_pin)
        self.ipb = Debouncer(ipb_pin)

        self.ipb_lamp = mcp.get_pin(ipb_lamp_pin)
        self.ipb_lamp.direction = Direction.OUTPUT
        self.ipb_lamp.value = False

        self.active = False

        self.strip = neopixel.NeoPixel(
            led_pin, num_pixels, brightness=255, auto_write=True, pixel_order=neopixel.GRB
        )
        
        self.strip.fill((32,0,0))
        self.twin = [(index, (0,0,0) for index in range(num_pixels)]

    def update(self):
        self.sw_red.update()
        self.sw_green.update()
        self.sw_blue.update()
        self.ipb.update()

        if self.ipb.fell and self.active:
            self.active = False
            self.ipb_lamp.value = False
        elif self.ipb.fell and not self.active:
            self.active = True
            self.ipb_lamp.value = True

    def change(self, amount: int):
        if not self.active:
            return None
        color = (
            32 if self.sw_red.value else 0,
            32 if self.sw_green.value else 0,
            32 if self.sw_blue.value else 0,
            )
        if amount > 0:
            rng = range(0, self.num_pixels)
        else:
            rng = range(self.num_pixels, -1, -1)
        for i in range(self.num_pixels):
            if self.twin[i] == color:
                continue    
            else:
                self.twin[i] = color
                self.strip[i] = color
                break
        print(f"{self.twin}")