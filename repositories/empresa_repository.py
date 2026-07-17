from sqlalchemy.orm import Query, Session

from models.empresa import Empresa


def buscar_por_usuario(
    db: Session,
    usuario_id: int,
) -> Query[Empresa]:
    return db.query(Empresa).filter(
        Empresa.usuario_id == usuario_id,
        Empresa.ativo.is_(True),
    )


def buscar_por_cnpj(
    db: Session,
    cnpj: str,
    usuario_id: int,
) -> Empresa | None:
    return (
        db.query(Empresa)
        .filter(
            Empresa.cnpj == cnpj,
            Empresa.usuario_id == usuario_id,
            Empresa.ativo.is_(True),
        )
        .first()
    )


def criar(
    db: Session,
    empresa: Empresa,
) -> Empresa:
    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return empresa


def atualizar(
    db: Session,
    empresa: Empresa,
) -> Empresa:
    db.commit()
    db.refresh(empresa)

    return empresa


def deletar(
    db: Session,
    empresa: Empresa,
) -> None:
    empresa.ativo = False
    db.commit()