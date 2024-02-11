import network
import utime
import machine
import sys


class WiFiManager:
    """
    WiFiManager class helps to manage the WiFi connectivity of the device.
    """

    def __init__(self, ssid, password, max_retries=3, retry_delay=5):
        """
        Initializes WiFiManager with provided ssid and password.

        Parameters:
        ssid (str): The SSID of the WiFi network to connect.
        password (str): The password of the WiFi network to connect.
        max_retries (int): The maximum number of retries for WiFi connection attempts. Default is 3.
        retry_delay (int): The delay in seconds between WiFi connection attempts. Default is 5.
        """
        self.ssid = ssid
        self.password = password
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.wlan = None

    def connect_wifi(self):
        """
        Connects to the WiFi network with provided ssid and password.

        Returns:
        None
        """
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        retry_counter = 0
        while not self.wlan.isconnected():
            if retry_counter >= self.max_retries:
                print('Failed to connect to WiFi after', self.max_retries, 'attempts.')
                return
            print('Connecting to', self.ssid)
            self.wlan.connect(self.ssid, self.password)
            utime.sleep(self.retry_delay)
            retry_counter += 1
        print('Connected to Wi-Fi:', self.ssid)
        print('IP address:', self.wlan.ifconfig()[0])

    def is_connected(self):
        return self.wlan.isconnected()

