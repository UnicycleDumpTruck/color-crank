"""A ColorPath is a group of three toggle switches, an illuminated pushbutton
switch, and a NeoPixel strip. ColorPaths are fed hand wheel position chnages
and the LEDs respond depending on how their pushbutton and toggles are set.
"""
from time import sleep, monotonic
from random import randint
import board
import busio
from digitalio import Direction, Pull
from adafruit_mcp230XX.mcp23017 import MCP23017
from adafruit_debouncer import Debouncer
import neopixel
# from adafruit_soundboard import Soundboard

#sleep(2)
#sound = Soundboard('TX', 'RX', 'D4', debug=True)

#sound.play(b'T00     OGG')
#print(f"Soundboard files: {sound.files}")

#i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(board.I2C())

MAX_BRIGHT = 8 # maximum brightness
sys_stability = [0, 10] # Time in seconds before random decay of LED pattern

class ColorPath():
    """Group of three switches, one illum pushbutton, one LED strip."""
    def __init__(self, sw1_pin: int, sw2_pin: int, sw3_pin: int, ipb_pin: int, ipb_lamp_pin: int, led_pin, num_pixels: int):
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
        self.ipb_lamp.value = True

        self.active = True
        
        self.num_pixels = num_pixels
        self.strip = neopixel.NeoPixel(
            led_pin, num_pixels, brightness=255, auto_write=True, pixel_order=neopixel.GRB
        )
        
        self.twin = [(0,0,0) for index in range(num_pixels)]
        self.last_change = monotonic()
        self.stability = randint(*sys_stability)
        print(self)
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
        if monotonic() - self.last_change > self.stability:
            bad_px = randint(0,self.num_pixels-1)
            
            bad_color = (randint(0,MAX_BRIGHT),randint(0,MAX_BRIGHT),randint(0,MAX_BRIGHT))
            # print(f"bad_px:{bad_px}, bad_color:{bad_color}")
            self.twin[bad_px] = bad_color
            self.strip[bad_px] = bad_color
            self.last_change = monotonic()
            self.stability = randint(*sys_stability)
    def inc_stability(self):
        # print('Incrementing stability')
        sys_stability[1] += 1
    def dec_stability(self):
        # print('Decrementing stability')
        sys_stability[1] -= 1
        sys_stability[1] = max(0,sys_stability[1])
    def change(self, amount: int):
        if not self.active:
            return False
        if self.ipb.value == False:
            if amount > 0:
                self.inc_stability()
            else:
                self.dec_stability()
        change_occured = False
        color = (
            8 if self.sw_red.value else 0,
            8 if self.sw_green.value else 0,
            8 if self.sw_blue.value else 0,
            )
        if amount > 0:
            rng = range(0, self.num_pixels)
        else:
            rng = range(self.num_pixels - 1, -1, -1)
        for i in rng:
            if self.twin[i] == color:
                continue    
            else:
                self.twin[i] = color
                self.strip[i] = color
                change_occured = True
                break
        self.last_change = monotonic()
        print(f'returning {change_occured}')
        return change_occured

    def __repr__(self):
        output = ''
        for pixel in self.twin:
            output += 'x' if pixel[0] else '_'
            output += 'x' if pixel[1] else '_'
            output += 'x' if pixel[2] else '_'
            output += '|'
        return output
