from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.usuario import Usuario


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    cnpj: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    nome: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    cidade: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    estado: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="empresas",
    )
