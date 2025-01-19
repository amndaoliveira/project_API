from fastapi import APIRouter
from app.db import get_session
from app.models.Usuario import Usuario
from sqlmodel import SQLModel, Field, Session, create_engine, select


routes = APIRouter()


def proxima_session():
    session_generator = get_session()
    return next(session_generator)

@routes.post("/criarUsuario")
def criar_usuario(usuario: dict):
    nome = usuario.get("nome")
    idade = usuario.get("idade")
    email = usuario.get("email")

    user = Usuario(nome=nome, idade=idade, email=email)

    session = proxima_session()  # Obtém a sessão
    created_user = session.add(user)
    session.commit()  # Persiste as alterações
    session.refresh(user)

    return created_user

@routes.get("/usuarios")
def lista_usuarios():
    """
    Retorna todos os usuários do banco de dados.
    """
    session = proxima_session() # Obtém a sessão
    statement = select(Usuario)
    users = session.exec(statement).all()
    return users

@routes.put("/atualizar")
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


@routes.delete("/deletar")
def deletar_usuario(usuario_is : int):
    session = proxima_session
    user = Session.get(Usuario, usuario_id)
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    session.delete(user)
    session.commit()
    return {"message": "Usuário deletado com sucesso"}