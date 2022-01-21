from os import getenv, path
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = path.abspath(path.dirname(__file__))


database = SQLAlchemy()
bootsprap = Bootstrap()
migrate = Migrate(database)

def create_app():

    app = Flask(__name__)
    database.init_app(app)
    bootsprap.init_app(app)
    migrate.init_app(app)

    from main.regras_de_negocio.usuarios import routes

    routes.configure(app)

    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        path.join(basedir, 'data.sqlite')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    #@app.shell_context_processor
    #def make_shell_context():
    #    return dict(db=database, Usuario=Usuario)
   
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

    return app