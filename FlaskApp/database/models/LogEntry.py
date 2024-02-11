from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase
import datetime



class LogEntry(ModelBase):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String)
    log = Column(JSON)
    time = Column(DateTime, default=datetime.datetime.now)
    device_id = Column(String, ForeignKey('home-devices.id'))

    device = relationship("HomeDevice", back_populates="log_entries")

    def __repr__(self):
        message = self.log.get('message')
        unit_id = self.log.get('unit_id')
        return f"<LogEntry - {unit_id} | {self.time} |{message}>"

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "log": self.log,
            "time": self.time.strftime("%Y|%m|%d %H:%M:%S")
        }



