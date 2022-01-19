from pytest import mark
from uuid import uuid4
from requests import post
from contexto_de_negocio.alocacoes.config import get_api_url


def sufixo_aleatorio() -> str:
    return uuid4().hex[:6]


def referencia_de_lote_aleatoria(name="") -> str:
    return f'referencia-{name}-{sufixo_aleatorio()}'


def identificador_aleatorio(name="") -> str:
    return f'identificador-{name}-{sufixo_aleatorio()}'


def id_de_pedido_aleatorio(name="") -> str:
    return f'pedido-{name}-{sufixo_aleatorio()}'


def test_api_retorna_alocacao(add_estoque):

    identificador1, identificador2 = identificador_aleatorio(), identificador_aleatorio('outro')

    lote1 = referencia_de_lote_aleatoria(1)
    lote2 = referencia_de_lote_aleatoria(2)
    lote3 = referencia_de_lote_aleatoria(3)

    add_estoque(
        [
            (lote1, identificador1, 100, '22/01/2022'),
            (lote2, identificador1, 100, '30/01/2022'),
            (lote3, identificador2, 100, None)
        ]
    )
    id_pedido = id_de_pedido_aleatorio()

    pedido = {'id_pedido': id_pedido, 'identificador':identificador1(), 'quantidade':3}
    url = get_api_url()

    r = post(f'{url}/alocacoes', json=pedido)

    assert r.status_code == 201
    assert r.json()['referencia'] == lote1

@mark.task
def test_end_point_de_alocacoes_retorna_200():

    identificador1 = identificador_aleatorio()
    id_pedido = id_de_pedido_aleatorio()

    pedido = {'id_pedido': id_pedido, 'identificador': identificador1, 'quantidade': 3}

    url = get_api_url()
    post(f'{url}/alocacoes', json=pedido)
