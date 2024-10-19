import machine
import sys
import json


class Fan:

    def __init__(self, enable_pin, pwm_pin, freq):
        self._platform = sys.platform

        if self._platform not in ['rp2', 'esp32']:
            raise ValueError(f"Unsupported platform: {self._platform}")

        if self._platform == "rp2":
            self.pwm_pin = machine.PWM(machine.Pin(pwm_pin))
            self.pwm_pin.freq(freq)
        elif self._platform == "esp32":
            self.pwm_pin = machine.PWM(machine.Pin(pwm_pin), freq=freq)

        self.enable_pin = machine.Pin(enable_pin, machine.Pin.OUT)
        # self.pwm_pin = machine.PWM(machine.Pin(pwm_pin))
        self.power_scale = 100
        self.state = "OFF"
        self.percentage = 50

    def on(self):
        self.state = "ON"
        self.enable_pin.on()

    def off(self):
        self.state = "OFF"
        self.enable_pin.off()

    def set_duty_cycle(self, duty_cycle):
        if self._platform == "rp2":
            self.pwm_pin.duty_u16(duty_cycle)
        elif self._platform == "esp32":
            self.pwm_pin.duty(duty_cycle)

    def set_freq(self, freq):
        self.pwm_pin.freq(freq)

    def set_power_scale(self, power_scale):
        self.power_scale = power_scale

    def convert_to_duty(self, value: int) -> int:
        if self._platform == "rp2":
            return round((65535 / self.power_scale) * value)
        elif self._platform == "esp32":
            return round((1023 / self.power_scale) * value)
        else:
            return value

    def set_power(self, power):
        self.percentage = power
        duty = self.convert_to_duty(power)
        self.set_duty_cycle(duty)
        print(f'setting power to: {self.percentage}')


class MQTTFan:

    def __init__(self, mqtt_client, fan: Fan,
                 name=None, state_topic=None, command_topic=None,
                 percentage_state_topic=None, percentage_command_topic=None, discovery_topic=None, availability_topic=None):
        self.mqtt_client = mqtt_client
        self.fan = fan
        self.name = f"MQTTFan" if name is None else name
        self.state_topic = state_topic
        self.command_topic = command_topic
        self.percentage_state_topic = percentage_state_topic
        self.percentage_command_topic = percentage_command_topic
        self.discovery_topic = discovery_topic
        self.availability_topic = availability_topic
        self.subscribe_to = [self.command_topic, self.percentage_command_topic]

    def publish_state(self):
        self.mqtt_client.publish(self.state_topic, str(self.fan.state))
        print(f"\nPublished State: {self.fan.state}")

    def publish_percentage(self):
        self.mqtt_client.publish(self.percentage_state_topic, str(self.fan.percentage))
        print(f"\nPublished Percentage: {self.fan.percentage}")

    def publish_availability(self):
        if self.availability_topic is not None:
            self.mqtt_client.publish(self.availability_topic, "online")
            print(f"\nPublished Fan Availability: online")

    def set_name(self, name):
        self.name = name

    def publish_discovery(self, device_info):
        print(f"{self.name} Discovery Topic: ", self.discovery_topic)
        print(f"{self.name} State Topic: ", self.state_topic)
        config = {
            "name": self.name,
            "device_class": "fan",
            "state_topic": self.state_topic,
            "command_topic": self.command_topic,
            "percentage_state_topic": self.percentage_state_topic,
            "percentage_command_topic": self.percentage_command_topic,
            "payload_on": "ON",
            "payload_off": "OFF",
            "optimistic": False,
            "device": device_info,
            "unique_id": f"{self.mqtt_client.config_manager.name}-{self.name}",

        }
        if self.availability_topic is not None:
            config["availability"] = [{'topic': self.availability_topic}]
        self.mqtt_client.publish(self.discovery_topic, json.dumps(config), retain=True)

    def on_message(self, topic, msg):
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')

        print(f"\nReceived Command:\n\tTopic: {topic}\n\tMessage: {msg}")
        if topic == self.percentage_command_topic:
            try:
                percentage = int(msg)
                self.fan.percentage = percentage
                self.fan.set_power(percentage)
            except ValueError:
                print(f"Invalid brightness value received: {msg}")
        elif topic == self.command_topic:
            if msg == "ON":
                self.fan.on()
                self.publish_state()

            elif msg == "OFF":
                self.fan.off()
                self.publish_state()


class HomeFan(MQTTFan):

    def __init__(self, home_client, name, sensor_config, topics, sensor_index=None):
        self.pin = sensor_config.get('pin')
        self.enable_pin = sensor_config.get('enable_pin')
        self.sensor_index = sensor_index
        freq = sensor_config.get('freq')
        super().__init__(mqtt_client=home_client,
                         name=name,
                         state_topic=topics.get('state_topic'),
                         command_topic=topics.get('command_topic'),
                         percentage_state_topic=topics.get('percentage_state_topic'),
                         percentage_command_topic=topics.get('percentage_state_topic'),
                         discovery_topic=topics.get('discovery_topic'),
                         availability_topic=topics.get('availability_topic'),
                         fan=Fan(pwm_pin=self.pin, enable_pin=self.enable_pin, freq=freq))

    def __repr__(self):
        return f"<HomeFan| {self.name} | pin:{self.pin}>"

    def force_update(self):
        self.publish_availability()
        self.publish_state()
        self.publish_percentage()

