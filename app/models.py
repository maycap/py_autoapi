# coding: utf-8
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, unique=True, nullable=False)
    user = Column(String(64), nullable=False)
    content = Column(String(100))
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now)


some_enginne = create_engine('sqlite:///foo.db')
session_factory = sessionmaker(bind=some_enginne)
Session = scoped_session(session_factory)

if __name__ == '__main__':
    Base.metadata.create_all(some_enginne)