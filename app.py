#!/usr/bin/env python3

from os import remove
from os.path import exists
from sqlalchemy import (Binary, Column, DateTime, String, Integer, ForeignKey, 
    create_engine, func)
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    hash = Column(Binary(32))
    created_at = Column(DateTime, default=func.now())

class Names(Base):
    __tablename__ = "names"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# class UserNames(Base):
#     __tablename__ = "user_names"
#     user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
#     name_id = Column(Integer, ForeignKey("name.id"), primary_key=True)

db_name = "tcenter.db"
if exists(db_name):
    remove(db_name)

engine = create_engine("sqlite:///{}".format(db_name))
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)