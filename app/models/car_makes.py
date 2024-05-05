from sqlalchemy import Column, Integer, String

from app.database import Base


class CarMake(Base):
    """
    Car makes model, model for mapping vehicle make related on value from ./makes.py.
    """
    __tablename__ = "car_makes"

    id = Column(Integer, primary_key=True)
    make_name = Column(String, index=True)
    code = Column(String, unique=True, index=True)