from typing import Literal
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import database, services
from models import ReservaEntrada, ReservaAtualizacao, ReservaSaida

database.criar_tabela()
app=FastAPI(title="Sistema de Reservas de Laboratórios")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5500","http://127.0.0.1:5500"],allow_methods=["*"],allow_headers=["*"])

@app.get("/api/status")
def status() -> dict[str, str]:
    return {"status":"online"}

def erro(exc):
    if isinstance(exc,services.ReservaNaoEncontrada): raise HTTPException(404,str(exc))
    if isinstance(exc,services.ConflitoReserva): raise HTTPException(409,str(exc))

@app.post("/api/reservas",response_model=ReservaSaida,status_code=201)
def criar(dados:ReservaEntrada):
    try: return services.criar_reserva(dados)
    except (services.ConflitoReserva,services.ReservaNaoEncontrada) as e: erro(e)

@app.get("/api/reservas",response_model=list[ReservaSaida])
def listar(status:Literal["confirmada","pendente","cancelada"]|None=None,laboratorio:str|None=None):
    return services.listar_reservas(status,laboratorio)

@app.get("/api/reservas/{reserva_id}",response_model=ReservaSaida)
def obter(reserva_id:int):
    try: return services.obter_reserva(reserva_id)
    except services.ReservaNaoEncontrada as e: erro(e)

@app.put("/api/reservas/{reserva_id}",response_model=ReservaSaida)
def atualizar(reserva_id:int,dados:ReservaAtualizacao):
    try: return services.atualizar_reserva(reserva_id,dados)
    except (services.ConflitoReserva,services.ReservaNaoEncontrada) as e: erro(e)

@app.delete("/api/reservas/{reserva_id}",status_code=204)
def excluir(reserva_id:int):
    try: services.excluir_reserva(reserva_id); return Response(status_code=204)
    except services.ReservaNaoEncontrada as e: erro(e)
