from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from aplicacao.alocacoes.adaptadores.orm import start_mappers, metadata

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