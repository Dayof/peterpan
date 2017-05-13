from flask import Flask, Blueprint, render_template

mod = Blueprint('main', __name__)

@mod.route('/')
def index():
    return render_template('home.html')
