#  sqlite3 test_db.db    for compile


import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float,DateTime,ForeignKey, Date, Time, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__="users"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    college = Column(String)
    roll = Column(Integer,unique=True)
    year = Column(Integer)
    course = Column(String)

class Attendance(Base):
    __tablename__="attendance"
    id=Column(Integer,primary_key=True)
    date =  Column(Date,default=func.date(func.now()))
    time =  Column(Time,default=func.time(func.now()))
    roll =  Column(Integer,ForeignKey('users.roll'))
    
    

if __name__ == "__main__":
    engine = create_engine('sqlite:///attendance_db.sqlite3')
    Base.metadata.create_all(engine)
