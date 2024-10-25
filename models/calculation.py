
from sqlalchemy import Column, Integer, Float, String

from database.connection import Base


class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    result = Column(Float)
