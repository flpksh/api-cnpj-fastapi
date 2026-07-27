import os

import pytest
from sqlalchemy import inspect

from database import engine

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1",
    reason="PostgreSQL integration tests are disabled",
)


def test_postgresql_migrations():
    assert engine.dialect.name == "postgresql"

    inspector = inspect(engine)

    assert {"usuarios", "empresas", "alembic_version"} <= set(
        inspector.get_table_names()
    )

    empresa_columns = {column["name"] for column in inspector.get_columns("empresas")}

    assert {
        "id",
        "cnpj",
        "nome",
        "cidade",
        "estado",
        "usuario_id",
        "ativo",
        "criado_em",
        "atualizado_em",
    } <= empresa_columns
