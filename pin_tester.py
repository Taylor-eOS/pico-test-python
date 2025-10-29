from machine import Pin
from neopixel import NeoPixel
import time
import gc

#pins_to_test = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
pins_to_test = [16,17,18,19,20,21,22,23,24,25,26,27,28,29]

colors = [
    (32,0,0),
    (32,32,32)
]

def flush_pins():
    print("Actively clearing data lines and forcing WS2812 reset")
    lengths_to_try = [1,4,8,30]
    for p in pins_to_test:
        try:
            Pin(p, Pin.OUT).off()
            time.sleep_ms(2)
        except Exception:
            pass
    time.sleep_ms(5)
    for p in pins_to_test:
        cleared = False
        for L in lengths_to_try:
            try:
                np = NeoPixel(Pin(p, Pin.OUT), L)
                for i in range(L):
                    np[i] = (0,0,0)
                np.write()
                gc.collect()
                time.sleep_ms(2)
                cleared = True
                break
            except Exception:
                try:
                    Pin(p, Pin.OUT).off()
                except Exception:
                    pass
        if not cleared:
            try:
                line = Pin(p, Pin.OUT)
                line.off()
                time.sleep_ms(5)
                for _ in range(6):
                    line.on()
                    time.sleep_us(400)
                    line.off()
                    time.sleep_us(400)
                time.sleep_ms(2)
            except Exception:
                pass
        try:
            Pin(p, Pin.IN)
        except Exception:
            try:
                Pin(p, Pin.OUT).off()
            except Exception:
                pass
    print("Flush complete; data lines pulled low then released.")

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

time.sleep(2)
flush_pins()
time.sleep(2)
for p in pins_to_test:
    print("----- GPIO", p, "-----")
    try_neopixel(p)
    time.sleep(0.2)
    try_gpio_blink(p)
    time.sleep(0.2)
print("Scan complete")

