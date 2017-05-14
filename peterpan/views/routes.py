from flask import Blueprint, render_template
from bs4 import BeautifulSoup
import requests

mod = Blueprint('main', __name__)

links = []
titles = []
sources = []
dates = []
imgs = []
descriptions = []

def canConnect(page):
	return page.status_code == 200

def get_title(link):
	title = str(link).split('<a class')
	title = str(title).split('</a>')[0]
	if 'img' in title:
		return ''
	title = title.split('>')[1]
	return title

def isUrlValid(url):
	return not (url is None)

def has_title(link):
	return not ('img' in str(link))	

def isUrlComplete(url):
	return url.startswith("//g1.globo.com/busca")

def add_new(url):
	url = 'http:' + url
	page = requests.get(url)

	if canConnect(page):
		links.append(url)

def append_source(text):
	if not 'busca-portal">' in text:
		return ''
	text = text.split('busca-portal">', 1)[1]
	source, text = text.split('</span>', 1)
	sources.append(source)
	return text

def parse(link):
	url = link.get('href')
	if isUrlValid(url) and has_title(link):
		if isUrlComplete(url):
			add_new(url)
			titles.append(get_title(link))

def get_template(pages):
		soup = BeautifulSoup(pages.content, 'html.parser')
		a_link = soup.find_all('a')

		for link in a_link:
			parse(link)

		text = soup.prettify()
		while(text != ''):
			text = append_source(text)

		content = zip(titles, links)
		return render_template('links_list.html', content=content)

@mod.route('/')
def index():
	search_term = 'enem'
	pages = requests.get('http://g1.globo.com/busca/?q=' + search_term)

	if canConnect(pages):
		return get_template(pages)
	else:
		return render_template('404.html')
