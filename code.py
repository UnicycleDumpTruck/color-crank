import time
from random import choice
from time import sleep
import board
from adafruit_seesaw import seesaw #, rotaryio
from adafruit_soundboard import Soundboard


#from adafruit_seesaw import digitalio as sdio
#import neopixel
#import digitalio as dio
#from adafruit_debouncer import Debouncer

from knob import Knob
from colorpath import ColorPath

# lever_pin = dio.DigitalInOut(board.D10)
#lever_pin.direction = dio.Direction.INPUT
#lever_pin.pull = dio.Pull.UP
#lever = Debouncer(lever_pin)

#sound_trigger_pin = dio.DigitalInOut(board.D9)
#sound_trigger_pin.direction = dio.Direction.OUTPUT
#sound_trigger_pin.drive_mode = dio.DriveMode.OPEN_DRAIN
#sound_trigger_pin.value = True


sound = Soundboard('TX', 'RX', 'D4', debug = True)
print(sound.files)
sound.play(b'T00     OGG')



PX_PER_STRIP = 25

cpath_a = ColorPath(0,1,2,3,15, board.A1, PX_PER_STRIP)
cpath_b = ColorPath(4,5,6,7,14, board.A2, PX_PER_STRIP)
cpath_c = ColorPath(8,9,10,11,13, board.A3, PX_PER_STRIP)

handwheel = Knob(seesaw.Seesaw(board.I2C(), addr=0x36))

print("Boot complete, starting loop...")

while True:
    cpath_a.update()
    cpath_b.update()
    cpath_c.update()

    wheel_change = handwheel.update()
    
    if wheel_change is not None:
        if any([
            cpath_a.change(wheel_change),
            cpath_b.change(wheel_change),
            cpath_c.change(wheel_change),
            ]):
                if wheel_change > 0:
                    sound.play_now(b'T03     OGG')
                else:
                    sound.play_now(b'T02     OGG')

