import utime
import machine
import json
from .WiFiManager import WiFiManager
from .MQTTManager import MQTTManager
from .UpdateManager import UpdateManager
from .sensors.StatusLED import StatusLED
from .SensorManager import SensorManager
from .ConfigManager import ConfigManager
from .CommandMessage import CommandMessage, MessageError
from .Timer import Timer


class HomeError(Exception):
    pass


class Home:
    wifi_manager: WiFiManager = None
    mqtt_manager: MQTTManager = None
    update_manager: UpdateManager = None
    sensor_manager: SensorManager = None
    device_info = None
    device_configs = None
    sensor_configs = None

    @staticmethod
    def restart_device(delay_seconds=None):
        if delay_seconds is not None:
            utime.sleep(delay_seconds)
        machine.reset()

    @staticmethod
    def status_led_off():
        light = StatusLED()
        light.off()

    @staticmethod
    def status_led_on():
        light = StatusLED()
        light.on()

    @staticmethod
    def status_led_blink():
        light = StatusLED()
        light.blink_light()

    def log(self, log_message, log_type='info'):
        print(log_message)
        if self.mqtt_manager is not None and self.mqtt_manager.is_connected:
            self.publish(self.log_topic, json.dumps({
                "unit_id": self.config_manager.device_id,
                "display_name": self.config_manager.name,
                "message": log_message,
                "type": log_type
            }))

    def restart_on_error(self, error_message):
        self.log(f'{error_message} - Restarting', log_type='error')
        self.status_led_off()
        self.restart_device(delay_seconds=5)

    def __init__(self):
        self.config_manager = ConfigManager(self)
        self.device_id = self.config_manager.device_id
        if self.config_manager.platform not in ['rp2', 'esp32']:
            raise HomeError(f"Unsupported platform: {self.config_manager.platform}")

        self.command_topic = f"command/#"
        self.log_topic = f"z-home/log/{self.device_id}"
        self.timer = None
        self.sensors = []
        print("\nPlatform: ", self.config_manager.platform, "\nUnit: ", self.device_id)

    def connect_wifi(self, ssid, password):
        self.wifi_manager = WiFiManager(ssid, password)
        print("\nconnecting Wi-Fi")
        self.wifi_manager.connect_wifi()

    def connect_mqtt(self):
        if self.config_manager.mqtt is None:
            raise HomeError("no mqtt connection details found")
        self.mqtt_manager = MQTTManager(unit_id=self.config_manager.device_id,
                                        server=self.config_manager.mqtt.host,
                                        port=self.config_manager.mqtt.port,
                                        username=self.config_manager.mqtt.username,
                                        password=self.config_manager.mqtt.password)
        print("\nconnecting MQTT")
        self.mqtt_manager.connect_mqtt()

    def connect_ftp(self):
        if self.config_manager.ftp is not None:
            self.update_manager = UpdateManager(observer_func=self.log,
                                                host=self.config_manager.ftp.host,
                                                user=self.config_manager.ftp.username,
                                                password=self.config_manager.ftp.password)

    def check_connections(self):
        """
        Checks the Wi-Fi connection and reconnects if the connection is lost.
        """
        if not self.wifi_manager.is_connected():
            print('Lost Wi-Fi connection. Reconnecting...')
            self.wifi_manager.connect_wifi()
            self.log("Reconnected Wifi")
        if not self.mqtt_manager.is_connected:
            self.mqtt_manager.connect_mqtt()
            self.setup_subscriptions()
            self.log("Reconnected MQTT")
        else:
            if self.config_manager.use_ping:
                self.mqtt_ping()

    def set_connection_check_timer(self):
        self.timer = Timer(timer_number=0, period=5000, mode=machine.Timer.PERIODIC, callback=self.check_connections)

    def setup_sensors(self):
        if self.config_manager.sensors is None:
            return
        self.sensor_manager = SensorManager(self)
        self.sensor_manager.create_sensors()

    def setup_subscriptions(self):
        self.set_callback(self.on_message)
        self.subscribe(self.command_topic)
        if self.sensor_manager is not None:
            self.sensor_manager.subscribe_sensors()

    def start_sequence(self):
        self.config_manager.get_startup_settings()
        self.connect_wifi(self.config_manager.wifi_ssid, self.config_manager.wifi_password)
        self.config_manager.obtain_config()
        self.config_manager.parse_config()
        self.connect_mqtt()
        self.connect_ftp()

        connected = self.wifi_manager.is_connected() and self.mqtt_manager.is_connected
        if not connected:
            raise HomeError("Wi-Fi and MQTT Connection Error")
        self.log("Connected to Wifi and MQTT\n")

        self.set_connection_check_timer()
        self.setup_sensors()
        self.setup_subscriptions()
        print(self.sensor_manager.sensors)

        self.status_led_blink()
        if self.config_manager.led_on_after_connect:
            self.status_led_on()

    def on_message(self, topic, msg):

        self.sensor_manager.on_message(topic, msg)

        def should_respond():
            t = topic.decode('utf-8')
            to_unit_id = t == f'command/{self.config_manager.device_id}'
            to_all_units = t == 'command/all-units'
            to_display_name = t == f'command/{self.config_manager.name}'
            return to_unit_id or to_all_units or to_display_name

        if should_respond():
            try:
                command = CommandMessage(self, msg)
                command.execute_command()
            except MessageError as e:
                self.log(f'MessageError: {e.args}', log_type='error')
            except Exception as e:
                self.log(f"Error in Home.on_message: {e}", log_type='error')

    def publish(self, topic, message, **kwargs):
        """
        Publishes a message to a specific topic on the MQTT broker.

        :param topic: The topic to publish the message to.
        :param message: The message to be published.
        """
        self.mqtt_manager.publish(topic, message, **kwargs)

    def subscribe(self, topic):
        """
        Subscribes to a specific topic on the MQTT broker.

        :param topic: The topic to subscribe to.
        """
        self.mqtt_manager.subscribe(topic)

    def set_callback(self, callback_function):
        """
        Sets the callback function for MQTT messages.
        :param callback_function: The callback function.
        """
        self.mqtt_manager.set_callback(callback_function)

    def check_msg(self):
        """
        Checks for MQTT messages.
        """
        self.mqtt_manager.check_msg()

    def mqtt_ping(self):
        self.mqtt_manager.ping()
