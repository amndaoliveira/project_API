from sqlmodel import SQLModel, Field, Relationship
from typing import List

from app.models.UsuarioGrupo import UsuarioGrupo

class Usuario(SQLModel, table=True):
    __tablename__: 'usuarios'

    id: int = Field(default=None, nullable=False, primary_key = True)
    nome: str 
    email: str =Field(default=None, nullable=False, unique=True) #definir o email como chave unica e que não pode haver outro usuário com o mesmo
    idade: int | None = Field(default=None)

    despesas: List['Despesa'] = Relationship(back_populates="usuario", cascade_delete=True)
    
    grupos: List['Grupo'] = Relationship(back_populates="users", link_model=UsuarioGrupo)
    grupo_admin: "Grupo"= Relationship(back_populates="administrador")
