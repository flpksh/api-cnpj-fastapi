from sqlalchemy.orm import Session

from models.empresa import Empresa


def buscar_por_usuario(
    db: Session,
    usuario_id: int,
):

    return (
        db.query(Empresa)
        .filter(
            Empresa.usuario_id == usuario_id,
            Empresa.ativo,
        )
    )


def buscar_por_cnpj(
    db: Session,
    cnpj: str,
    usuario_id: int,
):

    return (
        db.query(Empresa)
        .filter(
            Empresa.cnpj == cnpj,
            Empresa.usuario_id == usuario_id,
            Empresa.ativo,
        )
        .first()
    )


def criar(
    db: Session,
    empresa: Empresa,
):

    db.add(empresa)

    db.commit()

    db.refresh(empresa)

    return empresa


def atualizar(db: Session):

    db.commit()


def deletar(
    db: Session,
    empresa: Empresa,
):

    empresa.ativo = False

    db.commit()