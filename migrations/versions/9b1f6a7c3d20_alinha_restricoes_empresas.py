"""alinha restricoes empresas

Revision ID: 9b1f6a7c3d20
Revises: 86881d3be44c
Create Date: 2026-08-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9b1f6a7c3d20"
down_revision: str | Sequence[str] | None = "86881d3be44c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    connection = op.get_bind()
    orphan_count = connection.execute(
        sa.text("SELECT COUNT(*) FROM empresas WHERE usuario_id IS NULL")
    ).scalar_one()
    if orphan_count:
        raise RuntimeError(
            "Existem empresas sem usuario_id; associe-as antes de aplicar a migração"
        )

    op.execute(sa.text("UPDATE empresas SET ativo = TRUE WHERE ativo IS NULL"))
    op.execute(
        sa.text(
            "UPDATE empresas SET criado_em = CURRENT_TIMESTAMP WHERE criado_em IS NULL"
        )
    )
    op.execute(
        sa.text(
            "UPDATE empresas SET atualizado_em = CURRENT_TIMESTAMP "
            "WHERE atualizado_em IS NULL"
        )
    )

    op.drop_constraint("empresas_cnpj_key", "empresas", type_="unique")
    op.create_unique_constraint(
        "uq_empresas_usuario_cnpj", "empresas", ["usuario_id", "cnpj"]
    )
    op.alter_column(
        "empresas", "usuario_id", existing_type=sa.Integer(), nullable=False
    )
    op.alter_column("empresas", "ativo", existing_type=sa.Boolean(), nullable=False)
    op.alter_column(
        "empresas", "criado_em", existing_type=sa.DateTime(), nullable=False
    )
    op.alter_column(
        "empresas", "atualizado_em", existing_type=sa.DateTime(), nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        "empresas", "atualizado_em", existing_type=sa.DateTime(), nullable=True
    )
    op.alter_column("empresas", "criado_em", existing_type=sa.DateTime(), nullable=True)
    op.alter_column("empresas", "ativo", existing_type=sa.Boolean(), nullable=True)
    op.alter_column("empresas", "usuario_id", existing_type=sa.Integer(), nullable=True)
    op.drop_constraint("uq_empresas_usuario_cnpj", "empresas", type_="unique")
    op.create_unique_constraint("empresas_cnpj_key", "empresas", ["cnpj"])
