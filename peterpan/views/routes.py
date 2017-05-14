from flask import Blueprint, render_template, request, make_response
from bs4 import BeautifulSoup
import requests

mod = Blueprint('main', __name__)

links = []
labels = []

title = []
source = []
date = []
img = []
description = []

def isUrlValid(url):
	return not (url is None)

def isUrlComplete(url):
	return url.startswith("//g1.globo.com/busca")

def canConnect(page):
	return page.status_code == 200

def getTitle(link):
	title = str(link).split('<a class')
	title = str(title).split('</a>')[0]
	if 'img' in title:
		return ''
	title = title.split('>')[1]
	return title

def hasTitle(link):
	return not ('img' in str(link))

def parse(link):
	url = link.get('href')
	if isUrlValid(url) and hasTitle(link):
		if isUrlComplete(url):
			add_new(url)
			title.append(getTitle(link))

def add_new(url):
	url = 'http:' + url
	page = requests.get(url)

	if canConnect(page):
		links.append(url)
		labels.append(url)

@mod.route('/')
def index():
	search_term = 'enem'
	pages = requests.get('http://g1.globo.com/busca/?q=' + search_term)

	if canConnect(pages):
		soup = BeautifulSoup(pages.content, 'html.parser')
		a_link = soup.find_all('a')

		html_content = ''
		for link in a_link:
			parse(link)

		content = zip(title, links)

		user_id = request.cookies.get('user_id')
		if user_id:
			print(user_id, 'user with id')
			return render_template('links_list.html', content=content)
		else:
			resp = make_response(render_template('links_list.html', content=content))
			resp.set_cookie('user_id', '123')
			return resp
	else:
		return render_template('404.html')
