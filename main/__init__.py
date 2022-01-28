from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import config

database = SQLAlchemy()
bootsprap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'user.login'

def create_app(config_name):

    app = Flask(__name__, static_folder='static')
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    database.init_app(app)
    bootsprap.init_app(app)
    login_manager.init_app(app)

    from main.regras_de_negocio.usuarios.pontos_de_entrada import routes

    routes.configure(app)


    return app