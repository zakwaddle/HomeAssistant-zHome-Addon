import machine
import settings
from Messenger import Messenger
from MotionSensor import MotionSensor
from StatusLED import StatusLED
from TimeManager import TimeManager
from Timer import Timer
from WiFiManager import WiFiManager

# Constants
PIN = 16

# Setup WiFi
wifi = WiFiManager(settings.wifi_ssid, settings.wifi_password)
wifi.connect_wifi()


def check_connections():
    if not wifi.is_connected():
        wifi.connect_wifi()


timer = Timer(timer_number=0, period=5000, mode=machine.Timer.PERIODIC, callback=check_connections)

# Setup time of day manager
tm = TimeManager()
tm.sync_time()
timer2 = Timer(timer_number=4, mode=machine.Timer.PERIODIC, period=30 * 60 * 1000, callback=tm.sync_time)

# Setup Socket Messenger
messenger = Messenger(settings.coffee_light_hostname, settings.coffee_light_port)

# Setup LED
led = StatusLED()
led.blink_light()


# Setup Motion Sensor
def motion_detected():
    is_day_time = tm.is_day_time(settings.day_time_start, settings.day_time_end)
    if is_day_time:
        print('day time light')
        led.on()
        messenger.queue_message(b"Motion Detected")
    else:
        print('night time light')
        led.on()
        messenger.queue_message(b"Motion Detected")


def no_motion_detected():
    led.off()
    messenger.queue_message(b"No Motion")


motion_sensor = MotionSensor(PIN, 10000)
motion_sensor.set_on_motion_detected(motion_detected)
motion_sensor.set_on_motion_not_detected(no_motion_detected)
motion_sensor.enable_interrupt()

# Main Loop
while True:
    messenger.send_queued_message()
    machine.idle()
