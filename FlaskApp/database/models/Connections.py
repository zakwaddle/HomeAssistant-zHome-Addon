from sqlalchemy import Column, Integer, String, Boolean
from .ModelBase import ModelBase


class WifiNetwork(ModelBase):
    __tablename__ = 'wifi-networks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_default = Column(Boolean, default=False)
    ssid = Column(String)
    password = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "ssid": self.ssid,
            "password": self.password,
            "is_default": self.is_default
        }

    def to_config(self):
        return {
            "wifi": {
                "ssid": self.ssid,
                "password": self.password
            }
        }


class FTPServer(ModelBase):
    __tablename__ = 'ftp-servers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_default = Column(Boolean, default=False)
    host_address = Column(String)
    username = Column(String)
    password = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "host_address": self.host_address,
            "username": self.username,
            "password": self.password,
            "is_default": self.is_default

        }

    def to_config(self):
        return {
            "ftp": {
                "host_address": self.host_address,
                "username": self.username,
                "password": self.password,
            }
        }


class MQTTBroker(ModelBase):
    __tablename__ = 'mqtt-brokers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_default = Column(Boolean, default=False)
    host_address = Column(String, nullable=False)
    port = Column(Integer, default=1883)
    username = Column(String, default=None)
    password = Column(String, default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "host_address": self.host_address,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "is_default": self.is_default

        }

    def to_config(self):
        return {
            "mqtt": {
                "host_address": self.host_address,
                "port": self.port,
                "username": self.username,
                "password": self.password,
            }
        }
