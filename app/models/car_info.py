import datetime

from sqlalchemy import Column, DateTime, Integer, String


class CarInfo():
    __tablename__ = "car_info"

    make = Column(String, index=True, nullable=True)
    model = Column(String, index=True, nullable=True)
    spec_name = Column(String, nullable=True)
    type = Column(String, index=True, nullable=True)
    body_type = Column(String, index=True, nullable=True)
    # Research
    reg = Column(DateTime, unique=True, nullable=True)
    engine = Column(String, nullable=True)
    fuel = Column(String, index=True, nullable=True)
    mileage = Column(Integer, nullable=True)
    drive = Column(String, index=True, nullable=True)
    seats = Column(String, index=True, nullable=True)
    doors = Column(String, index=True, nullable=True)
    transmission = Column(String, index=True, nullable=True)
    color = Column(String, index=True, nullable=True)
    reg_number = Column(String, unique=True, nullable=True)
    vin = Column(String, unique=True, nullable=True)
    price = Column(Integer, nullable=True)
    bargain_price = Column(Integer, nullable=True)
    export_price = Column(Integer, nullable=True)
    vat = Column(Integer, index=True, nullable=True)
    link = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.date.today().strftime('%Y-%m-%d'))