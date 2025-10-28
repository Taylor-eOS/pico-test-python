from machine import Pin
from neopixel import NeoPixel
import time
import gc

pins_to_test = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,20,21,22,23,26,27,28,29,30]

colors = [
    (32,0,0),
    #(32,32,0),
    #(32,0,32),
    #(0,32,32),
    (32,32,32)
]

def try_neopixel(pin):
    print("Testing NeoPixel on GPIO", pin)
    try:
        np = NeoPixel(Pin(pin, Pin.OUT), 1)
        for c in colors:
            np[0] = c
            np.write()
            print("  wrote color", c)
            time.sleep(1.0)
        np[0] = (0,0,0)
        np.write()
        print("  cleared")
        np = None
        gc.collect()
        Pin(pin, Pin.OUT).off()
        return True
    except Exception as e:
        print("  failed:", e)
        try:
            Pin(pin, Pin.OUT).off()
        except Exception:
            pass
        return False

def try_gpio_blink(pin):
    print("Testing GPIO blink on", pin)
    try:
        led = Pin(pin, Pin.OUT)
        for _ in range(2):
            led.on()
            print("  ON")
            time.sleep(0.6)
            led.off()
            print("  OFF")
            time.sleep(0.4)
        led.off()
        return True
    except Exception as e:
        print("  failed:", e)
        return False

for p in pins_to_test:
    print("----- GPIO", p, "-----")
    try_neopixel(p)
    time.sleep(0.2)
    try_gpio_blink(p)
    time.sleep(0.2)

print("Scan complete. Watch for any LED activity.")

