from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from . import config

database = SQLAlchemy()
bootsprap = Bootstrap()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config.config[config_name])
    config.config[config_name].init_app(app)

    database.init_app(app)
    bootsprap.init_app(app)

    from main.regras_de_negocio.usuarios import routes

    routes.configure(app)


    return app