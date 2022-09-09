"""A ColorPath is a group of three toggle switches, an illuminated pushbutton
switch, and a NeoPixel strip. ColorPaths are fed hand wheel position chnages
and the LEDs respond depending on how their pushbutton and toggles are set.
"""
from time import sleep, monotonic
from random import randint, choice
import board
import busio
from digitalio import DigitalInOut, Direction, DriveMode, Pull
from adafruit_mcp230XX.mcp23017 import MCP23017
from adafruit_debouncer import Debouncer
import neopixel

mcp = MCP23017(board.I2C())

MAX_BRIGHT = 255 # maximum brightness
sys_stability = [0, 10] # Time in seconds before random decay of LED pattern

sound_pins = (board.D4, board.D5, board.D6, board.D9, board.D10, board.D11, board.D12)
sound_triggers = []
for pin in sound_pins:
    trigger_pin = DigitalInOut(pin)
    trigger_pin.direction = Direction.OUTPUT
    #trigger_pin.drive_mode = DriveMode.OPEN_DRAIN
    trigger_pin.value = True
    sound_triggers.append([trigger_pin, 0])

def reset_sound_player():
    sound_triggers[0][0].value = False
    sleep(0.2)
    sound_triggers[0][0].value = True
reset_sound_player()

def play_sound(num):
    sound_triggers[num][0].value = False
    sound_triggers[num][1] = monotonic()

def update_sound_pins():
    for t_pin in sound_triggers:
        if t_pin[0].value == False:
            if monotonic() - t_pin[1] > 0.2:
                t_pin[0].value = True
                t_pin[1] = 0


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
        update_sound_pins()
        self.sw_red.update()
        self.sw_green.update()
        self.sw_blue.update()
        self.ipb.update()
        #if self.sw_red.fell:
        #    play_sound(2)
        #if self.sw_red.rose:
        #    play_sound(3)
        #if self.sw_green.fell:
        #    play_sound(2)
        #if self.sw_green.rose:
        #    play_sound(3)
        #if self.sw_blue.fell:
        #    play_sound(2)
        #if self.sw_blue.rose:
        #    play_sound(3)
        if self.ipb.fell and self.active:
            self.active = False
            self.ipb_lamp.value = False
            play_sound(2)
        elif self.ipb.fell and not self.active:
            self.active = True
            self.ipb_lamp.value = True
            play_sound(3)
        if monotonic() - self.last_change > self.stability:
            bad_px = randint(0,self.num_pixels-1)
            vals = [0,1,2]
            
            strongest_val = choice(vals)
            vals.remove(strongest_val)
            middle_val = choice(vals)
            vals.remove(middle_val)
            weakest_val = choice(vals)
            
            bad_color = [0,0,0]

            bad_color[strongest_val] = randint(MAX_BRIGHT//2,MAX_BRIGHT)
            bad_color[middle_val] = max((bad_color[strongest_val] - randint(bad_color[strongest_val]//2,bad_color[strongest_val])), 0)
            bad_color[weakest_val] = max((bad_color[middle_val] - randint(bad_color[middle_val]//2,bad_color[middle_val])), 0)

            # bad_color = (randint(0,MAX_BRIGHT),randint(0,MAX_BRIGHT),randint(0,MAX_BRIGHT))
            # print(f"bad_px:{bad_px}, bad_color:{bad_color}")
            self.twin[bad_px] = tuple(bad_color)
            self.strip[bad_px] = tuple(bad_color)
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
            MAX_BRIGHT if self.sw_red.value else 0,
            MAX_BRIGHT if self.sw_green.value else 0,
            MAX_BRIGHT if self.sw_blue.value else 0,
            )
        if amount > 0:
            rng = range(0, self.num_pixels)
            snd = 2
        else:
            rng = range(self.num_pixels - 1, -1, -1)
            snd = 3
        for i in rng:
            if self.twin[i] == color:
                continue    
            else:
                self.twin[i] = color
                self.strip[i] = color
                change_occured = True
                play_sound(snd)
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
