from .lib.umqtt.simple import MQTTClient, MQTTException
import utime


class MQTTManager:
    """
    MQTTManager class helps to manage the MQTT client of the device.
    """

    def __init__(self, unit_id, server, port, username, password):
        """
        Initializes MQTTManager with provided parameters.

        Parameters:
        :param unit_id: (str) The unit id of the device.
        :param server: (str) The MQTT broker server address.
        :param port: (int) The port number of the MQTT broker server.
        :param username: (str) The username for the MQTT broker server.
        :param password: (str) The password for the MQTT broker server.
        """
        self.unit_id = unit_id
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.mqtt_client = None
        self.is_connected = False

    def connect_mqtt(self, clean_session=True):
        """
        Connects to the MQTT broker with provided server, port, username, and password.
        """
        self.mqtt_client = MQTTClient(self.unit_id, self.server, self.port, self.username, self.password, keepalive=60)
        try:
            self.mqtt_client.connect(clean_session)
            self.is_connected = True
            print('Connected to MQTT broker:', self.server)
        except MQTTException:
            print("MQTTException - Try checking connection configs")
            self.is_connected = False
            utime.sleep(5)
        except OSError:
            print("MQTT Connection Error")
            self.is_connected = False
            utime.sleep(10)

    def publish(self, topic, message, **kwargs):
        """
        Publishes a message to a specific topic on the MQTT broker.

        :param topic: The topic to publish the message to.
        :param message: The message to be published.
        """
        try:
            self.mqtt_client.publish(topic, message, **kwargs)
        except OSError:
            print("OSError - possibly lost connection to broker")
            self.is_connected = False
            utime.sleep(3)

    def subscribe(self, topic: str):
        """
        Subscribes to a specific topic on the MQTT broker.

        :param topic: The topic to subscribe to.
        """
        self.mqtt_client.subscribe(topic)

    def set_callback(self, callback_function):
        """
        Sets the callback function that will be called when a message arrives for a subscribed topic.

        :param callback_function: The callback function.
        """
        self.mqtt_client.set_callback(callback_function)

    def check_msg(self):
        """
        Checks for any incoming messages on the subscribed topics.
        """
        try:
            self.mqtt_client.check_msg()
        except OSError:
            print("OSError - possibly lost connection to broker")
            self.is_connected = False
            utime.sleep(3)

    def ping(self):
        try:
            self.mqtt_client.ping()
        except OSError:
            print("OSError - possibly lost connection to broker")
            self.is_connected = False
            utime.sleep(3)
