from readability.readability import Document
from bs4 import BeautifulSoup as BS
import urllib
import re

def striphtml(data):
    p = re.compile(r'<[^>]*>')
    return p.sub('', data)

def num_apperances_of_tag(tag_name, html):
    soup = BS(html, "lxml")
    return len(soup.find_all(tag_name))


url = "http://apps.topcoder.com/forums/?module=Thread&threadID=670169&start=0&mc=5"
html = urllib.urlopen(url).read()

print num_apperances_of_tag('div', html)

# readable_article = Document(html).summary()

# readable_title = Document(html).short_title()
# print readable_title
# print striphtml(readable_article)