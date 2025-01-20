from fastapi import APIRouter, HTTPException, Response
from app.db import get_session
from app.models.Grupo import Grupo
from sqlmodel import SQLModel, Field, Session, create_engine, select


routes = APIRouter()

def proxima_session():
    session_generator = get_session()
    return next(session_generator)


@routes.post("/criarGrupo/")
def criar_grupo(grupo:Grupo):
    db_grupo = Grupo(nome=grupo.nome, descricao=grupo.descricao)
    session = proxima_session()
    session.add(db_grupo)
    session.commit()
    session.refresh(db_grupo)
    return db_grupo


@routes.get("/grupos/")
def obter_grupos():
    session = proxima_session()
    statement = select(Grupo)
    data = session.exec(statement).all()
    return data
  

@routes.get("/grupos/{grupo_id}", response_model=Grupo)
def obter_grupo(grupo_id: int):
    session = proxima_session()
    grupo = session.get(Grupo, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    return grupo


@routes.put("/grupos/")
def atualizar_grupo(grupo_id: int, grupo: Grupo):
    session = proxima_session()

    db_grupo = session.get(Grupo, grupo_id)
    if not db_grupo:
        raise HTTPException(status_code=404, detail=f"Grupo com ID {grupo_id} não encontrado")
    db_grupo.nome = grupo.nome_grupo
    db_grupo.descricao = grupo.descricao_grupo
    session.commit()
    session.refresh(db_grupo)
    return db_grupo


@routes.delete("/grupos/")
def deletar_grupo(grupo_id: int):
    session = proxima_session()
    grupo = session.query(Grupo).filter(Grupo.id == grupo_id).delete()
    session.commit()
    return Response(status_code=204)



"""
@TODO
- def adicionar_usuario_ao_grupo
- def remover_usuario_do_grupo
"""