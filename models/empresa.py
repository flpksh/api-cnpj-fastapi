from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Empresa(Base):

    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    cnpj = Column(String, unique=True, nullable=False)

    nome = Column(String, nullable=False)

    cidade = Column(String)

    estado = Column(String)

    ativo = Column(Boolean, default=True)

    criado_em = Column(DateTime, default=datetime.utcnow)

    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    usuario = relationship("Usuario", back_populates="empresas")
