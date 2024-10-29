import utime
import machine
import sys
import json
from .managers import WiFiManager, MQTTManager, UpdateManager, SensorManager, ConfigManager, CommandMessage, MessageError
from .sensors import Timer, StatusLED


class HomeError(Exception):
    pass


class Home:
    log_level = 1
    wifi_manager: WiFiManager = None
    mqtt_manager: MQTTManager = None
    update_manager: UpdateManager = None
    sensor_manager: SensorManager = None
    device_info = None
    device_configs = None
    sensor_configs = None
    __log_hook_func = None

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

    def set_log_hook(self, hook_func):
        if isinstance(hook_func, function):
            self.__log_hook_func = hook_func

    def __log_hook(self, log_message):
        if self.__log_hook_func is not None:
            self.__log_hook_func(log_message)

    def log(self, log_message, log_type='info', log_level=1):
        print("logged: ", log_message)
        self.__log_hook(log_message)
        can_log = self.mqtt_manager is not None and self.mqtt_manager.is_connected
        should_log = self.log_level <= log_level
        if can_log and should_log:
            self.publish(self.log_topic, json.dumps({
                "unit_id": self.config_manager.device_id,
                "display_name": self.config_manager.name,
                "message": log_message,
                "type": log_type,
                "level": log_level,
                "version": self.config_manager.version
            }))

    def restart_on_error(self, error_message):
        self.log(f'{error_message} - Restarting', log_type='error', log_level=1)
        self.status_led_off()
        self.sensor_manager.publish_offline()
        self.restart_device(delay_seconds=5)

    def __init__(self):
        self.log("initializing home client", log_level=5)
        self.config_manager = ConfigManager(self)
        self.device_id = self.config_manager.device_id
        if self.config_manager.platform not in ['rp2', 'esp32']:
            raise HomeError(f"Unsupported platform: {self.config_manager.platform}")
        self.ha_topic = "homeassistant/status"
        self.command_topic = f"command/#"
        self.disconnect_topic = "z-home/disconnect"
        self.log_topic = f"z-home/log/{self.device_id}"
        self.timer = None
        self.sensors = []
        self.subscriptions = []
        self.msg_observer_func = None
        print("\nPlatform: ", self.config_manager.platform, "\nUnit: ", self.device_id)

    def add_subscriptions(self, *topics):
        for topic in topics:
            self.subscriptions.append(topic)
    
    def set_msg_observer(self, f):
        self.msg_observer_func = f

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
        self.setup_disconnect()
        self.mqtt_manager.connect_mqtt()
        if self.mqtt_manager.is_connected:
            self.log("Connected MQTT", log_level=2)
        else:
            self.log("Could Not Connect MQTT", log_level=2, log_type='error')

    def connect_ftp(self):
        if self.config_manager.ftp is not None:
            print('\nconnecting FTP')
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
            self.setup_disconnect()
            self.mqtt_manager.connect_mqtt()
            self.setup_subscriptions()
            self.log("Reconnected MQTT")
            self.force_update_sensors()
        else:
            if self.config_manager.use_ping:
                self.mqtt_ping()

    def set_connection_check_timer(self):
        self.timer = Timer(timer_number=0, period=5000, mode=machine.Timer.PERIODIC, callback=self.check_connections)

    def setup_sensors(self):
        if self.config_manager.sensors is None:
            return
        self.sensor_manager = SensorManager(self)
        self.log("creating sensors", log_level=3)
        self.sensor_manager.create_sensors()

    def get_availibity_topics(self):
        if self.config_manager.sensors is None:
            return []
        else:
            topics = []
            for i in self.config_manager.sensors:
                sensor_config = i.get('sensor_config')
                t = sensor_config.get('topics') if sensor_config is not None else None
                if t is not None:
                    a = t.get("availability_topic")
                    if a is not None:
                        topics.append(a)
                    elif a is None:
                        a = t.get("temperature_availability_topic")
                        b = t.get("humidity_availability_topic")
                        if a is not None and b is not None:
                            topics.append(a)
                            topics.append(b)
            return topics
    
    def setup_disconnect(self):
        topics = self.get_availibity_topics()
        self.mqtt_set_last_will("z-home/disconnect", json.dumps({"availability_topics": topics}))

    def setup_subscriptions(self):
        self.log("setting message callback and subscriptions", log_level=3)
        self.set_callback(self.on_message)
        self.subscribe(self.command_topic)
        self.subscribe(self.ha_topic)
        for i in self.subscriptions:
            self.subscribe(i)
            print(f"subscribed to: {i}")
        if self.sensor_manager is not None:
            self.sensor_manager.subscribe_sensors()

    def start_sequence(self):
        self.config_manager.get_startup_settings()
        wifi = self.config_manager.wifi
        self.connect_wifi(wifi.ssid, wifi.password)
        self.config_manager.obtain_config()
        self.config_manager.parse_config()
        self.connect_mqtt()
        self.connect_ftp()

        connected = self.wifi_manager.is_connected() and self.mqtt_manager.is_connected
        if not connected:
            raise HomeError("Wi-Fi and MQTT Connection Error")
        self.log("Connected to Wifi and MQTT\n")
        self.config_manager.update_device_on_home_server()

        self.set_connection_check_timer()
        self.setup_sensors()
        self.setup_subscriptions()
        print("sensors: " ,self.sensor_manager.sensors)

        self.status_led_blink()
        if self.config_manager.led_on_after_connect:
            self.status_led_on()

    def force_update_sensors(self):
        for i in self.sensor_manager.sensors:
            try:
                i.force_update()
            except Exception as e:
                self.log(f'sensor update error: {e}', log_type='error')
                

    def msg_observer(self, topic, msg):
        if self.msg_observer_func is not None:
            # print(f"message observer got = \ntopic: {topic}\nmessage: {msg}")
            self.msg_observer_func(topic, msg)

    def on_message(self, topic, msg):

        self.sensor_manager.on_message(topic, msg)

        tp = topic.decode('utf-8')
        ms = msg.decode('utf-8')

        self.msg_observer(topic, msg)

        if tp == self.ha_topic:
            if ms == "online":
                self.force_update_sensors()
                # for i in self.sensor_manager.sensors:
                #     try:
                #         i.force_update()
                #     except Exception as e:
                #         self.log(f'message error: {e}')
                #         print(f'message error: {e}')
                self.log("force updated sensors")

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
        # print(f"\n--- publshing to topic: {topic}\n--- payload:{message}")
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

    def mqtt_set_last_will(self, topic, message):
        self.mqtt_manager.set_last_will(topic=topic, message=message)



def run():
    def disconnect(client):
        try:
            home_client.mqtt_manager.disconnect()
            print("disconnected mqtt")
        except Exception as e:
            print(f"mqtt disconnect error")

    while True:
        home_client = Home()
        try:
            home_client.start_sequence()
            home_client.log("---listening for messages---")
            while True:
                home_client.check_msg()
                utime.sleep_ms(100)

        except KeyboardInterrupt:
            Home.status_led_off()
            # disconnect(home_client)
            raise KeyboardInterrupt
        except Exception as e:
            # disconnect(home_client)
            home_client.restart_on_error(f'Main Loop Error: \n\t{sys.print_exception(e)}')