import machine
import json
from ..Timer import Timer


class MotionSensor:

    def __init__(self, pin, retrigger_delay_ms, timer_n=1):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.retrigger_delay_ms = retrigger_delay_ms

        self.on_motion_detected = None
        self.on_motion_not_detected = None

        self.timer_n = timer_n
        self.timer = None
        self.last_motion = 0

    def enable_interrupt(self):
        """Enable interrupt for motion pin."""
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.motion_change)

    def set_on_motion_detected(self, func):
        self.on_motion_detected = func

    def set_on_motion_not_detected(self, func):
        self.on_motion_not_detected = func

    def set_timer_n(self, timer_n):
        self.timer_n = timer_n

    def motion_change(self, _):
        self._motion_detected()
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        self.timer = Timer(timer_number=self.timer_n * -1,
                           mode=Timer.ONE_SHOT,
                           period=self.retrigger_delay_ms,
                           callback=self._no_motion_detected)

    def _motion_detected(self):
        if not self.last_motion:
            self.last_motion = 1
            if self.on_motion_detected is not None:
                self.on_motion_detected()

    # def _no_motion_detected(self, _):
    def _no_motion_detected(self):
        self.last_motion = 0
        if self.on_motion_not_detected is not None:
            self.on_motion_not_detected()


class MQTTMotionSensor:
    def __init__(self, motion_sensor: MotionSensor, mqtt_client, name=None, state_topic=None, discovery_topic=None):
        self.motion_sensor = motion_sensor
        self.mqtt_client = mqtt_client
        self.sensor_index = self.motion_sensor.timer_n

        self.name = name
        self.state_topic = state_topic
        self.discovery_topic = discovery_topic
        self.motion_sensor.set_on_motion_detected(self.publish_last_motion)
        self.motion_sensor.set_on_motion_not_detected(self.publish_last_motion)

    def enable_interrupt(self):
        self.motion_sensor.enable_interrupt()

    def publish_last_motion(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.publish(self.state_topic, str(self.motion_sensor.last_motion))

    def publish_discovery(self, device_info):
        print("Motion Sensor Discovery Topic: ", self.discovery_topic)
        print("Motion Sensor State Topic: ", self.state_topic)
        config = {
            "name": self.name,
            "device_class": "motion",
            "device": device_info,
            "unique_id": f"{device_info.get('name')}-{self.name}",
            "payload_off": "0",
            "payload_on": "1",
            "state_topic": self.state_topic
        }
        self.mqtt_client.publish(self.discovery_topic, json.dumps(config), retain=True)


class HomeMotionSensor(MQTTMotionSensor):
    def __init__(self, home_client, name, sensor_config, topics, sensor_index):
        self.pin = sensor_config.get('pin')
        retrigger_delay_ms = sensor_config.get('retrigger_delay_ms')
        super().__init__(mqtt_client=home_client,
                         name=name,
                         state_topic=topics.get('state_topic'),
                         discovery_topic=topics.get('discovery_topic'),
                         motion_sensor=MotionSensor(pin=self.pin,
                                                    retrigger_delay_ms=retrigger_delay_ms,
                                                    timer_n=sensor_index))

    def __repr__(self):
        return f"<HomeMotionSensor| {self.name} | pin:{self.pin}>"
