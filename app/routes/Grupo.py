from fastapi import APIRouter, HTTPException, Response
from app.db import get_session
from app.models.Grupo import Grupo
from sqlmodel import SQLModel, Field, Session, create_engine, select

from app.models.Usuario import Usuario
from app.models.UsuarioGrupo import UsuarioGrupo


routes = APIRouter(
    tags=['Grupo',
          'Usuario',
          'UsuarioGrupo']
)

def proxima_session():
    session_generator = get_session()
    return next(session_generator)


@routes.post("/criarGrupo/")
def criar_grupo(grupo:Grupo):
    db_grupo = Grupo(nome=grupo.nome, descricao=grupo.descricao, administrador_id=grupo.administrador_id)
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
  

@routes.get("/grupos/{grupo_id}")
def obter_grupo(grupo_id: int):
    session = proxima_session()
    grupo = session.get(Grupo, grupo_id)
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
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


@routes.delete("/grupo_delete/{grupo_id}")
def deletar_grupo(grupo_id: int):
    session = proxima_session()
    grupo = session.query(Grupo).filter(Grupo.id == grupo_id).delete()
    session.commit()
    return Response(status_code=204)

@routes.post("/add_user_ao_grupo/{usuario_id}/{grupo_id}")
def add_user_ao_grupo(grupo_id : int, usuario_id: int):
    
    session = proxima_session()

    #BUSCAR O GRUPO E O USUÁRIO
    grupo = session.get(Grupo, grupo_id)
    usuario = session.get(Usuario, usuario_id)

    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # #SE O USUARIO JA ESTIVER NO GRUPO
    statement = select(UsuarioGrupo).where(UsuarioGrupo.grupo_id == grupo_id).where(UsuarioGrupo.user_id == usuario_id)
    usuario_existente = session.exec(statement).first()
    if usuario_existente:
        raise HTTPException(status_code=404, detail="Usuário já está no grupo.")

    #ADICIONAR O USUARIO AO GRUPO
    add_user = UsuarioGrupo(user_id= usuario_id, grupo_id=grupo_id)
    session.add(add_user)
    session.commit()
    session.refresh(add_user)

    #return {"messagem": f"usuario {usuario.nome} adicionado ao grupo {grupo.nome}"}
    return add_user

@routes.delete("/remover_do_grupo/{usuario_id}/{grupo_id}")
def remover_do_grupo(grupo_id : int, usuario_id : int):
    session = proxima_session()

    grupo = session.get(Grupo, grupo_id)
    usuario = session.get(Usuario, usuario_id)

    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    #O USUARIO NÃO ESTÁ NO GRUPO
    statement = select(UsuarioGrupo).where(UsuarioGrupo.grupo_id == grupo_id).where(UsuarioGrupo.user_id == usuario_id)
    relacao = session.exec(statement).first()

    if not relacao:
        raise HTTPException(status_code=400, detail="Usuário não encontrado neste grupo")

    #REMOVER O USUARIO DO GRUPO
    grupo.users.remove(usuario)
    session.commit()

    return {"mensagem": f"Usuário {usuario.nome} removido do grupo {grupo.nome}"}

@routes.get("/listar_user_grupo/{grupo_id}")
def listar_users_grupo(grupo_id : int):
    session = proxima_session()

    grupo_id = session.get(Grupo, grupo_id)
    if not grupo_id:
            raise HTTPException(status_code=404, detail="Grupo não encontrado.")
    return grupo_id.users


