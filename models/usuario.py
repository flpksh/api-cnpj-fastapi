from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, nullable=False)

    senha = Column(String, nullable=False)

    empresas = relationship("Empresa", back_populates="usuario")
