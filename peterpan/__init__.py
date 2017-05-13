from flask import Flask, render_template
from .views import routes

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

app.register_blueprint(routes.mod)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
