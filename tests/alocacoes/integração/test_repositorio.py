from pytest import mark
from datetime import datetime
from contexto_de_negocio.alocacoes.dominio.models import LoteMercadoriaDisponivel
from contexto_de_negocio.alocacoes.adaptadores.repositorio import RepositorioSqlAlchemy, RepositorioFake


def test_repositorio_pode_salvar_um_lote_de_mercadorias(session):

    lote_disponivel = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung',
        20,
        date=None
    )

    repo = RepositorioSqlAlchemy(session)
    repo.add(lote_disponivel)
    session.commit()

    lote_salvo = session.execute(
        'SELECT referencia, identificador, _quantidade_disponivel, date FROM "lotes"'
    )

    assert list(lote_salvo) == [
        ('smartphone-001', 'samsung-A2', 30, datetime(2022, 1, 17))
        ]
    

