from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from .models import (
    ModelBase, LogEntry, HomeDevice,
    DeviceSensor, DeviceConfig,
    WifiNetwork, FTPServer, MQTTBroker
)
import os

engine = create_engine(os.getenv('DATABASE_URI'), pool_size=20)
ModelBase.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


# --------- Logs --------- #
def get_logs():
    with Session() as session:
        entries = session.query(LogEntry).all()
        data = [entry.to_dict() for entry in entries]
    return data


def add_log(log_entry):
    with Session() as session:
        new_log = LogEntry(**log_entry)
        session.add(new_log)
        session.commit()
        data = new_log.to_dict()
    return data


def delete_log(log_id):
    with Session() as session:
        session.query(LogEntry).filter(LogEntry.id == log_id).delete()
        session.commit()


# --------- Devices --------- #
def get_devices():
    with Session() as session:
        devices = session.query(HomeDevice).all()
        data = [device.to_dict() for device in devices]
    return data


def get_device(device_id):
    with Session() as session:
        try:
            device = session.query(HomeDevice).filter(HomeDevice.id == device_id).one()
            data = device.to_dict()
        except NoResultFound:
            data = None
    return data


def update_display_name(device_id, new_name):
    with Session() as session:
        try:
            device = session.query(HomeDevice).filter(HomeDevice.id == device_id).one()
            device.display_name = new_name
            device_info = {**device.device_info, 'name': new_name}
            device.device_info = device_info
            print(device.device_info)
            session.commit()
            data = device.to_dict()
        except NoResultFound:
            data = None
    return data


def add_device(device):
    with Session() as session:
        new_device = HomeDevice(**device)
        session.add(new_device)
        session.commit()
        data = new_device.to_dict()
    return data


def delete_device(device_id):
    with Session() as session:
        session.query(HomeDevice).filter(HomeDevice.id == device_id).delete()
        session.commit()


# --------- Device Configs --------- #
def get_device_config(device_id):
    with Session() as session:
        try:
            config = session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).one()
            data = config.to_dict()
        except NoResultFound:
            data = {}
    return data


def update_device_settings(device_id, settings):
    with Session() as session:
        try:
            config = session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).one()
            config.device_settings = settings
            session.commit()
            data = config.to_dict()
        except NoResultFound:
            data = {}
    return data


def delete_device_config(device_id):
    with Session() as session:
        session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).delete()
        session.commit()


def update_device_config(device_id, new_config):
    with Session() as session:
        session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).update({"config": new_config})
        session.commit()


def add_device_config(device_id, wifi_network_id=None, ftp_server_id=None, mqtt_broker_id=None):
    with Session() as session:
        device_config = DeviceConfig(device_id=device_id,
                                     wifi_network_id=wifi_network_id,
                                     ftp_server_id=ftp_server_id,
                                     mqtt_broker_id=mqtt_broker_id)
        session.add(device_config)
        session.commit()
        data = device_config.to_dict()
    return data


# --------- Sensors --------- #
def get_device_sensors(device_config_id):
    with Session() as session:
        sensors = session.query(DeviceSensor).filter(DeviceSensor.device_config_id == device_config_id).all()
        data = [sensor.to_dict() for sensor in sensors]
    return data


def add_sensor(sensor):
    with Session() as session:
        new_sensor = DeviceSensor(**sensor)
        session.add(new_sensor)
        session.commit()
        data = new_sensor.to_dict()
    return data


def update_sensor_config(sensor_id, new_config):
    with Session() as session:
        session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).update({"sensor_config": new_config})
        session.commit()


def delete_sensor(sensor_id):
    with Session() as session:
        session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).delete()
        session.commit()


def get_sensor(sensor_id):
    with Session() as session:
        try:
            sensor = session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).one()
            data = sensor.to_dict()
        except NoResultFound:
            data = {}
    return data


# --------- WiFi Networks --------- #
def add_wifi_network(wifi_network):
    with Session() as session:
        new_wifi_network = WifiNetwork(**wifi_network)
        session.add(new_wifi_network)
        session.commit()
        data = new_wifi_network.to_dict()
    return data


def update_wifi_network(wifi_network_id, new_wifi_network):
    with Session() as session:
        session.query(WifiNetwork).filter(WifiNetwork.id == wifi_network_id).update(new_wifi_network)
        session.commit()


def delete_wifi_network(wifi_network_id):
    with Session() as session:
        session.query(WifiNetwork).filter(WifiNetwork.id == wifi_network_id).delete()
        session.commit()


def get_all_wifi_networks():
    with Session() as session:
        wifi_networks = session.query(WifiNetwork).all()
        data = [network.to_dict() for network in wifi_networks]
    return data


def get_wifi_network(wifi_network_id):
    with Session() as session:
        try:
            wifi_network = session.query(WifiNetwork).filter(WifiNetwork.id == wifi_network_id).one()
            data = wifi_network
        except NoResultFound:
            data = {}
    return data


# --------- FTP Servers --------- #
def add_ftp_server(ftp_server):
    with Session() as session:
        new_ftp_server = FTPServer(**ftp_server)
        session.add(new_ftp_server)
        session.commit()
        data = new_ftp_server.to_dict()
    return data


def update_ftp_server(ftp_server_id, new_ftp_server):
    with Session() as session:
        session.query(FTPServer).filter(FTPServer.id == ftp_server_id).update(new_ftp_server)
        session.commit()


def delete_ftp_server(ftp_server_id):
    with Session() as session:
        session.query(FTPServer).filter(FTPServer.id == ftp_server_id).delete()
        session.commit()


def get_ftp_server(ftp_server_id):
    with Session() as session:
        try:
            ftp_server = session.query(FTPServer).filter(FTPServer.id == ftp_server_id).one()
            data = ftp_server
        except NoResultFound:
            data = {}
    return data


def get_all_ftp_servers():
    with Session() as session:
        ftp_servers = session.query(FTPServer).all()
        data = [server.to_dict() for server in ftp_servers]
    return data


# --------- MQTT Brokers --------- #
def add_mqtt_broker(mqtt_broker):
    with Session() as session:
        new_mqtt_broker = MQTTBroker(**mqtt_broker)
        session.add(new_mqtt_broker)
        session.commit()
        data = new_mqtt_broker.to_dict()
    return data


def update_mqtt_broker(mqtt_broker_id, new_mqtt_broker):
    with Session() as session:
        session.query(MQTTBroker).filter(MQTTBroker.id == mqtt_broker_id).update(new_mqtt_broker)
        session.commit()


def delete_mqtt_broker(mqtt_broker_id):
    with Session() as session:
        session.query(MQTTBroker).filter(MQTTBroker.id == mqtt_broker_id).delete()
        session.commit()


def get_mqtt_broker(mqtt_broker_id):
    with Session() as session:
        try:
            mqtt_broker = session.query(MQTTBroker).filter(MQTTBroker.id == mqtt_broker_id).one()
            data = mqtt_broker
        except NoResultFound:
            data = {}
    return data


def get_all_mqtt_brokers():
    with Session() as session:
        mqtt_brokers = session.query(MQTTBroker).all()
        data = [broker.to_dict() for broker in mqtt_brokers]
    return data
