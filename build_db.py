# -*- coding: utf_8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
 
Base = declarative_base()
 
class WebPage(Base):
    __tablename__ = 'web_pages'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    url = Column(String(250), nullable=False, unique=True)
    text = Column(UnicodeText(convert_unicode=True))
    num_divs = Column(Integer, nullable=False)
    num_titles = Column(Integer, nullable=False)
    num_refs = Column(Integer, nullable=True)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", backref=backref('web_pages', order_by=id))
 
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True, unique=True)
    def __str__(self):
        return self.name


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///features.db', encoding='utf8', convert_unicode=True)
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)