import time
from random import choice
from time import sleep
import board
from adafruit_seesaw import seesaw, rotaryio
from adafruit_seesaw import digitalio as sdio
import neopixel
import digitalio as dio
from adafruit_debouncer import Debouncer

from knob import Knob
from colorpath import ColorPath

lever_pin = dio.DigitalInOut(board.D10)
lever_pin.direction = dio.Direction.INPUT
lever_pin.pull = dio.Pull.UP
lever = Debouncer(lever_pin)

sound_trigger_pin = dio.DigitalInOut(board.D9)
sound_trigger_pin.direction = dio.Direction.OUTPUT
sound_trigger_pin.drive_mode = dio.DriveMode.OPEN_DRAIN
sound_trigger_pin.value = True

PX_PER_STRIP = 24

handwheel = Knob(seesaw.Seesaw(board.I2C(), addr=0x36))
cpath_a = ColorPath(0,1,2,3,4, board.25, PX_PER_STRIP)

print("Boot complete, starting loop...")

while True:
#    lever.update()
#    if lever.rose or lever.fell:
#        print("Lever changed!")

    cpath_a.update()
    
    wheel_change = handwheel.update()

    cpath_a.change(wheel_change)
