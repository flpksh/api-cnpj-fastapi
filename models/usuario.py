from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.empresa import Empresa


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    senha: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    empresas: Mapped[list["Empresa"]] = relationship(
        "Empresa",
        back_populates="usuario",
    )
