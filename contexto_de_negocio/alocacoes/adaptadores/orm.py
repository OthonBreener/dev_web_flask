"""
! Inversão de Dependências no banco de dados

O Orm conhece o domínio e não o contrário. A ideia é manter
o modelo de domínio livre de preocupações com infraestrutura,
de forma que se caso necessário trocar o orm, não será preciso
mudar a camada de dominio.
"""


from sqlalchemy.orm import mapper, relationship
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey
from contexto_de_negocio.alocacoes.dominio.models import Pedido, LoteMercadoriaDisponivel

metadata = MetaData()

pedidos = Table(
    'pedidos',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('id_pedido', String(255)),
    Column('identificador', String(255)),
    Column('quantidade', Integer, nullable=False)
)


lotes = Table(
    'lotes',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('referencia', String(255)),
    Column('identificador', String(255)),
    Column('_quantidade_disponivel', Integer, nullable=False),
    Column('data', Date, nullable=True)
)


alocacoes = Table(
    'alocacoes',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('pedido_id', ForeignKey('pedidos.id')),
    Column('lote_id', ForeignKey('lotes.id'))
)


def start_mappers():
    mapeando_pedidos = mapper(Pedido, pedidos)
    mapper(
        LoteMercadoriaDisponivel, lotes,
        properties = {
            '_alocacoes': relationship(
                mapeando_pedidos, secondary=alocacoes, collection_class=set
            )
        }
    )