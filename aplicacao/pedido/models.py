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
        self.quantidade_disponivel = quantidade


    def alocar_pedido(self, pedido: Pedido) -> None:
        self.quantidade_disponivel -= pedido.quantidade
    

    def pode_alocar(self, pedido: Pedido) -> bool:

        return (self.identificador == pedido.identificador
            and self.quantidade_disponivel >= pedido.quantidade)