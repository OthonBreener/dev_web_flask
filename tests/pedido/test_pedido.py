from datetime import datetime
from aplicacao.pedido.models import LoteMercadoriaDisponivel, Pedido 
from typing import Tuple

def montando_lote_disponivel_e_pedido(
    identificador: str, 
    quantidade_disponivel: int,
    quantidade_pedido: int
    ) -> Tuple[LoteMercadoriaDisponivel, Pedido]:

    lote_disponivel = LoteMercadoriaDisponivel(
        'smartphone-001',
        identificador,
        quantidade_disponivel,
        datetime.utcnow()
    )
    pedido = Pedido('ref1', identificador, quantidade_pedido)

    return lote_disponivel, pedido


def test_alocando_pedido_reduz_a_quantidade_disponivel():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido('samsung A2', 20, 2)
    lote_disponivel.alocar_pedido(pedido)


    assert lote_disponivel.quantidade_disponivel == 18


def test_pode_alogar_se_a_quantidade_disponivel_for_maior_que_a_quantidade_pedida():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido(
        'samsung A2', 20, 2)
    
    assert lote_disponivel.pode_alocar(pedido)


def test_nao_pode_alogar_se_a_quantidade_disponivel_for_menor_que_a_quantidade_pedida():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido(
        'samsung A2', 2, 20)

    assert lote_disponivel.pode_alocar(pedido) is False


def test_pode_alogar_se_a_quantidade_disponivel_for_igual_a_quantidade_pedida():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido(
        'samsung A2', 2, 2)

    assert lote_disponivel.pode_alocar(pedido)


def test_nao_pode_alocar_se_o_identificador_nao_for_igual():

    lote_disponivel = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung',
        20,
        datetime.utcnow()
    )
    pedido = Pedido('ref1', 'motorola', 2)

    assert lote_disponivel.pode_alocar(pedido) is False


def test_pode_dealocar_pedidos_alocados():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido(
        'samsung A2', 20, 2)

    lote_disponivel.dealocar_pedido(pedido)

    assert lote_disponivel.quantidade_disponivel == 20


def test_alocacoes_e_idempotente():

    lote_disponivel, pedido = montando_lote_disponivel_e_pedido(
        'samsung A2', 20, 2)

    lote_disponivel.alocar_pedido(pedido)
    lote_disponivel.alocar_pedido(pedido)

    assert lote_disponivel.quantidade_disponivel == 18