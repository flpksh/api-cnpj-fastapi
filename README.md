# API de Consulta de Empresas (CNPJ)

Projeto desenvolvido com foco em aprendizado prático de backend utilizando FastAPI, PostgreSQL e Docker.

##  Tecnologias utilizadas

- Python
- FastAPI
- PostgreSQL
- Docker
- Uvicorn

## Funcionalidades

- Criar empresa
- Listar empresas
- Buscar empresa por CNPJ
- Atualizar empresa
- Deletar empresa

## Como executar o projeto

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>

#######################################################################################################################################

# API CNPJ

API REST desenvolvida com FastAPI para gerenciamento de empresas e usuários.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- JWT Authentication
- Docker
- Docker Compose

---

# Funcionalidades

- Cadastro de usuários
- Login com JWT
- CRUD de empresas
- Relacionamento usuário → empresas
- Paginação
- Filtros
- Ordenação
- Soft delete
- Auditoria
- Containerização com Docker

---

# Estrutura do Projeto

```bash
api_cnpj/
│
├── core/
├── models/
├── routes/
├── schemas/
├── services/
├── migrations/
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

# Como executar localmente

## Clonar repositório

```bash
git clone https://github.com/flpksh
```

## Entrar na pasta

```bash
cd api_cnpj
```

## Subir containers

```bash
docker compose up --build
```

---

# Acessar documentação

Swagger:

```bash
http://localhost:8000/docs
```

Redoc:

```bash
http://localhost:8000/redoc
```

---

# Autenticação

A API utiliza JWT Bearer Token.

## Fluxo

1. Registrar usuário
2. Fazer login
3. Copiar token
4. Autorizar no Swagger

---

# Endpoints principais

## Auth

- POST `/auth/register`
- POST `/auth/login`

## Empresas

- GET `/empresas`
- POST `/empresas`
- PUT `/empresas/{cnpj}`
- DELETE `/empresas/{cnpj}`

---

# Diferenciais implementados

- Arquitetura organizada
- Segurança JWT
- Soft delete
- Auditoria
- Dockerização
- PostgreSQL
- Alembic migrations

---

# Autor

Luis Felipe
