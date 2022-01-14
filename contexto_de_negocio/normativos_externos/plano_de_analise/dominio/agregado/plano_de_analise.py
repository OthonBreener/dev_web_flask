from dataclasses import dataclass
from datetime import datetime

@dataclass
class PlanodeAnalise:
    normativo: NormativoExterno
    descricao_risco: str
    grau_de_risco: str
    observacao: str
    data_de_adequacao: datetime
    politica_requirida: str
    politica_interna: str
    anexos: ADefinir
