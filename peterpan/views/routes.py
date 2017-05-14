from flask import Blueprint, render_template, redirect
from bs4 import BeautifulSoup
import requests

mod = Blueprint('main', __name__)

links = []
labels = []

def isUrlValid(url):
	return not (url is None)

def isUrlComplete(url):
	return url.startswith("//g1.globo.com/busca")

def canConnect(page):
	return page.status_code == 200

def add_new(url):
	url = 'http:' + url
	page = requests.get(url)

	if canConnect(page):
		#soup = BeautifulSoup(page.content, 'html.parser')
		links.append(url)
		labels.append(url)

@mod.route('/')
def index():
	termo_busca = 'enem'
	pages = requests.get('http://g1.globo.com/busca/?q=' + termo_busca)

	if canConnect(pages):
		soup = BeautifulSoup(pages.content, 'html.parser')
		a_link = soup.find_all('a')

		html_content = ''
		for link in a_link:
			url = link.get('href')
			if isUrlValid(url):
				if isUrlComplete(url):
					add_new(url)

		content = zip(labels, links)
		return render_template('links_list.html', content=content)
	else:
		return render_template('404.html')
