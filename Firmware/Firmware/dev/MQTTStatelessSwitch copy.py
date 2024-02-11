import machine
import utime

class Button:
    def __init__(self, pin, callback=None, debounce_ms=40):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.callback = callback
        self.debounce_ms = debounce_ms
        self.last_trigger = utime.ticks_ms()
        
        if self.callback:
            self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.pressed)

    def pressed(self):
        new_time = utime.ticks_ms()
        if utime.ticks_diff(new_time, self.last_trigger) > self.debounce_ms:
            self.last_trigger = new_time
            self.callback()

class MQTTStatelessSwitch:
    SINGLE_PRESS = "1"
    DOUBLE_PRESS = "2"
    LONG_PRESS = "L"

    def __init__(self, pin, mqtt_client, button_topic):
        self.switch = Button(pin, callback=self.check_button)
        self.client = mqtt_client
        self.button_topic = button_topic

    def publish_button_press(self, press_type):
        self.client.publish(self.button_topic, press_type)

    def _is_long_press(self):
        t1 = utime.ticks_ms()
        while self.switch.pin.value():
            utime.sleep_ms(10)
            pressed_time = utime.ticks_diff(utime.ticks_ms(), t1)
            if pressed_time > 600:
                return True
        return False

    def _is_double_press(self):
        countdown = 250
        while countdown > 0:
            if self.switch.pin.value():
                return True
            countdown -= 10
            utime.sleep_ms(10)
        return False

#     def check_button(self):
#         if self._is_long_press():
#             self.publish_button_press(self.LONG_PRESS)
#             print('long press')
#             utime.sleep(2)
# 
#         elif self._is_double_press():
#             self.publish_button_press(self.DOUBLE_PRESS)
#             print('double press')
# 
#         else:
#             self.publish_button_press(self.SINGLE_PRESS)
#             print('single press')
# 
#         utime.sleep_ms(250)
#     def check_button(self):
#         if self.switch.pin.value():
#             utime.sleep_ms(10)  # Small debounce delay
#             if self.switch.pin.value():
#                 start_time = utime.ticks_ms()
#                 while self.switch.pin.value():  # Wait for the button to be released
#                     utime.sleep_ms(10)
#                 pressed_time = utime.ticks_diff(utime.ticks_ms(), start_time)
# 
#                 if pressed_time > 600:  # Long press
#                     self.publish_button_press(self.LONG_PRESS)
#                     print('long press')
#                     utime.sleep(2)
# 
#                 else:
#                     utime.sleep_ms(250)  # Wait for possible second press
#                     if self.switch.pin.value():
#                         while self.switch.pin.value():  # Wait for the button to be released again
#                             utime.sleep_ms(10)
#                         self.publish_button_press(self.DOUBLE_PRESS)
#                         print('double press')
# 
#                     else:
#                         self.publish_button_press(self.SINGLE_PRESS)
#                         print('single press')
    def check_button(self):
        if self.switch.pin.value():
            utime.sleep_ms(10)  # Small debounce delay
            if self.switch.pin.value():
                start_time = utime.ticks_ms()
                while self.switch.pin.value():  # Wait for the button to be released
                    utime.sleep_ms(10)
                pressed_time = utime.ticks_diff(utime.ticks_ms(), start_time)

                if pressed_time > 600:  # Long press
                    self.publish_button_press(self.LONG_PRESS)
                    print('long press')
                    utime.sleep(2)

                else:
                    utime.sleep_ms(250)  # Wait for possible second press
                    if self.switch.pin.value():
                        while self.switch.pin.value():  # Wait for the button to be released again
                            utime.sleep_ms(10)
                        self.publish_button_press(self.DOUBLE_PRESS)
                        print('double press')

                    elif not self.switch.pin.value():
                        self.publish_button_press(self.SINGLE_PRESS)
                        print('single press')

