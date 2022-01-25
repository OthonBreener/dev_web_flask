from os import getenv
from flask import render_template
from flask_migrate import Migrate
from main import create_app, database
from main.regras_de_negocio.usuarios.models import Usuario

app = create_app(getenv('FLASK_CONFIG'))
migrate = Migrate(app, database)


@app.route('/')
def home_page():
    return {'message':'ok'}


@app.shell_context_processor
def make_shell_context():
    return dict(db=database, Usuario=Usuario)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500