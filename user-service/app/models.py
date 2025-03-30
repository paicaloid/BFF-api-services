from app.db import Base
from sqlalchemy import Column, Integer, String


# Define a sample table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
