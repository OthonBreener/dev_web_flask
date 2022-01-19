from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass(unsafe_hash=True)
class Pedido:
    """
    A classe Pedido é um objeto de valor: Objeto de valor é
    qualquer objeto de domínio identificado exclusivamente
    pelos dados que contém. 

    ! Dois pedidos com os mesmos atributos são iguais

    * fronzen=True implementa: __setattr__ e __delattr__
    * Para alterar o id: setattr(Pedido, 'id', 'Novo_id')
    """
    id_pedido: str 
    identificador: str
    quantidade: int


@dataclass(eq=True)
class LoteMercadoriaDisponivel:
    """
    A classe LoteMercadoriaDisponivel é uma entidade, diferente de Pedido
    o lote de mercadoria pode mudar. Dizemos que uma entidade possui
    igualdade de identidade, ou seja, podemos mudar seus valores que
    eles ainda são reconhecidos como a mesma coisa.

    * Tornamos explicito que se trata de uma entidade implementando os métodos
    * mágicos __eq__ e __hash__
    """

    def __init__(self, referencia: str, identificador: str, quantidade: int, date: Optional[str] ) -> None:

        self.referencia = referencia
        self.identificador = identificador
        self.date = self.string_para_data(date)
        self._quantidade_disponivel = quantidade
        self._alocacoes = set() # type: Set[Pedido]


    def __hash__(self):
        return hash(self.referencia)


    def __gt__(self, other):
        """
        Esse método foi implementado para comparar
        dois lotes pela data. 
        """

        if self.date is None:
            return False 

        if other.date is None:
            return True 

        return self.date > other.date


    def alocar_pedido(self, pedido: Pedido) -> None:

        if self.pode_alocar(pedido):
            self._alocacoes.add(pedido)
    

    def dealocar_pedido(self, pedido: Pedido):
        
        if pedido in self._alocacoes:
            self._alocacoes.remove(pedido)


    def pode_alocar(self, pedido: Pedido) -> bool:

        return (self.identificador == pedido.identificador
            and self.quantidade_disponivel >= pedido.quantidade)
    

    @property
    def quantidade_alocada(self) -> int:
        return sum(pedido.quantidade for pedido in self._alocacoes)
    

    @property
    def quantidade_disponivel(self) -> int:
        return self._quantidade_disponivel - self.quantidade_alocada

    
    def string_para_data(self, date: str) -> datetime:

        if date is None:
            return datetime.now()

        return datetime.strptime(date, '%d/%m/%Y')


class ForaDeEstoque(Exception):
    pass


def alocar_pedido(pedido: Pedido, lotes: List[LoteMercadoriaDisponivel]) -> str:
    """
    Esta função recebe uma lista de lotes com diferentes datas e aloca o pedido 
    para o lote que tem a menor data.
    """

    try: 
        lote = next(lote for lote in sorted(lotes) if lote.pode_alocar(pedido))
        lote.alocar_pedido(pedido)
        return lote.referencia
    
    except StopIteration:
        raise ForaDeEstoque(f'Fora de estoque para o identificador {pedido.identificador}')
