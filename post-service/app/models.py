from app.db import Base
from sqlalchemy import Column, Integer, String


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    userId = Column(Integer)


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     userId = Column(Integer, ForeignKey("users.id"), nullable=False)
#     title = Column(String)
#     body = Column(String)
