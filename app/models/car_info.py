import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class CarInfo(Base):
    __tablename__ = "car_info"

    id = Column(Integer, primary_key=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    spec_name = Column(String)
    type = Column(String, index=True)
    body_type = Column(String, index=True)
    # Research
    reg = Column(String)
    engine = Column(String)
    fuel = Column(String, index=True)
    mileage = Column(Integer)
    drive = Column(String, index=True)
    seats = Column(String, index=True)
    doors = Column(String, index=True)
    transmission = Column(String, index=True)
    color = Column(String, index=True)
    reg_number = Column(String)
    vin = Column(String)
    price = Column(Integer)
    bargain_price = Column(Integer)
    export_price = Column(Integer)
    vat = Column(Integer, index=True)
    link = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)