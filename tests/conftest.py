import time
import requests
from pytest import fail
from sqlite3 import OperationalError
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from contexto_de_negocio.alocacoes.config import get_postgres_uri, get_api_url
from contexto_de_negocio.alocacoes.adaptadores.orm import start_mappers, metadata

@fixture
def in_memory_db():
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    return engine

@fixture
def session(in_memory_db):

    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


def esperar_o_postegres_aparecer(engine):

    tempo_final = time.time() + 10

    while time.time() < tempo_final:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    
    fail('Postegres não apareceu!')


def esperar_a_aplicacao_subir():

    tempo_final = time.time() + 10
    url = get_api_url()

    while time.time() < tempo_final:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    fail("Api não apareceu!")


