from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CarInfo(Base):
    __tablename__ = "car_info"

    make: Mapped[str] = mapped_column(String, index=True)
    model: Mapped[str] = mapped_column(String, index=True)
    spec_name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String, index=True)
    body_type: Mapped[str] = mapped_column(String, index=True)
    reg: Mapped[str] = mapped_column(String)
    engine: Mapped[str] = mapped_column(String)
    fuel: Mapped[str] = mapped_column(String, index=True)
    mileage: Mapped[int] = mapped_column(Integer)
    drive: Mapped[str] = mapped_column(String, index=True)
    seats: Mapped[str] = mapped_column(String, index=True)
    doors: Mapped[str] = mapped_column(String, index=True)
    transmission: Mapped[str] = mapped_column(String, index=True)
    color: Mapped[str] = mapped_column(String, index=True)
    reg_number: Mapped[str] = mapped_column(String)
    vin: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    bargain_price: Mapped[int] = mapped_column(Integer)
    export_price: Mapped[int] = mapped_column(Integer)
    vat: Mapped[int] = mapped_column(Integer, index=True)
    link: Mapped[str] = mapped_column(String)
