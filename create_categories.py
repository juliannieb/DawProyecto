from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from build_db import Category, Base
 
engine = create_engine('sqlite:///features.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
# Insert a Person in the person table
categories = ['Sports', 'Entertainment', 'Tech', 'Business', 'Lifestyle', 'Shopping', 'Education']

for category in categories:
	new_category = Category(name=category)
	session.add(new_category)
	session.commit()
 
