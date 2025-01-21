from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.Grupo import Grupo
from app.models.Usuario import Usuario


class Despesa(SQLModel, table=True):
    __tablename__: 'despesas'

    id : int =Field(default=None, nullable=False, primary_key = True)
    valor: float
    descricao: str
    status: str
    
    #relação de usuário com despesa
    usuario_id: int = Field(default= None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="despesas")

    #relação de despesa com grupo
    grupo_id: int | None = Field(default=None, foreign_key="grupo.id")
    grupo: Optional["Grupo"] = Relationship(back_populates="despesas")
    """
    @TODO
    - criar relacao com grupo (adicionar despesa, atualizar despesa, dividir despesa) [ X ]
    - deixar relação com usuario optional (?)
    """
    
    