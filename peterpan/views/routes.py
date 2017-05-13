from flask import Blueprint, render_template
from bs4 import BeautifulSoup
import requests

mod = Blueprint('main', __name__)

links = ['http://g1.globo.com/','http://www.google.com/']
labels = ['G1', 'Google']

def isUrlValid(url):
	return (not url is None)

def isUrlIncomplete(url):
	return not url.startswith("http://")

@mod.route('/')
def index():

	pages = requests.get('http://g1.globo.com/')

	if pages.status_code == 200:
		soup = BeautifulSoup(pages.content, 'html.parser')
		a_link = soup.find_all('a')

		for link in a_link:
			url = link.get('href')
			if isUrlValid(url):
				if isUrlIncomplete(url):
					url = 'http://g1.globo.com' + url
				links.append(url)
				labels.append(url)

		content = zip(labels, links)
		return render_template('links_list.html', content=content)
	else:
		return render_template('404.html')