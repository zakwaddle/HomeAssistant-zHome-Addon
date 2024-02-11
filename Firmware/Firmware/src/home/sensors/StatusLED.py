import machine
import utime
import sys


class StatusLED:

    def __init__(self):
        status_pins = {
            "Raspberry Pi Pico W with RP2040": "LED",
            "ESP32 module with ESP32": 2,
            "LOLIN_S2_MINI with ESP32-S2FN4R2": 15
        }
        self.platform = sys.implementation._machine
        self.led_pin = machine.Pin(status_pins[self.platform], machine.Pin.OUT)
        self.off()

    def on(self):
        self.led_pin(1)

    def off(self):
        self.led_pin(0)

    def blink_light(self, speed_ms=250):
        self.on()
        utime.sleep_ms(speed_ms)
        self.off()
        utime.sleep_ms(speed_ms)
        self.on()
        utime.sleep_ms(speed_ms)
        self.off()
        utime.sleep_ms(speed_ms)
        self.on()
        utime.sleep_ms(speed_ms)
        self.off()
        utime.sleep_ms(speed_ms)
