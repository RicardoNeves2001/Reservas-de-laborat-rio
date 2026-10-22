# Alunos:
Ricardo da Silva Neves
Thiago Penetra

# Sistema de Reservas de Laboratórios
Exemplo didático Full Stack alinhado aos cinco encontros: HTML/CSS → JavaScript/Fetch → HTTP → FastAPI/Pydantic → serviço → SQLite.

## Executar no VS Code (PowerShell)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn main:app --reload
```
Em outro terminal:
```powershell
cd frontend
py -m http.server 5500
```
Abra `http://localhost:5500` e o Swagger em `http://127.0.0.1:8000/docs`.

## Sequência guiada
1. `database.py`: conexão, tabela e persistência.
2. `models.py`: contrato e validação estrutural.
3. `services.py`: CRUD, filtros, SQL e conflito.
4. `main.py`: endpoints, códigos HTTP e tradução de exceções.
5. `frontend/app.js`: objeto JS, JSON, Fetch e DOM.
6. `tests/test_api.py`: testes de integração, incluindo os limites de quantidade de alunos.

## Quantidade de alunos
O campo `quantidade_alunos` (1 a 40) percorre HTML, JavaScript, Pydantic, SQLite, SQL, contrato e testes.
