from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field

Turno = Literal["manha", "tarde", "noite"]
Status = Literal["confirmada", "pendente", "cancelada"]

class ReservaEntrada(BaseModel):
    laboratorio: str = Field(min_length=2, max_length=60)
    responsavel: str = Field(min_length=2, max_length=100)
    data: date
    turno: Turno
    finalidade: str = Field(min_length=3, max_length=200)
    status: Status = "confirmada"
    quantidade_alunos: int = Field(ge=1, le=40)

class ReservaAtualizacao(ReservaEntrada):
    pass

class ReservaSaida(ReservaEntrada):
    id: int
    data_criacao: datetime
