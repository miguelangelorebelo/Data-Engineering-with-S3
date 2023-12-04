from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from .database import Base


class VehicleModel(Base):
    __tablename__ = "on_vehicle"
    __table_args__ = ({"mysql_engine": "Aria"},)

    instance_id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    process_date = Column(DateTime, default=(datetime.utcnow()))
    event = Column(String(64), unique=False, nullable=False, index=True)
    at = Column(DateTime, unique=False, nullable=False)
    # on = Column(String, unique=False, nullable=True)
    id = Column(String(64), unique=False, nullable=False)
    lat = Column(Float, unique=False, nullable=True)  # register, deregister
    lng = Column(Float, unique=False, nullable=True)  # register, deregister
    organization_id = Column(String(32), unique=False, nullable=False)


class OperatingPeriodModel(Base):
    __tablename__ = "on_operating_period"
    __table_args__ = ({"mysql_engine": "Aria"},)

    instance_id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    process_date = Column(DateTime, default=(datetime.utcnow()))
    event = Column(String(32), unique=False, nullable=False)
    at = Column(DateTime, unique=False, nullable=False)
    # on = Column(String, unique=False, nullable=True)
    id = Column(String(32), unique=False, nullable=False)
    start = Column(DateTime, unique=False, nullable=False)
    finish = Column(DateTime, unique=False, nullable=False)
    organization_id = Column(String(32), unique=False, nullable=False)
