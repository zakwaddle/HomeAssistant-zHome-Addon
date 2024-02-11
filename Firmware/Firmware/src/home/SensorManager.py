import home.Home
from .sensors import HomeMotionSensor, HomeWeatherSensor, HomeLEDDimmer


class SensorManager:

    def __init__(self, home_client: home.Home):
        self.home_client = home_client
        self.sensor_configs = self.home_client.config_manager.sensors
        self.device_info = self.home_client.config_manager.device_info
        self.sensors = []

    def create_sensors(self):
        for i in self.sensor_configs:
            sensor_type = i.get('sensor_type')
            name = i.get('name')
            sensor_config = i.get('sensor_config')
            topics = sensor_config.get('topics') if sensor_config is not None else None
            sensor_index = self.sensor_configs.index(i) + 1
            if sensor_type == "motion":
                self.create_motion_sensor(name, sensor_config, topics, sensor_index)
            elif sensor_type == "led":
                self.create_led_dimmer(name, sensor_config, topics, sensor_index)
            elif sensor_type == "weather":
                self.create_weather_sensor(name, sensor_config, topics, sensor_index)

    def create_motion_sensor(self, name, sensor_config, topics, sensor_index):
        motion = HomeMotionSensor(self.home_client, name, sensor_config, topics, sensor_index)
        motion.publish_discovery(self.device_info)
        motion.enable_interrupt()
        self.sensors.append(motion)

    def create_led_dimmer(self, name, sensor_config, topics, sensor_index):
        led = HomeLEDDimmer(self.home_client, name, sensor_config, topics, sensor_index)
        led.publish_discovery(self.device_info)
        led.publish_brightness()
        led.publish_state()
        self.sensors.append(led)

    def create_weather_sensor(self, name, sensor_config, topics, sensor_index):
        measurement_interval_ms = sensor_config.get('measurement_interval_ms')
        weather = HomeWeatherSensor(self.home_client, name, sensor_config, topics, sensor_index)
        weather.publish_discovery(self.device_info)
        weather.enable_interrupt(measurement_interval_ms)
        self.sensors.append(weather)

    def subscribe_sensors(self):
        for s in self.sensors:
            print("\nsubscribing sensor: ", s)
            if hasattr(s, 'subscribe_to'):
                for t in s.subscribe_to:
                    print("\tsubscribed to: ", t)
                    self.home_client.subscribe(t)

    def on_message(self, topic, msg):
        for s in self.sensors:
            if hasattr(s, 'on_message'):
                s.on_message(topic, msg)



