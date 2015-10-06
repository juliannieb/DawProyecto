import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class WebPage(Base):
    __tablename__ = 'web pages'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False)
    text = Column(Text())
 
class Category(Base):
    __tablename__ = 'categories'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True, unique=True)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///features.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)