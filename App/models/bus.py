from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship


from App.db.base_class import Base

class Bus(Base):

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)