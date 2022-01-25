from flask import Flask
import flask
from pytest import fixture
from main import create_app

@fixture
def test_client():

    flask_app = Flask(__name__)
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_fake.db'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as client:
        yield client