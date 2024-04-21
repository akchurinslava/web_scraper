from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Settings

Base = declarative_base()
engine = create_engine(Settings().database_url)

Session = sessionmaker(bind=engine)
session = Session()