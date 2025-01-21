from fastapi import APIRouter, HTTPException
from app.db import get_session
from app.models.Usuario import Usuario
from sqlmodel import SQLModel, Field, Session, create_engine, select


routes = APIRouter(
    tags=['Usuario']
)


def proxima_session():
    session_generator = get_session()
    return next(session_generator)


@routes.post("/criarUsuario")
def criar_usuario(usuario: dict):
    nome = usuario.get("nome")
    idade = usuario.get("idade")
    email = usuario.get("email")

    #verificar se o usuario ja existe com o mesmo email
    session = proxima_session()
    #usuario_existente = Session.query(Usuario).filter(Usuario.email == email).first()
    usuario_existente = session.exec(select(Usuario).where(Usuario.email == email)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Há outro usuário já cadastrado com este email.")

    user = Usuario(nome=nome, idade=idade, email=email)

    #session = proxima_session()  # Obtém a sessão
    created_user = session.add(user)
    session.commit()  # Persiste as alterações
    session.refresh(user)

    return "Usuário cadastrado com sucesso."

@routes.get("/usuarios")
def lista_usuarios():
    """ Retorna todos os usuários do banco de dados."""
    session = proxima_session() # Obtém a sessão
    statement = select(Usuario)
    users = session.exec(statement).all()
    return users

@routes.put("/atualizar/{usuario_id}")
def atualizar_usuario(usuario_id: int, usuario: Usuario):
    session = proxima_session()  # Obtém a sessão
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza os campos fornecidos
    user.nome = usuario.nome or user.nome
    user.idade = usuario.idade or user.idade
    user.email = usuario.email or user.email

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@routes.delete("/deletar/{usuario_id}")
def deletar_usuario(usuario_id : int):
    session = proxima_session()
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado com sucesso"}

@routes.get("/selecionar_usuario/{usuario_id}")
def selecionar_usuario(usuario_id : int):
    session = proxima_session()
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail= "Usuário não encontrado")
    
    return user

