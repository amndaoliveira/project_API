from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models.Usuario import Usuario
from app.models.UsuarioGrupo import UsuarioGrupo

class Grupo(SQLModel, table=True):
    __tablename__: 'grupos'
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    descricao: str

    administrador_id: int = Field(default=None, foreign_key="usuario.id", unique=True)
    users: List[Usuario] = Relationship(back_populates="grupos", link_model=UsuarioGrupo)
    administrador: Usuario = Relationship(back_populates="grupo_admin")
    
    # Relacionamento 1:N entre Grupo e Despesa
    despesas: List["Despesa"] = Relationship(back_populates="grupo")