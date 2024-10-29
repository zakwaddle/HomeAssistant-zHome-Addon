import machine
import json
from ..Timer import Timer


class Button:

    def __init__(self, pin, retrigger_delay_ms, timer_n=1):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.retrigger_delay_ms = retrigger_delay_ms

        self.on_button_press = None
        self.on_press_not_detected = None

        self.timer_n = timer_n
        self.timer = None
        self.last_press = 0

    def enable_interrupt(self):
        """Enable interrupt for motion pin."""
        print("enabling interrupt")
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.button_change)

    def set_on_button_press(self, func):
        self.on_button_press = func

    def set_on_press_not_detected(self, func):
        self.on_press_not_detected = func

    def set_timer_n(self, timer_n):
        self.timer_n = timer_n

    def button_change(self, _):
        self._press_detected()
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        self.timer = Timer(timer_number=self.timer_n * -1,
                           mode=Timer.ONE_SHOT,
                           period=self.retrigger_delay_ms,
                           callback=self._no_press_detected)

    def _press_detected(self):
        print("press detected")
        if not self.last_press:
            self.last_press = 1
            if self.on_button_press is not None:
                self.on_button_press()

    def _no_press_detected(self):
        print("no press detected")
        print()
        self.last_press = 0
        if self.on_press_not_detected is not None:
            self.on_press_not_detected()


class MQTTButton:
    def __init__(self, button: Button, mqtt_client, name=None, command_topic=None, discovery_topic=None, availability_topic=None):
        self.button = button
        self.mqtt_client = mqtt_client
        self.sensor_index = self.button.timer_n

        self.name = name
        self.command_topic = command_topic
        self.discovery_topic = discovery_topic
        self.availability_topic = availability_topic
        self.button.set_on_button_press(self.publish_button_press)
        # self.button.set_on_press_not_detected(self.publish_no_press)

    def enable_interrupt(self):
        self.button.enable_interrupt()

    def publish_button_press(self):
        """Publish button press detected to the MQTT topic."""
        print("publishing button press to ", self.command_topic)
        self.mqtt_client.publish(self.command_topic, "PRESS")

    def publish_no_press(self):
        """Publish button press detected to the MQTT topic."""
        print("publishing button press to ", self.command_topic)
        self.mqtt_client.publish(self.command_topic, "NO PRESS")

    def publish_online(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.publish(self.availability_topic, "online")

    def publish_offline(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.publish(self.availability_topic, "offline")

    def set_last_will(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.mqtt_set_last_will(self.availability_topic, "offline")

    def publish_discovery(self, device_info):
        print("Publishing Discovery")
        print("Button Discovery Topic: ", self.discovery_topic)
        print("Button Command Topic: ", self.command_topic)
        config = {
            "name": self.name,
            "device": device_info,
            "unique_id": f"{device_info.get('name')}-{self.name}",
            "command_topic": self.command_topic,
            "availability": [{"topic": self.availability_topic}]
        }
        self.mqtt_client.publish(self.discovery_topic, json.dumps(config), retain=True)


class HomeButton(MQTTButton):
    def __init__(self, home_client, name, sensor_config, topics, sensor_index):
        self.pin = sensor_config.get('pin')
        retrigger_delay_ms = sensor_config.get('retrigger_delay_ms')
        super().__init__(mqtt_client=home_client,
                         name=name,
                         command_topic=topics.get('command_topic'),
                         discovery_topic=topics.get('discovery_topic'),
                         availability_topic=topics.get('availability_topic'),
                         button=Button(pin=self.pin,
                         retrigger_delay_ms=retrigger_delay_ms,
                         timer_n=sensor_index))

    def __repr__(self):
        return f"<HomeButton| {self.name} | pin:{self.pin}>"

    def force_update(self):
        self.publish_online()
