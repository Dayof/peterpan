from flask import Blueprint, render_template, request, make_response
from bs4 import BeautifulSoup
from random import shuffle
import requests

mod = Blueprint('main', __name__)

links = []
titles = []
sources = []
dates = []
imgs = []
descriptions = []

# Stubs
user_info_total = [{'user_id' : None,
                    'locals' : [],
                    'links_tags' : [] },
                    {'user_id' : '123',
                    'locals' : ['unb'],
                    'links_tags' : []},
                    {'user_id' : '123',
                    'locals' : ['unb'],
                    'links_tags' : ['enem']},
                    {'user_id' : '123',
                    'locals' : ['elite', 'supervia'],
                    'links_tags' : ['enem', 'unb']} ]

TEST_CASE = 2

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

    source = source.replace('\n', ' ')
    index = 0
    for i in range(len(source)):
        if source[i] != ' ':
            index = i
            break
    source = source[index:]
    index = 0
    for i in range(1,len(source)):
        if (source[-i]) != ' ':
            index = i
            break
    source = source[:len(source)-index+1]

    sources.append(source)
    return text

def append_link(link):
    url = link.get('href')
    if isUrlValid(url) and has_title(link):
        if isUrlComplete(url):
            add_new(url)
            titles.append(get_title(link))

def append_links_in(soup):
    a_link = soup.find_all('a')
    for link in a_link:
        append_link(link)

def append_date(text):
    if text != '':
        near_text = text[:80]
        date = ''
        if 'busca-tempo-decorrido' in near_text:
            date = near_text.split('>')[1]

        date = date.replace('\n', ' ')
        index = 0
        for i in range(len(date)):
            if date[i] != ' ':
                index = i
                break
        date = date[index:]
        index = 0
        for i in range(1,len(date)):
            if (date[-i]) != ' ':
                index = i
                break
        date = date[:len(date)-index+1]

        dates.append(date)
    return text

all_img = []
def append_img(text):
    if text != '':
        img = ''
        near_text = text[:650]
        if near_text.count('img src') > 0:
            near_text = near_text.split('img src="', 1)[1]
            img = near_text.split('"/>')[0]
            img = img.split('">')[0]
        if '.jpg' in img:
            imgs.append(img)
        else:
            imgs.append('')

def append_desc(text):
    if text != '':
        description = ''
        near_text = text[:1200]
        if near_text.count('<p class="busca-highlight">') > 0:
            description = near_text.split('<p class="busca-highlight">',1)[1]
            description = description.split('<span>',1)[1]
            description = description.split('</span>',1)[0]
            description = description.split('</span',1)[0]
            description = description.replace('<em>', '&')
            description = description.replace('</em>', '&')
            description = ''.join([c for c in description if c!='&'])
        elif near_text.count('navegacional-core-page-description">') > 0:
            description = near_text.split('<p class="widget-navegacional-core-page-description">',1)[1]
            description = description.split('</p>')[0]
        descriptions.append(description)

def append_sources_and_date_and_image_in(soup):
    text = soup.prettify()
    while(text != ''):
        text = append_source(text)
        text = append_date(text)
        append_img(text)
        append_desc(text)

def get_some_from_locals(locals):
    src = requests.get('http://g1.globo.com/busca/?q=' + locals[0])
    soup = BeautifulSoup(src.content, 'html.parser')

    append_links_in(soup)
    append_sources_and_date_and_image_in(soup)

def get_some_from_links_tag(tags):
    src = requests.get('http://g1.globo.com/busca/?q=' + tags[0])
    soup = BeautifulSoup(src.content, 'html.parser')

    append_links_in(soup)
    append_sources_and_date_and_image_in(soup)


def get_template(pages, locals=None, links_tag=None):
    soup = BeautifulSoup(pages.content, 'html.parser')

    append_links_in(soup)
    append_sources_and_date_and_image_in(soup)

    if locals:
        print('adding locals')
        # get soup from local
        get_some_from_locals(locals)

    if links_tag:
        print('adding tags links')
        # get soup from tags
        get_some_from_links_tag(links_tag)

    content = zip(titles, links, sources, dates, imgs, descriptions)

    return content

def empty_lists():
    links.clear()
    titles.clear()
    sources.clear()
    dates.clear()
    imgs.clear()
    descriptions.clear()

@mod.route('/<name>')
def index(name):
    pages = requests.get('http://g1.globo.com/busca/?q=' + name)
    empty_lists()

    if canConnect(pages):
        # user_id = request.cookies.get('user_id')
        user_id = user_info_total[TEST_CASE]['user_id']
        user_info = {}

        if user_id:
            content = get_template(pages,
                                    user_info_total[TEST_CASE]['locals'],
                                    user_info_total[TEST_CASE]['links_tags'])
            # print(list(content))
            # shuffle(list(content))
            content = list(content)
            shuffle(content)
            user_info['message'] = None
            return render_template('links_list.html', content=content, user_info=user_info)
        else:
            content = get_template(pages)
            user_info['message'] = 'Bem vindo'
            resp = make_response(render_template('links_list.html', content=content, user_info=user_info))
            resp.set_cookie('user_id', '123')

            return resp
    else:
        return render_template('404.html')
