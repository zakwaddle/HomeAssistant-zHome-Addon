from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase


class DeviceSensor(ModelBase):
    __tablename__ = 'device-sensors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_type = Column(String)
    name = Column(String)
    sensor_config = Column(JSON)
    device_config_id = Column(String, ForeignKey('device-configs.id'))

    device_config = relationship("DeviceConfig", back_populates="sensors")  # one-to-many relationship

    def __repr__(self):
        return f"<DeviceSensor - {self.id} | {self.sensor_type}>"

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_type": self.sensor_type,
            "name": self.name,
            "device_config_id": self.device_config_id,
            "sensor_config": self.sensor_config,
        }
