import home.Home
from ..sensors import HomeMotionSensor, HomeWeatherSensor, HomeLEDDimmer, HomeFan, HomeButton


class SensorManager:
    __sensors = {
            "motion": HomeMotionSensor,
            "led": HomeLEDDimmer,
            "fan": HomeFan,
            "weather": HomeWeatherSensor,
            "button": HomeButton,
        }
    
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
            
            Sensor = self.__sensors.get(sensor_type)
            if Sensor is not None:
                sensor = Sensor(self.home_client, name, sensor_config, topics, sensor_index)
                sensor.setup(self.device_info)
                self.sensors.append(sensor)
                self.home_client.log(f"sensor {sensor} online")

    def publish_online(self):
        for sensor in self.sensors:
            try:
                sensor.publish_online()
            except Exception as e:
                self.home_client.log(f"error publishing {sensor} online: {e}", log_type="error")

    def publish_offline(self):
        for sensor in self.sensors:
            try:
                sensor.publish_offline()
            except Exception as e:
                self.home_client.log(f"error publishing {sensor} offline: {e}", log_type="error")

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

