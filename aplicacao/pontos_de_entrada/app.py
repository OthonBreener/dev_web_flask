from crypt import methods
from os import getenv
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contexto_de_negocio.alocacoes.config import get_postgres_uri
from contexto_de_negocio.alocacoes.dominio.models import ForaDeEstoque, Pedido
from contexto_de_negocio.alocacoes.adaptadores.orm import start_mappers
from contexto_de_negocio.alocacoes.adaptadores.repositorio import (
    RepositorioSqlAlchemy)
from contexto_de_negocio.alocacoes.servicos.servicos import IdentificadorInvalido, alocar

start_mappers()
get_session = sessionmaker(bind=create_engine(get_postgres_uri()))
app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')


@app.route('/alocacoes', methods=['POST'])
def end_point_de_alocacoes():

    session = get_session()
    lotes = RepositorioSqlAlchemy(session)
    pedido = Pedido(
        request.json['id_pedido'], 
        request.json['identificador'], 
        request.json['quantidade']
    )

    try:
        referencia_de_lote = alocar(pedido, lotes, session)

    except (ForaDeEstoque, IdentificadorInvalido) as e:
        return {'mensagem': str(e)}, 400
    
    return {'referencia_de_lote': referencia_de_lote}, 201
