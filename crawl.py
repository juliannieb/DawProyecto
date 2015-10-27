# -*- coding: utf_8 -*-
import urllib
from urllib2 import Request, urlopen, URLError, HTTPError

from readability.readability import Document
from bs4 import BeautifulSoup as BS

import re
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from build_db import Category, Base, WebPage
 
engine = create_engine('sqlite:///features.db', encoding='utf8', convert_unicode=True)

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

# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

def create_csv(name_source, name_dest):
    session = open_session()
    categories_query = session.query(Category).all()
    categories = [c.name for c in categories_query]
    with open(name_source,'rb') as tsvin, open(name_dest, 'wb') as csvout:
        tsvin = csv.reader(tsvin, delimiter='\t')
        csvout = csv.writer(csvout, delimiter='\t')
        for row in tsvin:
            # for cat in categories:
            if 'sport' in row[0].lower() or 'sport' in row[1].lower():
                csvout.writerow(['Sports', row[2], row[3]])
            

def create_page(req, row, category, encoding):
    link = row[2]
    readable_article = None
    html = None
    try:
        html = req.read()
        readable_article = Document(html).summary()
    except Exception as e:
        print repr(e)    
    
    if not html:
        return None

    if readable_article:
        txt = striphtml(readable_article)
    else:
        txt = ""

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
    session = open_session()
    with open(name_source) as csvin:
        csvin = csv.reader(csvin, delimiter='\t')
        for row in csvin:
            print cont
            cont += 1
            cat = session.query(Category).name = row[0]
            try:
                query = session.query(WebPage).filter(WebPage.title.in_([row[1]]))
                if query.all():
                    print "Ya existe"
                    continue
            except Exception as e:
                print repr(e)
                continue
            req = None
            try: 
                req = urlopen(row[2], timeout=1)
            except URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                elif hasattr(e, 'code'): # <--
                    print 'The server couldn\'t fulfill the request.'
                    print 'Error code: ', e.code
            except HTTPError as e:
                print e.reason
            except Exception:
                pass
            if req:
                if 'content-type' in req.headers:
                    encoding = req.headers['content-type'].split('charset=')[-1]
                    if encoding == "text/html":
                        encoding = "ascii"
                else:
                    encoding = 'utf8'
                web_page = create_page(req, row, cat, encoding)
                if web_page:
                    try:
                        session.add(web_page)
                        session.commit()
                    except Exception as e:
                        session.rollback()
                        print repr(e)
                        pass

# crawl('new.csv')
crawl('sprt.csv')
# create_csv('classification.tsv', 'sprt.csv')