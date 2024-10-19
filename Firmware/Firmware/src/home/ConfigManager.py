import json
import urequests
import home
import sys
import machine
import ubinascii


class ConfigError(Exception):
    pass


class WifiConfig:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password


class MQTTConfig:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password


class FTPConfig:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password


class ConfigManager:
    version = None
    start_up_settings_path = '/config.json'
    last_run_config_path = '/last-run-config.json'
    start_up_settings = None
    wifi_ssid = None
    wifi_password = None
    host_name = None
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
    has_hard_pins = False

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
            json.dump(self.start_up_settings, f)

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
        self.version = self.start_up_settings.get("version")
        print('Home Version: ', self.version) 
        self.host_name = self.start_up_settings.get('host')
        log_level = self.start_up_settings.get("log_level")
        if log_level is not None:
            self.home_client.log_level = log_level
        if self.host_name is not None:
            self.host = f"http://{self.host_name}.local:5000"
            
        wifi = self.start_up_settings.get('wifi')
        self.wifi = WifiConfig(**wifi) if wifi is not None else None
        

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
                "model": f"{self.platform.upper()}-{self.start_up_settings.get('model')}",
                "identifiers": self.device_id,
                "sw_version": self.start_up_settings.get('version')
            }})
        print("announcing device...")
        if response.status_code == 200:
            data = response.json()
            print("device added")
            self.home_device = data['device']


    def update_device_on_home_server(self):
        firmware_version = self.start_up_settings.get('version')
        server_device = self.home_device if self.home_device is not None else None
        device_info = server_device.get('device_info') if server_device is not None else None
        server_version = device_info.get("sw_version")
        print(server_version, firmware_version)
        if device_info.get("sw_version") != firmware_version:
            response = urequests.post(f'{self.host}/api/home/devices/{self.home_device.get('id')}/firmware_version', json={
                "new_version": firmware_version
                })
            if response.status_code == 200:
                print(f"updated version on home server to {firmware_version}")
            

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


    def obtain_config(self):
        self.get_mqtt_details()
        self.get_ftp_details()
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

    def get_mqtt_details(self):
        response = urequests.get(f'{self.host}/api/mqtt')
        if response.status_code == 200:
            mqtt = response.json()
            mqtt_host = f"{self.host_name}.local"
            self.mqtt = MQTTConfig(
                host=mqtt_host, 
                port=mqtt.get("port"), 
                username=mqtt.get("username"), 
                password=mqtt.get("password")
                )
        
    def get_ftp_details(self):
        ftp = self.start_up_settings.get('ftp')
        self.ftp = FTPConfig(**ftp) if ftp is not None else None

    def update_log_level(self, new_log_level:int):
        if 0 < new_log_level < 6:
            self.start_up_settings['log_level'] = new_log_level
            self.__save_startup_settings
            self.home_client.log_level = new_log_level
            self.home_client.log(f"updated log_level to: {new_log_level}", log_level=2)
