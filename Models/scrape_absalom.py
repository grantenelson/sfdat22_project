# Scrape text of Absalom Absalom! 

import requests
from bs4 import BeautifulSoup

url_stub = 'http://reading-everyday.com/235/Absalom,%20Absalom!%20-%20William%20Faulkner_split_00'

string_list = []

for i in range(1,10):
	url = url_stub + str(i) + '.htm'
	r = requests.get(url)
	b = BeautifulSoup(r.text)
	for span in b.findAll('span', attrs = {'class':'calibre2'}):
		string_list.append(span.text)

txt = ''.join(string_list)
