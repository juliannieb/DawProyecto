from readability.readability import Document
from bs4 import BeautifulSoup as BS
import urllib
import re
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from build_db import Category, Base, WebPage
 
engine = create_engine('sqlite:///features.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def striphtml(data):
    p = re.compile(r'<[^>]*>')
    txt = p.sub('', data)
    return ' '.join(txt.split())

def num_apperances_of_tag(tag_name, html):
    soup = BS(html, "lxml")
    return len(soup.find_all(tag_name))


# url = "http://apps.topcoder.com/forums/?module=Thread&threadID=670169&start=0&mc=5"
# html = urllib.urlopen(url).read()
# # print(html)
# # print num_apperances_of_tag('div', html)

# readable_article = Document(html).summary()

# readable_title = Document(html).short_title()
# # print readable_title
# print striphtml(readable_article)

categories_query = session.query(Category).all()
categories = [c.name for c in categories_query]

def create_csv():
	with open('classification.tsv','rb') as tsvin, open('new.csv', 'wb') as csvout:
	    tsvin = csv.reader(tsvin, delimiter='\t')
	    csvout = csv.writer(csvout, delimiter=',')
	    for row in tsvin:
	    	for cat in categories:
	    		if cat.lower() in row[0].lower() or cat in row[1].lower():
	    			csvout.writerow([cat, row[2], row[3]])

        # count = int(row[4])
        # if count > 0:
        #     csvout.writerows([row[2:4] for _ in xrange(count)])