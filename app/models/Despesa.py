from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.Usuario import Usuario


class Despesa(SQLModel, table=True):
    __tablename__: 'despesas'

    id : int =Field(default=None, nullable=False, primary_key = True)
    valor: float
    descricao: str
    status: str

    usuario_id: int = Field(foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="despesas")
    #falta grupo ter despesas