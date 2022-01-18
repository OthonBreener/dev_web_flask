"""
! Padrão de Repositório: situado entre o modelo de dominio e o banco de dados (orm)

Abstração simplificadora sobre armazenamento de dados, permite desacoplar
a camada de modelo da camada de dados. Esse padrão torna o sistema mais
testável, ocultando as complexidades do banco de dados. 

"""


from abc import ABC, abstractmethod
from contexto_de_negocio.alocacoes.dominio.models import LoteMercadoriaDisponivel
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
