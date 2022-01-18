from contexto_de_negocio.alocacoes.adaptadores.repositorio import (
    RepositorioSqlAlchemy)
from contexto_de_negocio.alocacoes.dominio.models import Pedido, alocar_pedido


class IdentificadorInvalido(Exception):
    pass


def identificador_valido(identificador, lotes):
    return identificador in {lote.identificador for lote in lotes}


def alocar(pedido: Pedido, repositorio: RepositorioSqlAlchemy, session) -> str:

    lotes = repositorio.list()
    if not identificador_valido(pedido.identificador, lotes):
        raise IdentificadorInvalido(f'Identificado Inválido {pedido.identificador}')
    
    referencia_de_lote = alocar_pedido(pedido, lotes)
    session.commit()
    return referencia_de_lote

