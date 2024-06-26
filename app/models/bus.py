from sqlalchemy import Column, Integer, String, Float

from app.db.base_class import Base


class Bus(Base):
    id = Column(Integer, primary_key=True)
    bus_id = Column(String, unique=True)
    lat = Column(Float)
    lon = Column(Float)
    time = Column(String)
    last_stop_index = Column(Integer)