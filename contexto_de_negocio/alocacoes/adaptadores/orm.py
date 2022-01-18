"""
! Inversão de Dependências no banco de dados

O Orm conhece o domínio e não o contrário. A ideia é manter
o modelo de domínio livre de preocupações com infraestrutura,
de forma que se caso necessário trocar o orm, não será preciso
mudar a camada de dominio.
"""


from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String
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