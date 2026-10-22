# Sistema de Reservas de Laboratórios

Aplicação didática full stack que demonstra HTML/CSS, JavaScript/Fetch, HTTP, FastAPI, Pydantic, serviços e persistência em SQLite.

## Integrantes

- Ricardo da Silva Neves
- Thiago Penetra

## Requisitos

- Python 3.10 ou superior
- VS Code (opcional)

## Executar no Windows (PowerShell)

No primeiro terminal, a partir da pasta raiz do projeto:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Se o PowerShell bloquear a ativação, permita-a somente na sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Executar no macOS ou Linux

No primeiro terminal, a partir da pasta raiz do projeto:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Executar o front-end

Mantenha o terminal da API em execução. Abra um segundo terminal na raiz do projeto:

```bash
cd frontend
python3 -m http.server 5500
```

No Windows, `py -m http.server 5500` também pode ser usado. Acesse:

- Aplicação: <http://localhost:5500>
- Documentação interativa da API: <http://127.0.0.1:8000/docs>

## Persistência e regra de conflito

Os dados são armazenados em `backend/reservas.db`. A tabela é criada quando a API inicia, e os registros permanecem após reiniciar o Uvicorn. Se o banco de uma versão anterior ainda não tiver a coluna `quantidade_alunos`, a inicialização adiciona essa coluna.

Não é permitido criar duas reservas ativas para o mesmo laboratório, data e turno. Uma tentativa conflitante retorna HTTP `409`; reservas canceladas não bloqueiam o horário. O campo `quantidade_alunos` é obrigatório e deve estar entre 1 e 40.

## Endpoints

| Método | Caminho | Comportamento |
|---|---|---|
| `GET` | `/api/status` | Informa o estado da API. |
| `POST` | `/api/reservas` | Cria uma reserva (`201`); conflito retorna `409`. |
| `GET` | `/api/reservas` | Lista reservas. |
| `GET` | `/api/reservas/{id}` | Consulta uma reserva (`404` se não existir). |
| `PUT` | `/api/reservas/{id}` | Atualiza uma reserva; conflito retorna `409`. |
| `DELETE` | `/api/reservas/{id}` | Exclui uma reserva (`204`; `404` se não existir). |

A listagem aceita filtros combináveis:

- `GET /api/reservas?status_reserva=confirmada`
- `GET /api/reservas?laboratorio=02` (busca parcial pelo nome do laboratório)

## Testes

Com o ambiente virtual ativado e na pasta raiz do projeto:

```bash
python -m pytest -q tests/test_api.py
```

Os testes cobrem criação, consulta, atualização, exclusão, persistência após reiniciar a aplicação, filtros, conflito e validação da quantidade de alunos.

## Organização do projeto

- `backend/main.py`: aplicação FastAPI e rotas HTTP.
- `backend/database.py`: caminho, conexão e inicialização do SQLite.
- `backend/models.py`: contratos e validação com Pydantic.
- `backend/services.py`: regras de negócio e operações SQL.
- `frontend/index.html`, `frontend/styles.css` e `frontend/app.js`: interface e integração com a API.
- `tests/test_api.py`: testes automatizados da API.
