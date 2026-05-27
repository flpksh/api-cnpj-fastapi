from sqlalchemy.orm import Session

from models.empresa import Empresa


def listar_empresas(db: Session):

    return db.query(Empresa).all()


def buscar_empresa_por_cnpj(
    cnpj: str,
    db: Session
):

    return db.query(Empresa).filter(
        Empresa.cnpj == cnpj
    ).first()


def criar_empresa(
    nova_empresa: Empresa,
    db: Session
):

    db.add(nova_empresa)

    db.commit()

    db.refresh(nova_empresa)

    return nova_empresa


def atualizar_empresa(
    db: Session
):

    db.commit()


def deletar_empresa(
    empresa: Empresa,
    db: Session
):

    db.delete(empresa)

    db.commit()
