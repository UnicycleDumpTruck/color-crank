import time
from random import choice
from time import sleep
import board
from adafruit_seesaw import seesaw #, rotaryio

from digitalio import DigitalInOut, Direction, DriveMode


from knob import Knob
from colorpath import ColorPath

#sound_pins = (board.D4, board.D5, board.D6, board.D9, board.D10, board.D11, board.D12)
#sound_triggers = []
#for pin in sound_pins:
#    trigger_pin = DigitalInOut(pin)
#    trigger_pin.direction = Direction.OUTPUT
#    #trigger_pin.drive_mode = DriveMode.OPEN_DRAIN
#    trigger_pin.value = True
#    sound_triggers.append(trigger_pin)

#sound_triggers[0].value = True

#def reset_sound_player():
#    sound_triggers[0].value = False
#    time.sleep(0.2)
#    sound_triggers[0].value = True

#reset_sound_player()
#for snd in sound_triggers:
#    snd.value = False
#    time.sleep(0.2)
#    snd.value = True
#def play_sound(num):
#    sound_triggers[num].value = False
#    time.sleep(0.2)
#    sound_triggers[num].value = True

#time.sleep(5)
#sound = Soundboard('TX', 'RX', 'D4', debug=True)
#time.sleep(1)
#sound.reset()
# print(sound.files)
#sound.play(b'T00     OGG')



PX_PER_STRIP = 25

cpath_a = ColorPath(0,1,2,3,15, board.A1, PX_PER_STRIP)
cpath_b = ColorPath(4,5,6,7,14, board.A2, PX_PER_STRIP)
cpath_c = ColorPath(8,9,10,11,13, board.A3, PX_PER_STRIP)

handwheel = Knob(seesaw.Seesaw(board.I2C(), addr=0x36))

print("Boot complete, starting loop...")

while True:
    wheel_change = handwheel.update()
    cpath_a.update()
    cpath_b.update()
    cpath_c.update()
    if wheel_change is not None:
        cpath_a.change(wheel_change)
        cpath_b.change(wheel_change)
        cpath_c.change(wheel_change)

