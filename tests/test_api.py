import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/"backend"))
import database
from fastapi.testclient import TestClient
from main import app
client=TestClient(app)
BASE={"laboratorio":"Lab 01","responsavel":"Ana","data":"2026-10-10","turno":"manha","finalidade":"Aula prática","status":"confirmada","quantidade_alunos":25}
def test_status_online():
    r=client.get('/api/status'); assert r.status_code==200; assert r.json()=={"status":"online"}
def setup_function():
    database.criar_tabela()
    with database.conectar() as c: c.execute("DELETE FROM reservas")
def test_criar_listar_consultar():
    r=client.post('/api/reservas',json=BASE); assert r.status_code==201; assert r.json()["quantidade_alunos"]==25; rid=r.json()['id']; assert client.get('/api/reservas').status_code==200; assert client.get(f'/api/reservas/{rid}').json()["quantidade_alunos"]==25
def test_conflito_409():
    assert client.post('/api/reservas',json=BASE).status_code==201; assert client.post('/api/reservas',json=BASE).status_code==409
def test_turno_invalido_422():
    d={**BASE,"turno":"madrugada"}; assert client.post('/api/reservas',json=d).status_code==422
def test_quantidade_alunos_limites_inclusivos():
    for quantidade in (1,40):
        r=client.post('/api/reservas',json={**BASE,"laboratorio":f"Lab {quantidade}","quantidade_alunos":quantidade})
        assert r.status_code==201; assert r.json()["quantidade_alunos"]==quantidade
def test_quantidade_alunos_fora_dos_limites():
    for quantidade in (0,41):
        r=client.post('/api/reservas',json={**BASE,"quantidade_alunos":quantidade})
        assert r.status_code==422; assert r.json()["detail"][0]["loc"]==["body","quantidade_alunos"]
def test_quantidade_alunos_obrigatoria():
    dados={k:v for k,v in BASE.items() if k!="quantidade_alunos"}
    r=client.post('/api/reservas',json=dados)
    assert r.status_code==422; assert r.json()["detail"][0]["loc"]==["body","quantidade_alunos"]
def test_filtro_laboratorio():
    client.post('/api/reservas',json=BASE); r=client.get('/api/reservas?laboratorio=01'); assert len(r.json())==1
def test_excluir_204_depois_404():
    rid=client.post('/api/reservas',json=BASE).json()['id']; assert client.delete(f'/api/reservas/{rid}').status_code==204; assert client.delete(f'/api/reservas/{rid}').status_code==404
