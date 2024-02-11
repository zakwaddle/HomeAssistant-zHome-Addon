import machine
import utime


class Button:
    
    def __init__(self, pin):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.last_trigger = utime.ticks_ms()
        self.debounce = 40
        
    def get_delta(self):
        new_time = utime.ticks_ms()
        delta = utime.ticks_diff(new_time, self.last_trigger)
        self.last_trigger = new_time
        return delta > self.debounce

    def pressed(self):
        return self.pin.value() and self.get_delta()


class MQTTStatelessSwitch:
    
    def __init__(self, pin, mqtt_client, button_topic):
        self.switch = Button(pin)
        self.client = mqtt_client
        self.button_topic = button_topic
        
    def publish_button_press(self):
        self.client.publish(self.button_topic, "1") 
        
    def publish_double_press(self):
        self.client.publish(self.button_topic, "2")
        
    def publish_long_press(self):
        self.client.publish(self.button_topic, "L")

    def update(self):
        def is_long_press():
            t1 = utime.ticks_ms()
            is_long = False
            while self.switch.pin.value():
                utime.sleep_ms(10)
                pressed_time = utime.ticks_diff(utime.ticks_ms(), t1)
                is_long = pressed_time > 600
                if is_long:
                    self.publish_long_press()
                    print("long", pressed_time)
                    utime.sleep(2)
                    break
            return is_long
        
        def is_double_press():
            is_double = False
            countdown = 250
            while countdown > 0:
                if self.switch.pressed():
                    is_double = True
                    self.publish_double_press()
                    break
                countdown -= 10
                utime.sleep_ms(10)
            return is_double
        
        if self.switch.pressed():
            if not is_long_press():
                if is_double_press():
                    print("double")
                else:
                    print("button")
                    self.publish_button_press()
            utime.sleep_ms(250)
