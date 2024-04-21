from sqlalchemy import Column, Integer, String

from app.database import Base


class CarTypes(Base):
    __tablename__ = "car_types"

    id = Column(Integer, primary_key=True)
    type_name = Column(String, index=True)
    code = Column(String, unique=True, index=True)