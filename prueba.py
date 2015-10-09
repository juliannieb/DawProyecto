from readability.readability import Document
from bs4 import BeautifulSoup as BS
import urllib
import re
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from build_db import Category, Base, WebPage
 
engine = create_engine('sqlite:///features.db')

def striphtml(data):
    p = re.compile(r'<[^>]*>')
    txt = p.sub('', data)
    return ' '.join(txt.split())

def num_apperances_of_tag(tag_name, html):
    soup = BS(html, "lxml")
    return len(soup.find_all(tag_name))




def open_session():
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session


def create_csv(name_source, name_dest):
	session = open_session()
	categories_query = session.query(Category).all()
	categories = [c.name for c in categories_query]
	with open(name_source,'rb') as tsvin, open(name_dest, 'wb') as csvout:
	    tsvin = csv.reader(tsvin, delimiter='\t')
	    csvout = csv.writer(csvout, delimiter='\t')
	    for row in tsvin:
	    	for cat in categories:
	    		if cat.lower() in row[0].lower() or cat in row[1].lower():
	    			csvout.writerow([cat, row[2], row[3]])
	    			break



url = "http://apps.topcoder.com/forums/?module=Thread&threadID=670169&start=0&mc=5"
html = urllib.urlopen(url).read()
# print(html)
# print num_apperances_of_tag('div', html)

readable_article = Document(html).summary()

readable_title = Document(html).short_title()
print readable_title
print len(striphtml(readable_article))
print num_apperances_of_tag('a', html)


def create_page(row, category):
	link = row[2]
	html = urllib.urlopen(link).read()
	readable_article = Document(html).summary()
	txt = striphtml(readable_article)
	print txt
	num_divs = num_apperances_of_tag('div', html)
	num_refs = num_apperances_of_tag('a', html)
	num_titles = num_apperances_of_tag('title', html)
	title = row[1]
	web_page = WebPage(title=title, url=link, text=txt, 
				num_divs=num_divs, num_titles=num_titles, num_refs=num_refs,
				cat_id=category)
	return web_page
	


def crawl(name_source):
	cont = 0
	tags = ['title', 'div', 'a']
	session = open_session()
	with open(name_source) as csvin:
		csvin = csv.reader(csvin, delimiter='\t')
		for row in csvin:
			cat = session.query(Category).name = row[0]
			web_page = create_page(row, cat)
			session.add(web_page)
			session.commit()
			if cont%50 == 0:
				print cont
			cont += 1
			

# crawl('new.csv')
crawl('new.csv')
# create_csv('classification.tsv', 'new.csv')