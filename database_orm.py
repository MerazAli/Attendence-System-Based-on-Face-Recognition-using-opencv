#  sqlite3 test_db.db    for compile


import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float,DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    college = Column(String)
    roll = Column(Integer)
    year = Column(Integer)
    course = Column(String)

class Attendance(Base):
    __tablename__="attendance"
    id=Column(Integer,primary_key=True)
    date =  Column(DateTime,default=datetime.date)
    time =  Column(DateTime,default=datetime.time)
    userid = Column(Integer,ForeignKey('users.id'))
    

if __name__ == "__main__":
    engine = create_engine('sqlite:///db.sqlite3')
    Base.metadata.create_all(engine)
