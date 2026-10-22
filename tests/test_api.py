import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))

import database
from main import app

BASE = {
    "laboratorio": "Lab 01",
    "responsavel": "Ana",
    "data": "2026-10-10",
    "turno": "manha",
    "finalidade": "Aula prática",
    "status": "confirmada",
    "quantidade_alunos": 25,
}


@pytest.fixture
def isolated_database(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "CAMINHO_BANCO", tmp_path / "reservas.db")


@pytest.fixture
def client(isolated_database):
    with TestClient(app) as test_client:
        yield test_client


def test_status_online(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}


def test_criar_listar_consultar(client):
    response = client.post("/api/reservas", json=BASE)
    assert response.status_code == 201
    assert response.json()["quantidade_alunos"] == 25
    reserva_id = response.json()["id"]

    assert client.get("/api/reservas").status_code == 200
    assert client.get(f"/api/reservas/{reserva_id}").json()["quantidade_alunos"] == 25


def test_conflito_409_ignora_espacos_e_maiusculas(client):
    assert client.post("/api/reservas", json=BASE).status_code == 201
    conflito = {**BASE, "laboratorio": "  LAB 01  "}

    response = client.post("/api/reservas", json=conflito)
    assert response.status_code == 409
    assert response.json()["detail"] == "Horário já reservado para este laboratório."


def test_turno_invalido_422(client):
    response = client.post("/api/reservas", json={**BASE, "turno": "madrugada"})
    assert response.status_code == 422


def test_quantidade_alunos_limites_inclusivos(client):
    for quantidade in (1, 40):
        response = client.post(
            "/api/reservas",
            json={
                **BASE,
                "laboratorio": f"Lab {quantidade}",
                "quantidade_alunos": quantidade,
            },
        )
        assert response.status_code == 201
        assert response.json()["quantidade_alunos"] == quantidade


def test_quantidade_alunos_fora_dos_limites(client):
    for quantidade in (0, 41):
        response = client.post(
            "/api/reservas",
            json={**BASE, "quantidade_alunos": quantidade},
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "quantidade_alunos"]


def test_quantidade_alunos_obrigatoria(client):
    dados = {key: value for key, value in BASE.items() if key != "quantidade_alunos"}
    response = client.post("/api/reservas", json=dados)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "quantidade_alunos"]


def test_filtros_por_status_e_nome_parcial(client):
    client.post("/api/reservas", json=BASE)
    pendente = {
        **BASE,
        "laboratorio": "Lab 02",
        "status": "pendente",
        "turno": "tarde",
    }
    client.post("/api/reservas", json=pendente)

    por_status = client.get("/api/reservas?status_reserva=pendente")
    por_laboratorio = client.get("/api/reservas?laboratorio=02")
    assert por_status.status_code == 200
    assert [item["laboratorio"] for item in por_status.json()] == ["Lab 02"]
    assert por_laboratorio.status_code == 200
    assert [item["laboratorio"] for item in por_laboratorio.json()] == ["Lab 02"]


def test_filtro_status_legado(client):
    client.post("/api/reservas", json=BASE)
    response = client.get("/api/reservas?status=confirmada")
    assert response.status_code == 200
    assert [item["laboratorio"] for item in response.json()] == ["Lab 01"]


def test_consulta_inexistente_404(client):
    response = client.get("/api/reservas/999")
    assert response.status_code == 404


def test_atualizar_reserva(client):
    reserva_id = client.post("/api/reservas", json=BASE).json()["id"]
    response = client.put(
        f"/api/reservas/{reserva_id}",
        json={**BASE, "laboratorio": "Lab atualizado", "quantidade_alunos": 30},
    )

    assert response.status_code == 200
    assert response.json()["laboratorio"] == "Lab atualizado"
    assert response.json()["quantidade_alunos"] == 30


def test_persistencia_apos_reiniciar_aplicacao(isolated_database):
    with TestClient(app) as first_client:
        created = first_client.post("/api/reservas", json=BASE)
        assert created.status_code == 201
        reserva_id = created.json()["id"]

    with TestClient(app) as restarted_client:
        response = restarted_client.get(f"/api/reservas/{reserva_id}")

    assert response.status_code == 200
    assert response.json()["laboratorio"] == BASE["laboratorio"]


def test_excluir_204_depois_404(client):
    reserva_id = client.post("/api/reservas", json=BASE).json()["id"]
    assert client.delete(f"/api/reservas/{reserva_id}").status_code == 204
    assert client.delete(f"/api/reservas/{reserva_id}").status_code == 404
