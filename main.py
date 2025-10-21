from machine import Pin
from neopixel import NeoPixel
import time

led = NeoPixel(Pin(23), 1)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

pos = 0
while True:
    color = wheel(pos)
    led[0] = color
    led.write()
    print("Color:", color)
    pos = (pos + 1) % 256
    time.sleep(0.05)

