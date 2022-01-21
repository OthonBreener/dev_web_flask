from pytest import fixture
from main import create_app

@fixture
def test_client():

    flask_app = create_app('testing')
    #from main.app import app as flask_app
    with flask_app.test_client() as testing_client:
        yield testing_client
