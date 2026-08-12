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

* JWT Authentication com expiração obrigatória
* Hash de senhas com Argon2id e migração automática de bcrypt

### DevOps

* Docker
* Docker Compose
* GitHub Actions (CI)

### Testes

* Pytest

---

# Funcionalidades

## Autenticação

* Cadastro de usuários com validação de credenciais
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
│   ├── middleware.py
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

## Operação

| Método | Endpoint      | Descrição                             |
| ------ | ------------- | ------------------------------------- |
| GET    | /health/live  | Confirma que o processo está ativo    |
| GET    | /health/ready | Confirma o acesso da aplicação ao banco |

Todas as respostas incluem o cabeçalho `X-Request-ID`. Um identificador válido
enviado pelo cliente é preservado; caso contrário, a API gera um UUID. Os logs
são enviados para a saída padrão com método, caminho, status e duração.

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
| page      | 1      | Página da listagem (mínimo: 1)             |
| limit     | 10     | Registros por página (entre 1 e 100)       |
| cidade    | —      | Filtra por cidade (até 100 caracteres)     |
| estado    | —      | Filtra por UF (duas letras)                |
| ordem     | id     | `id`, `nome`, `cnpj`, `cidade` ou `estado` |
| direcao   | asc    | `asc` ou `desc`                            |

Exemplo:

```text
GET /empresas/?page=1&limit=10&estado=SC&ordem=nome&direcao=asc
```

Parâmetros inválidos ou desconhecidos retornam `422`. A resposta informa
`page`, `limit`, `total` de registros e `pages` com o total de páginas.

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
SECRET_KEY=
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
porta `5434` da máquina local.

O Compose exige uma `SECRET_KEY` preenchida e não inicia com um placeholder de
desenvolvimento. O container da API executa como usuário sem privilégios e usa
`/health/ready` para informar seu estado ao Docker.

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

A API utiliza autenticação baseada em **JWT Bearer Token**. A chave JWT deve
ter pelo menos 32 caracteres e pode ser gerada com
`python -c "import secrets; print(secrets.token_hex(32))"`.

Novos usuários precisam informar um identificador de 3 a 50 caracteres, usando
letras, números, ponto, hífen ou sublinhado. A senha deve ter entre 15
caracteres e 72 bytes. Novos hashes usam Argon2id; hashes bcrypt existentes são
migrados automaticamente após um login válido.

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
* Health checks de liveness e readiness
* Logs correlacionados por `X-Request-ID`
* Rate limiting de tentativas de login
* Testes automatizados com Pytest
* Cobertura mínima de 85%

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
pytest --cov --cov-report=term-missing
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

O limite padrão de login é de 5 tentativas por endereço em 60 segundos. Em
execuções com múltiplas instâncias, substitua o armazenamento em memória por
um backend compartilhado, como Redis.

## Portas locais

Por padrão, a API usa `8000` e o PostgreSQL usa `5434` na máquina local. As
portas podem ser alteradas por `API_HOST_PORT` e `DB_HOST_PORT` no `.env`.

A combinação `(usuario_id, cnpj)` é única: usuários diferentes podem cadastrar
a mesma empresa sem quebrar o isolamento de propriedade.

---

# Autor

**Luis Felipe**

Desenvolvedor Backend focado em Python, FastAPI, APIs REST e arquitetura de software.
