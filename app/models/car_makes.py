from sqlalchemy import Column, Integer, String

from app.database import Base


class CarMakes(Base):
    __tablename__ = "car_makes"

    id = Column(Integer, primary_key=True)
    make_name = Column(String, index=True)
    code = Column(String, unique=True, index=True)