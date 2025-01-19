from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    __tablename__: 'usuarios'
    nome: str 
    email: str
    idade: int | None = Field(default=None)
  