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
| GET    | /empresas        | Lista empresas               |
| GET    | /empresas/{cnpj} | Busca empresa por CNPJ       |
| POST   | /empresas        | Cadastra empresa             |
| PUT    | /empresas/{cnpj} | Atualiza empresa             |
| DELETE | /empresas/{cnpj} | Remove empresa (Soft Delete) |

---

# Como executar

## Clonar o projeto

```bash
git clone https://github.com/flpksh/api_cnpj.git
```

```bash
cd api_cnpj
```

---

## Executar com Docker

```bash
docker compose up --build
```

A aplicação ficará disponível em:

```
http://localhost:8000
```

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

A API retorna respostas padronizadas.

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

* Pipeline CI/CD
* Deploy em ambiente cloud
* Observabilidade com Prometheus e Grafana
* Cache com Redis
* Cobertura de testes ampliada
* Integração contínua

---

# Autor

**Luis Felipe**

Desenvolvedor Backend focado em Python, FastAPI, APIs REST e arquitetura de software.
