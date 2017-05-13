from peterpan import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
#
# from flask import Flask, Blueprint, render_template
# app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     return render_template('home.html')
#
# if __name__ == '__main__':
#     app.run()
