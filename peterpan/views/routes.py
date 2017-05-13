from flask import Blueprint, render_template
from bs4 import BeautifulSoup
import requests

mod = Blueprint('main', __name__)

links = ['http://g1.globo.com/','http://www.google.com/']
labels = ['G1', 'Google']

def isUrlValid(url):
	return (not url is None) and url.startswith('https://')

@mod.route('/')
def index():

	pages = requests.get('http://g1.globo.com/')
	soup = BeautifulSoup(pages.content, 'html.parser')
	a_link = soup.find_all('a')
	
	for link in a_link:
		url = link.get('href')
		if isUrlValid(url):
			links.append(url)
			labels.append(url)

	content = zip(labels, links)
	return render_template('links_list.html', content=content)
