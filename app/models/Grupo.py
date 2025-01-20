from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models.Usuario import Usuario
from app.models.UsuarioGrupo import UsuarioGrupo

class Grupo(SQLModel, table=True):
    __tablename__: 'grupos'
    
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    descricao: str

    users: List[Usuario] = Relationship(back_populates="grupos", link_model=UsuarioGrupo)
    