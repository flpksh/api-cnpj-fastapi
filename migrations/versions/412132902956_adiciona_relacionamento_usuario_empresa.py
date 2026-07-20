"""adiciona relacionamento usuario empresa

Revision ID: 412132902956
Revises: 29134aaa8ba7
Create Date: 2026-05-18 11:31:07.515557
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "412132902956"
down_revision: Union[str, Sequence[str], None] = "29134aaa8ba7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

FK_NAME = "fk_empresas_usuario_id"


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "empresas",
        sa.Column("usuario_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        FK_NAME,
        "empresas",
        "usuarios",
        ["usuario_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        FK_NAME,
        "empresas",
        type_="foreignkey",
    )

    op.drop_column(
        "empresas",
        "usuario_id",
    )
