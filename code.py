import time
from random import choice
from time import sleep
import board
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as sdio
import neopixel
import digitalio as dio
from adafruit_debouncer import Debouncer


lever_pin = dio.DigitalInOut(board.D10)
lever_pin.direction = dio.Direction.INPUT
lever_pin.pull = dio.Pull.UP
lever = Debouncer(lever_pin)

sound_trigger_pin = dio.DigitalInOut(board.D9)
sound_trigger_pin.direction = dio.Direction.OUTPUT
sound_trigger_pin.drive_mode = dio.DriveMode.OPEN_DRAIN
sound_trigger_pin.value = True


# The number of NeoPixels per strip
PX_PER_STRIP = 64

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

strip_a = neopixel.NeoPixel(
    board.A0, PX_PER_STRIP, brightness=255, auto_write=True, pixel_order=ORDER
)
strip_b = neopixel.NeoPixel(
    board.A1, PX_PER_STRIP, brightness=255, auto_write=True, pixel_order=ORDER
)
strip_c = neopixel.NeoPixel(
    board.A2, PX_PER_STRIP, brightness=255, auto_write=True, pixel_order=ORDER
)

strips = (strip_a, strip_b, strip_c)

for strip in strips:
    strip.fill((64,0,0))

RESOLUTION = 1  # Only change on every nth position.

class Knob():
    def __init__(self, seesaw):
        self.seesaw = seesaw
#        self.matrix = matrix
#        self.color = color
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print(f"Found product {seesaw_product}")
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.button = sdio.DigitalIO(seesaw, 24)
        self.button_held = False
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = 0
        self.last_change = 0

    def update(self):
        position = -self.encoder.position
        if position > self.last_position:
            print(f"Position increased to: {position}, diff {position - self.last_position}")
            if ((position - self.last_change) > RESOLUTION):
                # print("ADD "*15)
#                self.matrix.add_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        elif position < self.last_position:
            print(f"Position decreased to: {position}, diff {self.last_position - position}")
            if ((self.last_change - position) > RESOLUTION):
                # print("REMOVE "*15)
#                self.matrix.remove_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Button pressed")
        if self.button.value and self.button_held:
            self.button_held = False
            print("Button released")


knobs = [Knob(seesaw.Seesaw(board.I2C(), addr=0x36))]

print("Boot complete, starting loop...")

while True:
    lever.update()
    if lever.rose or lever.fell:
        print("Lever changed!")
        transfer()

    for knob in knobs:
        knob.update()
