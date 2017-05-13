from flask import Blueprint, render_template

mod = Blueprint('main', __name__)

links = ['http://g1.globo.com/','http://www.google.com/']
label = ['G1', 'Google']

@mod.route('/')
def index():
	content = zip(label, links)
	return render_template('links_list.html', content=content)
