from sqlalchemy import Column, Integer, String


class CarMakes():
    __tablename__ = "car_makes"

    make_name = Column(String, index=True)
    code = Column(String, unique=True, index=True)