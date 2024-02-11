import json
import urequests
import home.Home as home
import sys
import machine
import ubinascii


class ConfigError(Exception):
    pass


class WifiConfig:
    def __init__(self, id, ssid, password, is_default):
        self.ssid = ssid
        self.password = password


class MQTTConfig:
    def __init__(self, id, host_address, port, username, password, is_default):
        self.host = host_address
        self.port = port
        self.username = username
        self.password = password


class FTPConfig:
    def __init__(self, id, host_address, username, password, is_default):
        self.host = host_address
        self.username = username
        self.password = password


class ConfigManager:
    start_up_settings_path = '/config.json'
    last_run_config_path = '/last-run-config.json'
    start_up_settings = None
    wifi_ssid = None
    wifi_password = None
    host = None
    name = None
    home_device = None
    device_config = None
    device_info = None
    sensors = None
    wifi = None
    mqtt = None
    ftp = None
    led_on_after_connect = True
    use_ping = True

    def __save_last_run_config(self):
        with open(self.last_run_config_path, 'w') as f:
            json.dump(self.home_device, f)

    def __load_last_run_config(self):
        try:
            with open(self.last_run_config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print("load last run config error: ", e)
            return None

    def __save_startup_settings(self):
        with open(self.start_up_settings_path, 'w') as f:
            json.dump({
                "host": self.host,
                "wifi_ssid": self.wifi_ssid,
                "wifi_password": self.wifi_password
            }, f)

    def __load_startup_settings(self):
        try:
            with open(self.start_up_settings_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print("load startup settings error: ", e)
            return None

    def __init__(self, home_client: home.Home):
        self.home_client = home_client
        self.device_id = ubinascii.hexlify(machine.unique_id()).decode()
        self.platform = sys.platform

    def get_startup_settings(self):
        self.start_up_settings = self.__load_startup_settings()
        self.host = self.start_up_settings.get('host')
        self.wifi_ssid = self.start_up_settings.get('wifi_ssid')
        self.wifi_password = self.start_up_settings.get('wifi_password')

    def request_device_config(self):
        url = f'{self.host}/api/home/devices/{self.device_id}'
        print(f'requesting settings from: {url}')

        response = urequests.get(url)
        if response.status_code == 200:
            print(f'received settings')
            self.home_device = response.json()

    def announce_device_to_home_server(self):
        response = urequests.post(f'{self.host}/api/home/devices/add', json={
            "id": self.device_id,
            "platform": self.platform,
            "display_name": self.name,
            "device_info": {
                "name": self.name,
                "manufacturer": "ZRW",
                "model": f"{self.platform.upper()}-Circuit",
                "identifiers": self.device_id
            }})
        print("announcing device...")
        if response.status_code == 200:
            data = response.json()
            print("device added")
            self.home_device = data['device']

    def parse_config(self):
        self.name = self.home_device.get('display_name')
        self.device_config = self.home_device.get('config')
        self.device_info = self.home_device.get('device_info')
        self.sensors = self.device_config.get('sensors')

        device_settings = self.device_config.get('device_settings')
        if device_settings is not None:
            led_on = device_settings.get('led_on_after_connect')
            self.led_on_after_connect = led_on if led_on is not None else self.led_on_after_connect
            use_ping = device_settings.get('use_ping')
            self.use_ping = use_ping if use_ping is not None else self.use_ping

        wifi_config = self.device_config.get('wifi_network')
        mqtt_config = self.device_config.get('mqtt_broker')
        ftp_config = self.device_config.get('ftp_server')
        self.wifi = WifiConfig(**wifi_config) if wifi_config is not None else None
        self.mqtt = MQTTConfig(**mqtt_config) if mqtt_config is not None else None
        self.ftp = FTPConfig(**ftp_config) if ftp_config is not None else None

    def obtain_config(self):
        self.request_device_config()
        if self.home_device is not None:
            self.__save_last_run_config()
        if self.home_device is None:
            self.__load_last_run_config()
        if self.home_device is None:
            self.announce_device_to_home_server()
        if self.home_device is None:
            raise ConfigError('Unable to locate device configs')

    def update_host(self, new_host):
        self.host = new_host
        has_host = self.host is not None and self.host
        has_wifi_ssid = self.wifi_ssid is not None and self.wifi_ssid
        has_wifi_password = self.wifi_password is not None and self.wifi_password
        if has_host and has_wifi_ssid and has_wifi_password:
            self.__save_startup_settings()
