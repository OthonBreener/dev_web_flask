from typing import Tuple
from datetime import datetime
from contexto_de_negocio.alocacoes.dominio.models import ForaDeEstoque, LoteMercadoriaDisponivel, Pedido, alocar_pedido
from pytest import mark, raises


def montando_lote_disponivel_e_pedido(
    identificador: str, 
    quantidade_disponivel: int,
    quantidade_pedido: int
    ) -> Tuple[LoteMercadoriaDisponivel, Pedido]:

    lote_disponivel = LoteMercadoriaDisponivel(
        'smartphone-001',
        identificador,
        quantidade_disponivel,
        date=None
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
        date=None
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


def test_preferencia_por_lotes_atuais_para_alocar_pedido():

    lote_disponivel = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        date=None
    )

    lote_para_amanha = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        '18/01/2022'
    )

    pedido = Pedido('ref1', 'samsung A2', 2)

    alocar_pedido(pedido, [lote_disponivel, lote_para_amanha])

    assert lote_disponivel.quantidade_disponivel == 28
    assert lote_para_amanha.quantidade_disponivel == 30


def test_preferencia_por_lote_disponivel_de_imediato():

    rapido = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        date='17/01/2022'
    )

    medio = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        '21/01/2022'
    )

    longo = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        '11/02/2022'
    )

    pedido = Pedido('ref1', 'samsung A2', 2)

    alocar_pedido(pedido, [rapido, medio, longo])

    assert rapido.quantidade_disponivel == 28
    assert medio.quantidade_disponivel == 30
    assert longo.quantidade_disponivel == 30


def test_retorna_o_lote_no_qual_o_pedido_foi_alocado():

    rapido = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        date=None
    )

    medio = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        '21/01/2022'
    )

    pedido = Pedido('ref1', 'samsung A2', 2)

    alocacao = alocar_pedido(pedido, [rapido, medio])

    assert alocacao == rapido.referencia


def test_levanta_excessao_fora_de_estoque_se_nao_poder_alocar_pedido():

    lote = LoteMercadoriaDisponivel(
        'smartphone-001',
        'samsung A2',
        30,
        date=None
    )

    alocar_pedido(Pedido('ref1', 'samsung A2', 30), [lote])

    with raises(ForaDeEstoque, match='samsung A2'):
        alocar_pedido(Pedido('ref2', 'samsung A2', 1), [lote])
