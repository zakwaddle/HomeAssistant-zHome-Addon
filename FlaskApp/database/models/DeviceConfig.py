from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase


class DeviceConfig(ModelBase):
    __tablename__ = 'device-configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String, ForeignKey('home-devices.id'), unique=True)  # one-to-one relationship
    device_settings = Column(JSON)
    wifi_network_id = Column(Integer, ForeignKey('wifi-networks.id'))
    ftp_server_id = Column(Integer, ForeignKey('ftp-servers.id'))
    mqtt_broker_id = Column(Integer, ForeignKey('mqtt-brokers.id'))

    wifi_network = relationship("WifiNetwork", uselist=False)
    ftp_server = relationship("FTPServer", uselist=False)
    mqtt_broker = relationship("MQTTBroker", uselist=False)

    device = relationship("HomeDevice", back_populates="config")  # one-to-one relationship
    # sensors = relationship("DeviceSensor", back_populates="device_config")  # one-to-many relationship
    sensors = relationship("DeviceSensor", back_populates="device_config", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DeviceConfig - {self.id} | {self.device_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_settings": self.device_settings,
            "wifi_network": self.wifi_network.to_dict() if self.wifi_network else None,
            "ftp_server": self.ftp_server.to_dict() if self.ftp_server else None,
            "mqtt_broker": self.mqtt_broker.to_dict() if self.mqtt_broker else None,
            "sensors": [s.to_dict() for s in self.sensors] if self.sensors else []
        }
