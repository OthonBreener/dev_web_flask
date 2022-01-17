from abc import ABC, abstractmethod
from aplicacao.alocacoes.dominio.models import LoteMercadoriaDisponivel
from typing import List


class RepositorioAbstrato(ABC):

    @abstractmethod
    def add(self, lote: LoteMercadoriaDisponivel):
        raise NotImplementedError
    
    @abstractmethod
    def get(self, referencia) -> LoteMercadoriaDisponivel:
        raise NotImplementedError


class RepositorioSqlAlchemy(RepositorioAbstrato):

    def __init__(self, session) -> None:
        self.session = session
    
    def add(self, lote: LoteMercadoriaDisponivel) -> None:
        self.session.add(lote)
    
    def get(self, referencia: str) -> LoteMercadoriaDisponivel:
        return self.session.query(LoteMercadoriaDisponivel).filter_by(referencia=referencia).one()

    def list(self) -> List[LoteMercadoriaDisponivel]:
        return self.session.query(LoteMercadoriaDisponivel).all()


class RepositorioFake(RepositorioAbstrato):

    def __init__(self, lotes: LoteMercadoriaDisponivel) -> None:
        self._lotes = set(lotes)

    def add(self, lote: LoteMercadoriaDisponivel) -> None:
        self._lotes.add(lote)

    def get(self, referencia: str) -> LoteMercadoriaDisponivel:
        return next(lote for lote in self._lotes if lote.referencia == referencia)

    def list(self) -> List[LoteMercadoriaDisponivel]:
        return list(self._lotes)
