from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String

# ! O Orm conhece o domínio e não o contrário ( Inversão de dependências )
from contexto_de_negocio.alocacoes.dominio.models import Pedido

metadata = MetaData()

pedidos = Table(
    'pedidos',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_pedido', String(255)),
    Column('identificador', String(255)),
    Column('quantidade', Integer, nullable=False)
)


def start_mappers():
    mapenado_pedidos = mapper(Pedido, pedidos)