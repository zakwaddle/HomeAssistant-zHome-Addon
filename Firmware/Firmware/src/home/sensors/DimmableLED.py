import machine
import sys
import json


class DimmableLight:
    def __init__(self, pin: int, freq: int = 300, timer_n=1, fade_time_ms=4, brightness_scale=100):
        self._platform = sys.platform
        if self._platform not in ['rp2', 'esp32']:
            raise ValueError(f"Unsupported platform: {self._platform}")

        self.pin = pin
        self.pwm = machine.Pin(self.pin)
        self.freq = freq
        self.timer_n = timer_n
        self.fade_time_ms = fade_time_ms
        self.brightness_scale = brightness_scale

        if self._platform == "rp2":
            self.light = machine.PWM(self.pwm)
            self.light.freq(freq)
        elif self._platform == "esp32":
            self.light = machine.PWM(self.pwm, freq=self.freq)

        self.current_brightness = 0
        self.target_brightness = 0
        self.prev_brightness = 255
        self.state = "OFF"
        self.set_brightness(0)

    def on(self):
        self.state = "ON"
        if self.target_brightness == 0:
            self.target_brightness = self.prev_brightness

    def off(self):
        self.state = "OFF"
        if not self.current_brightness == 0:
            self.prev_brightness = self.current_brightness
        self.target_brightness = 0

    def platform_timer(self, **kwargs):
        if sys.platform == 'rp2':
            t = machine.Timer(**kwargs)
        else:
            t = machine.Timer(self.timer_n * -1)
            t.init(**kwargs)
        return t

    def fade(self):
        keep_fading = False
        if self.current_brightness < self.target_brightness:
            self.current_brightness += 1
            keep_fading = True
        elif self.current_brightness > self.target_brightness:
            self.current_brightness -= 1
            keep_fading = True
        elif self.current_brightness == self.target_brightness:
            print("done fading - brightness: ", self.current_brightness)

        self.set_brightness(self.current_brightness)
        if keep_fading:
            self.platform_timer(period=self.fade_time_ms,
                                mode=machine.Timer.ONE_SHOT,
                                callback=lambda t: self.fade())

    def convert_to_duty(self, value: int) -> int:
        if self._platform == "rp2":
            return round((65535 / self.brightness_scale) * value)
        elif self._platform == "esp32":
            return round((1023 / self.brightness_scale) * value)
        else:
            return value

    def set_duty(self, value: int):
        if self._platform == "rp2":
            self.light.duty_u16(value)
        elif self._platform == "esp32":
            self.light.duty(value)

    def set_brightness(self, brightness: int):
        if not 0 <= brightness <= self.brightness_scale:
            raise ValueError("Brightness must be a value between 0 and 255")
        duty = self.convert_to_duty(brightness)
        self.set_duty(duty)


class MQTTDimmableLight:
    def __init__(self, mqtt_client, light: DimmableLight,
                 name=None, state_topic=None, command_topic=None,
                 brightness_state_topic=None, brightness_command_topic=None, discovery_topic=None):
        self.mqtt_client = mqtt_client
        self.light = light
        self.name = f"LED-{self.light.timer_n}" if name is None else name
        self.state_topic = state_topic
        self.command_topic = command_topic
        self.brightness_state_topic = brightness_state_topic
        self.brightness_command_topic = brightness_command_topic
        self.discovery_topic = discovery_topic
        # self.topic = f"homeassistant/light/{self.mqtt_client.unit_id}/{self.name.lower().replace(' ', '_')}"
        # self.state_topic = f"{self.topic}/state"
        # self.command_topic = f"{self.topic}/set"
        # self.brightness_state_topic = f"{self.topic}/dim"
        # self.brightness_command_topic = f"{self.topic}/dim/set"
        self.subscribe_to = [self.command_topic, self.brightness_command_topic]

    def publish_state(self):
        self.mqtt_client.publish(self.state_topic, str(self.light.state))
        print(f"\nPublished State: {self.light.state}")

    def publish_brightness(self):
        self.mqtt_client.publish(self.brightness_state_topic, str(self.light.target_brightness))
        print(f"\nPublished Brightness: {self.light.target_brightness}")

    def set_name(self, name):
        self.name = name

    def publish_discovery(self, device_info):
        # discovery_topic = f"{self.topic}/config"
        print(f"{self.name} Discovery Topic: ", self.discovery_topic)
        print(f"{self.name} State Topic: ", self.state_topic)
        config = {
            "name": self.name,
            "device_class": "light",
            "state_topic": self.state_topic,
            "command_topic": self.command_topic,
            "brightness_state_topic": self.brightness_state_topic,
            "brightness_command_topic": self.brightness_command_topic,
            "payload_on": "ON",
            "payload_off": "OFF",
            "optimistic": False,
            "device": device_info,
            "unique_id": f"{self.mqtt_client.config_manager.name}-{self.name}",

        }
        self.mqtt_client.publish(self.discovery_topic, json.dumps(config), retain=True)

    def on_message(self, topic, msg):
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')

        print(f"\nReceived Command:\n\tTopic: {topic}\n\tMessage: {msg}")
        if topic == self.brightness_command_topic:
            try:
                brightness = int(msg)
                self.light.target_brightness = brightness
                self.publish_brightness()
            except ValueError:
                print(f"Invalid brightness value received: {msg}")
        elif topic == self.command_topic:
            if msg == "ON":
                self.light.on()
                self.light.fade()
                self.publish_brightness()
                self.publish_state()

            elif msg == "OFF":
                self.light.off()
                self.light.fade()
                self.publish_brightness()
                self.publish_state()


class HomeLEDDimmer(MQTTDimmableLight):

    def __init__(self, home_client, name, sensor_config, topics, sensor_index):
        self.pin = sensor_config.get('pin')
        freq = sensor_config.get('freq')
        fade_time_ms = sensor_config.get('fade_time_ms')
        brightness_scale = sensor_config.get('brightness_scale')

        super().__init__(mqtt_client=home_client,
                         name=name,
                         state_topic=topics.get('state_topic'),
                         command_topic=topics.get('command_topic'),
                         brightness_state_topic=topics.get('brightness_state_topic'),
                         brightness_command_topic=topics.get('brightness_command_topic'),
                         discovery_topic=topics.get('discovery_topic'),
                         light=DimmableLight(pin=self.pin,
                                             freq=freq,
                                             timer_n=sensor_index,
                                             fade_time_ms=fade_time_ms,
                                             brightness_scale=brightness_scale))

    def __repr__(self):
        return f"<HomeLEDDimmer| {self.name} | pin:{self.pin}>"
