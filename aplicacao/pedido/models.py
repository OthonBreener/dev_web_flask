from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class Pedido:
    id: str 
    identificador: str
    quantidade: int


class LoteMercadoriaDisponivel:
    
    def __init__(self, referencia: str, identificador: str, quantidade: int, date: Optional[datetime] ) -> None:
        self.referencia = referencia
        self.identificador = identificador
        self.date = date
        self._quantidade_disponivel = quantidade
        self._alocacoes = set() # type: Set[Pedido]


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