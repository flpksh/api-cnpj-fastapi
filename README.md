# API CNPJ (Ainda em desenvolvimento)

API REST desenvolvida com **FastAPI** para gerenciamento de usuários e empresas, aplicando boas práticas de desenvolvimento backend, arquitetura em camadas e documentação automática de APIs.

O projeto foi desenvolvido utilizando uma arquitetura organizada em **Routes → Services → Repositories → Models**, com autenticação JWT, banco de dados relacional, migrações versionadas e conteinerização com Docker.

---

## Tecnologias

### Backend

* Python 3.12
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Banco de Dados

* PostgreSQL
* Alembic (Migrations)

### Segurança

* JWT Authentication
* Hash de senhas

### DevOps

* Docker
* Docker Compose
* GitHub Actions (CI)

### Testes

* Pytest

---

# Funcionalidades

## Autenticação

* Cadastro de usuários
* Login com JWT
* Proteção de rotas autenticadas

## Empresas

* Cadastro de empresas
* Validação de CNPJ numérico e alfanumérico
* Listagem paginada
* Consulta por CNPJ
* Atualização de empresas
* Soft Delete
* Auditoria de registros

## Recursos adicionais

* Paginação
* Filtros
* Ordenação
* Tratamento global de exceções
* Respostas padronizadas
* Documentação automática com Swagger/OpenAPI

---

# Arquitetura

```text
Cliente
    │
    ▼
FastAPI
    │
    ▼
Routes
    │
    ▼
Services
    │
    ▼
Repositories
    │
    ▼
PostgreSQL
```

### Organização do projeto

```text
api_cnpj/
│
├── core/
│   ├── cnpj.py
│   ├── config.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── responses.py
│   └── security.py
│
├── database/
│
├── migrations/
│
├── models/
│
├── repositories/
│
├── routes/
│
├── schemas/
│
├── services/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
└── README.md
```

---

# Endpoints

## Autenticação

| Método | Endpoint       | Descrição              |
| ------ | -------------- | ---------------------- |
| POST   | /auth/register | Cadastro de usuário    |
| POST   | /auth/login    | Login e geração do JWT |

---

## Empresas

| Método | Endpoint         | Descrição                    |
| ------ | ---------------- | ---------------------------- |
| GET    | /empresas/       | Lista empresas               |
| POST   | /empresas/       | Cadastra empresa             |
| PUT    | /empresas/{cnpj} | Atualiza empresa             |
| DELETE | /empresas/{cnpj} | Remove empresa (Soft Delete) |

### Formato do CNPJ

A API aceita o formato numérico tradicional e o novo formato alfanumérico,
mantendo os dois últimos caracteres como dígitos verificadores. Pontos, barra e
hífen são removidos, e letras são normalizadas para maiúsculas antes da
validação pelo módulo 11.

Exemplos válidos: `12.345.678/0001-95` e `12.ABC.345/01DE-35`. Nas rotas que
recebem `{cnpj}`, use o valor sem pontuação, como `12ABC34501DE35`.

### Paginação, filtros e ordenação

O endpoint `GET /empresas/` aceita os seguintes parâmetros de consulta:

| Parâmetro | Padrão | Descrição                                  |
| --------- | ------ | ------------------------------------------ |
| page      | 1      | Página da listagem                         |
| limit     | 10     | Quantidade de registros por página         |
| cidade    | —      | Filtra empresas por cidade                 |
| estado    | —      | Filtra empresas por estado                 |
| ordem     | id     | Campo utilizado para ordenar os resultados |
| direcao   | asc    | Direção da ordenação (`asc` ou `desc`)     |

Exemplo:

```text
GET /empresas/?page=1&limit=10&estado=SC&ordem=nome&direcao=asc
```

---

# Como executar

## Clonar o projeto

```bash
git clone https://github.com/flpksh/api-cnpj-fastapi.git
```

```bash
cd api-cnpj-fastapi
```

---

## Configurar o ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Preencha o `.env` com os dados do banco e uma chave secreta:

```env
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=cnpj_db
SECRET_KEY=substitua-por-uma-chave-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Executar localmente

Crie e ative um ambiente virtual, instale as dependências e aplique as migrações:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
alembic upgrade head
```

Inicie a API:

```bash
uvicorn main:app --reload
```

A aplicação fica disponível em:

```text
http://localhost:8000
```

## Executar com Docker Compose

Depois de configurar o `.env`, inicie a API e o PostgreSQL:

```bash
docker compose up --build
```

A API fica disponível em `http://localhost:8000` e o PostgreSQL é exposto na
porta `5433` da máquina local.

---

# Documentação da API

Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Autenticação

A API utiliza autenticação baseada em **JWT Bearer Token**.

Fluxo de autenticação:

1. Registrar um usuário
2. Realizar login
3. Receber o Access Token
4. Informar o token no botão **Authorize** do Swagger
5. Consumir os endpoints protegidos

---

# Estrutura das respostas

A maioria das operações da API retorna respostas padronizadas. O login retorna
diretamente o token de acesso, conforme descrito na documentação OpenAPI.

### Sucesso

```json
{
  "success": true,
  "message": "Operação realizada com sucesso.",
  "data": {}
}
```

### Erro

```json
{
  "success": false,
  "message": "Empresa não encontrada.",
  "data": null
}
```

---

# Diferenciais do projeto

* Arquitetura em camadas (Routes, Services e Repositories)
* Repository Pattern
* Separação entre regras de negócio e acesso a dados
* Autenticação JWT
* Tratamento global de exceções
* Soft Delete
* Auditoria de registros
* Paginação, filtros e ordenação
* Documentação automática com Swagger/OpenAPI
* Migrações de banco com Alembic
* Conteinerização com Docker
* Testes automatizados com Pytest

---

# Próximas evoluções

* Deploy em ambiente cloud
* Observabilidade com Prometheus e Grafana
* Cache com Redis
* Cobertura de testes ampliada
* Entrega contínua (CD)

---

# Qualidade e testes

Instale as dependências de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

Execute os testes:

```bash
pytest -v
```

Execute as mesmas verificações utilizadas pela integração contínua:

```bash
black --check .
isort --check-only .
ruff check .
mypy .
pytest -v
```

O workflow está definido em `.github/workflows/ci.yml` e é executado em pushes e
pull requests direcionados à branch `main`.

---

# Autor

**Luis Felipe**

Desenvolvedor Backend focado em Python, FastAPI, APIs REST e arquitetura de software.
